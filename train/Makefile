# -*-makefile-*-
#
# multi-source models with Marian
# see https://arxiv.org/pdf/1706.04138.pdf
# and https://marian-nmt.github.io/faq
#
#
# MT models using MarianNMT
#
# general parameters / variables
#   SRC ............ set source language      (en)
#   TRG ............ set target language      (de)
#   TESTSET ........ set test set             (newstest2018)
#   MODELTYPE ...... NMT architecture         (transformer)
#   NR ............. model number             (1)
#   DATASET ........ training data set        (ep+nc+rapid)
#   PRE_SRC ........ pre-processing (source)  (bpe50k)
#   PRE_TRG ........ pre-processing (target)  (bpe50k)
#
# 
# set MODELTYPE to multi-transformer to use multi-source architectures
#
#
# submit jobs by adding suffix to make-target to be run
#   .submit ........ job on GPU nodes (for train and translate)
#   .submitcpu ..... job on CPU nodes (for translate and eval)
#
# for example:
#    make train.submit
#
# run a multigpu job
#    make NR_GPUS=4 train-multigpu.submit
#
#
# typical procedure: train and evaluate en-de with 3 models in ensemble
#
# make NR=1 train.submit   (wait until the vocabulary files are created --> FIX THIS)
# make NR=2 train.submit
# make NR=3 train.submit
#
# make NR=1 eval.submit
# make NR=2 eval.submit
# make NR=3 eval.submit
# make eval-ensemble.submit
#
#
# include right-to-left models:
#
# make NR=1 train-RL.submit   (wait until the vocabulary files are created --> FIX THIS)
# make NR=2 train-RL.submit
# make NR=3 train-RL.submit
#
#
#
# finetune:
#
# make NR=1 finetune.submit  (same problem with vocab files as above!)
# make NR=2 finetune.submit  (so, wait until the vocab files are created)
# make NR=3 finetune.submit
#
# make NR=1 MODE=eval finetune.submit
# ...
# make MODE=eval-ensemble finetune.submit
#
#--------------------------------------------------------------------
#
# (1) train NMT model
#
# make train .............. train NMT model for current language pair
#
# (2) translate and evaluate
#
# make translate .......... translate test set
# make eval ............... evaluate
#
#--------------------------------------------------------------------
# train several versions of the same model (for ensembling)
#
#   make NR=1 ....
#   make NR=2 ....
#   make NR=3 ....
#
# DANGER: problem with vocabulary files if you start them simultaneously
#         --> racing situation for creating them between the processes
#
#--------------------------------------------------------------------
# resume training
#
#   make resume
#
#--------------------------------------------------------------------
# translate with ensembles of models
#
#   make translate-ensemble
#   make eval-ensemble
#
# this only makes sense if there are several models
# (created with different NR)
#--------------------------------------------------------------------


# SRCLANGS = da no sv
# TRGLANGS = fi

SRCLANGS = sv
TRGLANGS = fi

ifndef SRC
  SRC := ${firstword ${SRCLANGS}}
endif
ifndef TRG
  TRG := ${lastword ${TRGLANGS}}
endif


include Makefile.def

## all of OPUS
OPUSCORPORA  = ${patsubst %/latest/moses/${LANGPAIR}.txt.zip,%,\
		${patsubst ${OPUSHOME}/%,%,\
		${shell ls ${OPUSHOME}/*/latest/moses/${LANGPAIR}.txt.zip}}}

ALLLANGPAIRS = ${shell ls ${WORKHOME} | grep -- '-' | grep -v old}


## train/dev/test data

TRAINSET = $(filter-out WMT-News ${DEVSET} ${TESTSET},${OPUSCORPORA})
DEVSET   = Tatoeba
TESTSET  = ${DEVSET}
TUNESET  = OpenSubtitles


## size of dev data, test data and BPE merge operations

DEVSIZE     = 5000
DEVMINSIZE  = 1000
TESTSIZE    = 5000
HELDOUTSIZE = ${DEVSIZE}

BPESIZE    = 32000
SRCBPESIZE = ${BPESIZE}
TRGBPESIZE = ${BPESIZE}

ifndef VOCABSIZE
  VOCABSIZE  = $$((${SRCBPESIZE} + ${TRGBPESIZE} + 1000))
endif



## pre-processing type
PRE_SRC   = bpe${SRCBPESIZE:000=}k
PRE_TRG   = bpe${TRGBPESIZE:000=}k

##-------------------------------------
## name of the data set (and the model)
##  - single corpus = use that name
##  - multiple corpora = opus
## add also vocab size to the name
##-------------------------------------

ifndef DATASET
ifeq (${words ${TRAINSET}},1)
  DATASET = ${TRAINSET}
else
  DATASET = opus
endif
endif

MODEL   = ${DATASET}${TRAINSIZE}.${PRE_SRC}-${PRE_TRG}.${lastword ${SRCLANGS}}${lastword ${TRGLANGS}}


## MODELTYPE
MODELTYPE = transformer
NR        = 1

## what to do with fine-tune models
MODE = train


## DATADIR = directory where the train/dev/test data are
## TRAIN   = training data file base name (data should be in DATADIR)

SPACE   = $(empty) $(empty)
LANGSTR = ${subst ${SPACE},+,$(SRCLANGS)}-${subst ${SPACE},+,$(TRGLANGS)}
WORKDIR = ${WORKHOME}/${LANGSTR}
DATADIR = ${WORKHOME}/data

## data sets
TRAIN_SRC = ${WORKDIR}/train/${DATASET}.src
TRAIN_TRG = ${WORKDIR}/train/${DATASET}.trg

## training data in local space
LOCAL_TRAIN_SRC = ${TMPDIR}/train/${DATASET}.src
LOCAL_TRAIN_TRG = ${TMPDIR}/train/${DATASET}.trg

TUNE_SRC  = ${WORKDIR}/tune/${TUNESET}.src
TUNE_TRG  = ${WORKDIR}/tune/${TUNESET}.trg

DEV_SRC   = ${WORKDIR}/val/${DEVSET}.src
DEV_TRG   = ${WORKDIR}/val/${DEVSET}.trg

TEST_SRC  = ${WORKDIR}/test/${TESTSET}.src
TEST_TRG  = ${WORKDIR}/test/${TESTSET}.trg

## heldout data directory (keep one set per data set)
HELDOUT_DIR  = ${WORKDIR}/heldout

## testset dir for all test sets in this language pair
## and all trokenized test sets that can be found in that directory
TESTSET_DIR  = ${PWD}/testsets/${SRC}-${TRG}
TESTSETS     = $(patsubst ${TESTSET_DIR}/%.${SRC}.tok.gz,%,${wildcard ${TESTSET_DIR}/*.${SRC}.tok.gz})


MODEL_BASENAME = ${MODEL}.${MODELTYPE}.model${NR}
MODEL_FINAL    = ${WORKDIR}/${MODEL_BASENAME}.npz.best-perplexity.npz
MODEL_VOCAB    = ${WORKDIR}/${MODEL}.vocab.yml
MODEL_DECODER  = ${MODEL_FINAL}.decoder.yml



## make a distribution package

# DIST_PACKAGE = ${WORKHOME}/models/${LANGSTR}/${DATASET}-${shell date +%F}.zip
DIST_PACKAGE = ${WORKHOME}/models/${LANGSTR}/${DATASET}.zip

.PHONY: dist
dist: ${DIST_PACKAGE}

${DIST_PACKAGE}: ${MODEL_FINAL}
	touch ${WORKDIR}/source.tcmodel
	cp ${BPESRCMODEL} ${WORKDIR}/source.bpe
	sed -e 's# - /.*/\([^/]*\)$$# - \1#' \
	    -e 's/beam-size: [0-9]*$$/beam-size: 6/' \
	    -e 's/mini-batch: [0-9]*$$/mini-batch: 1/' \
	    -e 's/maxi-batch: [0-9]*$$/maxi-batch: 1/' \
	    -e 's/relative-paths: false/relative-paths: true/' \
	< ${MODEL_DECODER} > ${WORKDIR}/decoder.yml
	cd ${WORKDIR} && zip ${notdir $@} \
		${notdir ${MODEL_FINAL}} \
		${notdir ${MODEL_VOCAB}} \
		source.tcmodel source.bpe decoder.yml
	mkdir -p ${dir $@}
	mv -f ${WORKDIR}/${notdir $@} ${@:.zip=}-${shell date +%F}.zip
	rm -f $@
	cd ${dir $@} && ln -s ${notdir ${@:.zip=}-${shell date +%F}.zip} ${notdir $@}
	rm -f ${WORKDIR}/decoder.yml ${WORKDIR}/source.bpe ${WORKDIR}/source.tcmodel
	${MAKE} ${WORKDIR}/${TESTSET}.${MODEL}${NR}.${MODELTYPE}.${SRC}.${TRG}.eval
	${MAKE} ${WORKDIR}/${TESTSET}.${MODEL}${NR}.${MODELTYPE}.${SRC}.${TRG}.compare
	cp ${WORKDIR}/${TESTSET}.${MODEL}${NR}.${MODELTYPE}.${SRC}.${TRG}.eval $(@:.zip=-${shell date +%F}.eval)
	cp ${WORKDIR}/${TESTSET}.${MODEL}${NR}.${MODELTYPE}.${SRC}.${TRG}.compare $(@:.zip=-${shell date +%F}.test)



## eval all available test sets
eval-testsets:
	for s in ${SRCLANGS}; do \
	  for t in ${TRGLANGS}; do \
	    ${MAKE} SRC=$$s TRG=$$t eval-testsets-langpair; \
	  done \
	done

eval-testsets-langpair:
	for t in ${TESTSETS}; do \
	  ${MAKE} TESTSET=$$t eval; \
	done

## extension -all: run over all language pairs, e.g.
## - make eval-all
## - make dist-all
## ...
%-all:
	for l in ${ALLLANGPAIRS}; do \
	  if  [ `find ${WORKHOME}/$$l -name '${DATASET}${TRAINSIZE}.${PRE_SRC}-${PRE_TRG}.*.npz' | wc -l` -gt 0 ]; then \
	    ${MAKE} SRCLANGS="`echo $$l | cut -f1 -d'-' | sed 's/\\+/ /g'`" \
		    TRGLANGS="`echo $$l | cut -f2 -d'-' | sed 's/\\+/ /g'`" ${@:-all=}; \
	  fi \
	done

scores.txt:
	cd ${WORKHOME} && \
	grep base */*eval | cut -f1,2- -d '/' | cut -f1,8- -d '.' | \
	sed 's/.eval:baseline//' | sort  > ${PWD}/$@


## upload to Object Storage
## Don't forget to run this before uploading!
#	source project_2000661-openrc.sh
upload:
	cd ${WORKHOME} && swift upload OPUS-MT --changed --skip-identical models
	swift post OPUS-MT --read-acl ".r:*"

upload-scores: scores.txt
	swift upload OPUS-MT --changed --skip-identical $<



# ## fiskmo benchmark for sv-fi

# FISKMO_SV = ${PWD}/fiskmo_testset.sv.gz
# FISKMO_FI = ${PWD}/fiskmo_testset.fi.gz


# ## benchmark with the fiskmo testset and the current model

# evalfiskmo:
# 	if [ "${filter sv,${SRCLANGS}}" == "sv" ]; then \
# 	  ${MAKE} SRC=sv TRG=fi TESTSET=fiskmo_testset eval; \
# 	fi
# 	if [ "${filter sv,${TRGLANGS}}" == "sv" ]; then \
# 	  ${MAKE} TRG=sv SRC=fi TESTSET=fiskmo_testset eval; \
# 	fi


# ## benchmark with en-fi news data

# evalnews:
# 	if [ "${filter en,${SRCLANGS}}" == "en" ]; then \
# 	  ${MAKE} SRC=en TRG=fi TESTSET=newstest2015.en-fi eval; \
# 	  ${MAKE} SRC=en TRG=fi TESTSET=newstest2016.en-fi eval; \
# 	  ${MAKE} SRC=en TRG=fi TESTSET=newstest2017.en-fi eval; \
# 	  ${MAKE} SRC=en TRG=fi TESTSET=newstest2018.en-fi eval; \
# 	fi
# 	if [ "${filter en,${TRGLANGS}}" == "en" ]; then \
# 	  ${MAKE} TRG=en SRC=fi TESTSET=newstest2015.en-fi eval; \
# 	  ${MAKE} TRG=en SRC=fi TESTSET=newstest2016.en-fi eval; \
# 	  ${MAKE} TRG=en SRC=fi TESTSET=newstest2017.en-fi eval; \
# 	  ${MAKE} TRG=en SRC=fi TESTSET=newstest2018.en-fi eval; \
# 	fi


# #	${MAKE} SRCLANGS=fi TRGLANGS=en SRC=fi TRG=en evalnews
# #	${MAKE} SRCLANGS=fi TRGLANGS=en SRC=fi TRG=en eval

# multi-evalfiskmo:
# 	${MAKE} SRCLANGS="da fo is no nb nn sv" TRGLANGS="et fi" SRC=sv TRG=fi evalfiskmo
# 	${MAKE} TRGLANGS="da fo is no nb nn sv" SRCLANGS="et fi" SRC=fi TRG=sv evalfiskmo


# all-evalfiskmo: 
# 	${MAKE} SRCLANGS=sv TRGLANGS=fi SRC=sv TRG=fi evalfiskmo
# 	${MAKE} TRGLANGS=sv SRCLANGS=fi SRC=fi TRG=sv evalfiskmo
# 	${MAKE} SRCLANGS="da fo is no nb nn sv" TRGLANGS=fi SRC=sv TRG=fi evalfiskmo
# 	${MAKE} SRCLANGS="da fo is no nb nn sv" TRGLANGS='et hu fi' SRC=sv TRG=fi evalfiskmo

#	${MAKE} SRCLANGS="da no nb nn sv" TRGLANGS=fi SRC=sv TRG=fi evalfiskmo
#	${MAKE} TRGLANGS="da no nb nn sv" SRCLANGS=fi SRC=fi TRG=sv evalfiskmo
#	${MAKE} SRCLANGS="de da en no nb nn nl sv" TRGLANGS=fi SRC=sv TRG=fi evalfiskmo
#	${MAKE} TRGLANGS="de da en no nb nn nl sv" SRCLANGS=fi SRC=fi TRG=sv evalfiskmo
#	${MAKE} SRCLANGS="da no nb nn sv" TRGLANGS="fi et" SRC=sv TRG=fi evalfiskmo
#	${MAKE} TRGLANGS="da no nb nn sv" SRCLANGS="fi et" SRC=fi TRG=sv evalfiskmo
#	${MAKE} SRCLANGS="da fo is no nb nn sv" TRGLANGS="fi et hu" SRC=sv TRG=fi evalfiskmo
#	${MAKE} TRGLANGS="da fo is no nb nn sv" SRCLANGS="fi et hu" SRC=fi TRG=sv evalfiskmo
#	${MAKE} SRCLANGS="da no nb nn sv" TRGLANGS="fi et" SRC=sv TRG=fi evalfiskmo
#	${MAKE} TRGLANGS="da no nb nn sv" SRCLANGS="fi et" SRC=fi TRG=sv evalfiskmo

#	${MAKE} SRCLANGS=sv TRGLANGS=fi SRC=sv TRG=fi TRAINSET=Finlex evalfiskmo
#	${MAKE} TRGLANGS=sv SRCLANGS=fi SRC=fi TRG=sv TRAINSET=Finlex evalfiskmo
#	${MAKE} SRCLANGS=sv TRGLANGS=fi SRC=sv TRG=fi TRAINSET=fiskmo evalfiskmo
#	${MAKE} TRGLANGS=sv SRCLANGS=fi SRC=fi TRG=sv TRAINSET=fiskmo evalfiskmo
#	${MAKE} SRCLANGS=sv TRGLANGS=fi SRC=sv TRG=fi TRAINSET=fiskmo TRAINSIZE=100000 evalfiskmo
#	${MAKE} SRCLANGS=sv TRGLANGS=fi SRC=sv TRG=fi TRAINSET=fiskmo TRAINSIZE=500000 evalfiskmo
#	${MAKE} SRCLANGS=sv TRGLANGS=fi SRC=sv TRG=fi TRAINSET=fiskmo TRAINSIZE=1000000 evalfiskmo




run-eval:
	${MAKE} SRCLANGS=sv TRGLANGS=fi SRC=sv TRG=fi evalfiskmo
	${MAKE} TRGLANGS=sv SRCLANGS=fi SRC=fi TRG=sv evalfiskmo
	${MAKE} SRCLANGS=sv TRGLANGS=fi SRC=sv TRG=fi eval
	${MAKE} TRGLANGS=sv SRCLANGS=fi SRC=fi TRG=sv eval
	${MAKE} SRCLANGS=de TRGLANGS=fi SRC=de TRG=fi eval
	${MAKE} SRCLANGS=fi TRGLANGS=fr SRC=fi TRG=fr eval
	${MAKE} SRCLANGS=fr TRGLANGS=de SRC=fr TRG=de eval
	${MAKE} SRCLANGS=de TRGLANGS=fr SRC=de TRG=fr eval
	${MAKE} SRCLANGS=fi TRGLANGS=nl SRC=fi TRG=nl eval
	${MAKE} SRCLANGS=fr TRGLANGS=fi SRC=fr TRG=fi eval
	${MAKE} SRCLANGS=nl TRGLANGS=de SRC=nl TRG=de eval
	${MAKE} SRCLANGS=de TRGLANGS=nl SRC=de TRG=nl eval
	${MAKE} SRCLANGS=fi TRGLANGS=fr SRC=fi TRG=de eval
	${MAKE} SRCLANGS=fr TRGLANGS=nl SRC=fr TRG=nl eval
	${MAKE} SRCLANGS=nl TRGLANGS=fr SRC=nl TRG=fr eval
	${MAKE} SRCLANGS=sv TRGLANGS=de SRC=sv TRG=de eval



## run things with individual data sets only
%-fiskmo:
	${MAKE} TRAINSET=fiskmo ${@:-fiskmo=}

%-opensubtitles:
	${MAKE} TRAINSET=OpenSubtitles ${@:-opensubtitles=}

%-finlex:
	${MAKE} TRAINSET=Finlex ${@:-finlex=}



## a batch of interesting models ....

## some models with Finnish as source or target
## make sure that we don't use WMT testsets for fi-en/en-fi


iso639 = aa ab ae af ak am an ar as av ay az ba be bg bh bi bm bn bo br bs ca ce ch cn co cr cs cu cv cy da de dv dz ee el en eo es et eu fa ff fi fj fo fr fy ga gd gl gn gr gu gv ha hb he hi ho hr ht hu hy hz ia id ie ig ik io is it iu ja jp jv ka kg ki kj kk kl km kn ko kr ks ku kv kw ky la lb lg li ln lo lt lu lv me mg mh mi mk ml mn mo mr ms mt my na nb nd ne ng nl nn no nr nv ny oc oj om or os pa pi pl po ps pt qu rm rn ro ru rw ry sa sc sd se sg sh si sk sl sm sn so sq sr ss st su sv sw ta tc te tg th ti tk tl tn to tr ts tt tw ty ua ug uk ur uz ve vi vo wa wo xh yi yo za zh zu

all2en:
	for s in ${iso639}; do \
	  if [ "$$s" != "en" ]; then \
	    if [ ! -e ${WORKHOME}/$$s-en/train.submit ]; then \
	      ${MAKE} SRCLANGS=$$s TRGLANGS='en' traindata devdata; \
	      if [ `zcat ${WORKHOME}/$$s-en/train/*.src.${PRE_SRC}.gz | wc -l` -gt 1000000 ]; then \
		echo "$$s-en bigger than 1 million"; \
		${MAKE} SRCLANGS=$$s TRGLANGS='en' HPC_CORES=1 train.submit-multigpu; \
	      elif [ `zcat ${WORKHOME}/$$s-en/train/*.src.${PRE_SRC}.gz | wc -l` -gt 100000 ]; then \
		echo "$$s-en bigger than 100k"; \
		${MAKE} SRCLANGS=$$s TRGLANGS='en' \
			MARIAN_VALID_FREQ=2500 \
			MARIAN_EARLY_STOPPING=5 \
			HPC_CORES=1 train.submit; \
	      else \
		echo "$$s-en too small"; \
	      fi \
	    fi \
	  fi \
	done
	for s in ${iso639}; do \
	  if [ "$$s" != "en" ]; then \
	    if [ ! -e ${WORKHOME}/en-$$s/train.submit ]; then \
	      ${MAKE} TRGLANGS=$$s SRCLANGS='en' traindata devdata; \
	      if [ `zcat ${WORKHOME}/en-$$s/train/*.src.${PRE_SRC}.gz | wc -l` -gt 1000000 ]; then \
		echo "en-$$s bigger than 1 million"; \
		${MAKE} TRGLANGS=$$s SRCLANGS='en' HPC_CORES=1 train.submit-multigpu; \
	      elif [ `zcat ${WORKHOME}/en-$$s/train/*.src.${PRE_SRC}.gz | wc -l` -gt 100000 ]; then \
		echo "en-$$s bigger than 100k"; \
		${MAKE} TRGLANGS=$$s SRCLANGS='en' \
			MARIAN_VALID_FREQ=2500 \
			MARIAN_EARLY_STOPPING=5 \
			HPC_CORES=1 train.submit; \
	      else \
		echo "en-$$s too small"; \
	      fi \
	    fi \
	  fi \
	done

memad:
	for s in en fi sv de fr nl; do \
	  for t in en fi sv de fr nl; do \
	    if [ "$$s" != "$$t" ]; then \
	      ${MAKE} SRCLANGS=$$s TRGLANGS=$$t traindata devdata; \
	      ${MAKE} SRCLANGS=$$s TRGLANGS=$$t HPC_CORES=1 train.submit-multigpu; \
	    fi \
	  done \
	done

memad-missing:
	${MAKE} SRCLANGS=nl TRGLANGS=fi traindata devdata
	${MAKE} SRCLANGS=nl TRGLANGS=fi HPC_CORES=1 train.submit-multigpu
	${MAKE} SRCLANGS=nl TRGLANGS=sv traindata devdata
	${MAKE} SRCLANGS=nl TRGLANGS=sv HPC_CORES=1 train.submit-multigpu


memad-multi:
	for s in "da fo is no nb nn sv" "en fr" "et hu fi" "de nl af fy" "ca es fr ga it la oc pt_br pt"; do \
	      ${MAKE} SRCLANGS="$$s" TRGLANGS="$$s" traindata devdata; \
	      ${MAKE} SRCLANGS="$$s" TRGLANGS="$$s" HPC_CORES=1 train.submit-multigpu; \
	done
	for s in "da fo is no nb nn sv" "en fr" "et hu fi" "de nl af fy" "ca es fr ga it la oc pt_br pt"; do \
	  for t in "da fo is no nb nn sv" "en fr" "et hu fi" "de nl af fy" "ca es fr ga it la oc pt_br pt"; do \
	    if [ "$$s" != "$$t" ]; then \
	      ${MAKE} SRCLANGS="$$s" TRGLANGS="$$t" traindata devdata; \
	      ${MAKE} SRCLANGS="$$s" TRGLANGS="$$t" HPC_CORES=1 train.submit-multigpu; \
	    fi \
	  done \
	done

memad-multi2:
	for s in "en fr" "et hu fi" "de nl af fy" "ca es fr ga it la oc pt_br pt"; do \
	  for t in "da fo is no nb nn sv" "en fr" "et hu fi" "de nl af fy" "ca es fr ga it la oc pt_br pt"; do \
	    if [ "$$s" != "$$t" ]; then \
	      ${MAKE} SRCLANGS="$$s" TRGLANGS="$$t" traindata devdata; \
	      ${MAKE} SRCLANGS="$$s" TRGLANGS="$$t" HPC_CORES=1 train.submit-multigpu; \
	    fi \
	  done \
	done



memad-ethufi:
	${MAKE} SRCLANGS="et hu fi" TRGLANGS="et hu fi" traindata devdata
	${MAKE} SRCLANGS="et hu fi" TRGLANGS="et hu fi" HPC_CORES=1 train.submit-multigpu


memad-fi:
	for l in en sv de fr; do \
	  ${MAKE} SRCLANGS=$$l TRGLANGS=fi traindata devdata; \
	  ${MAKE} SRCLANGS=$$l TRGLANGS=fi HPC_CORES=1 train.submit-multigpu; \
	  ${MAKE} TRGLANGS=$$l SRCLANGS=fi traindata devdata; \
	  ${MAKE} TRGLANGS=$$l SRCLANGS=fi HPC_CORES=1 train.submit-multigpu; \
	done



nordic:
	${MAKE} SRCLANGS="da fo is no nb nn sv" TRGLANGS="fi et hu" traindata
	${MAKE} SRCLANGS="da fo is no nb nn sv" TRGLANGS="fi et hu" HPC_CORES=1 train.submit-multigpu
	${MAKE} TRGLANGS="da fo is no nb nn sv" SRCLANGS="fi et hu" traindata
	${MAKE} TRGLANGS="da fo is no nb nn sv" SRCLANGS="fi et hu" HPC_CORES=1 train.submit-multigpu

romance:
	${MAKE} SRCLANGS="es ca ga oc it la fr ro pt_br pt" TRGLANGS="fi et hu" traindata
	${MAKE} SRCLANGS="es ca ga oc it la fr ro pt_br pt" TRGLANGS="fi et hu" HPC_CORES=1 train.submit-multigpu
	${MAKE} TRGLANGS="es ca ga oc it la fr ro pt_br pt" SRCLANGS="fi et hu" traindata
	${MAKE} TRGLANGS="es ca ga oc it la fr ro pt_br pt" SRCLANGS="fi et hu" HPC_CORES=1 train.submit-multigpu

germanic:
	${MAKE} SRCLANGS="de nl af fy" TRGLANGS="fi et hu" traindata
	${MAKE} SRCLANGS="de nl af fy" TRGLANGS="fi et hu" HPC_CORES=1 train.submit-multigpu
	${MAKE} TRGLANGS="de nl af fy" SRCLANGS="fi et hu" traindata
	${MAKE} TRGLANGS="de nl af fy" SRCLANGS="fi et hu" HPC_CORES=1 train.submit-multigpu


germanic-romance:
	${MAKE} SRCLANGS="fr ca es gl it la oc pt_br pt ro" \
		TRGLANGS="en de nl fy af da fo is no nb nn sv" traindata
	${MAKE} HPC_CORES=1 SRCLANGS="fr ca es gl it la oc pt_br pt ro" \
		TRGLANGS="en de nl fy af da fo is no nb nn sv" train.submit-multigpu
	${MAKE} TRGLANGS="fr ca es gl it la oc pt_br pt ro" \
		SRCLANGS="en de nl fy af da fo is no nb nn sv" traindata devdata
	${MAKE} HPC_CORES=1 TRGLANGS="fr ca es gl it la oc pt_br pt ro" \
		SRCLANGS="en de nl fy af da fo is no nb nn sv" train.submit-multigpu





##==========================
## various data sets
##==========================

.PHONY: data
data:		${TRAIN_SRC}.${PRE_SRC}.gz ${TRAIN_TRG}.${PRE_TRG}.gz \
		${DEV_SRC}.${PRE_SRC} ${DEV_TRG}.${PRE_TRG} \
		${TUNE_SRC}.${PRE_SRC} ${TUNE_TRG}.${PRE_TRG} \
		${TEST_SRC}.${PRE_SRC} ${TEST_TRG}

traindata: 	${TRAIN_SRC}.${PRE_SRC}.gz ${TRAIN_TRG}.${PRE_TRG}.gz
tunedata: 	${TUNE_SRC}.${PRE_SRC} ${TUNE_TRG}.${PRE_TRG}
devdata:	${DEV_SRC}.${PRE_SRC} ${DEV_TRG}.${PRE_TRG}
testdata:	${TEST_SRC}.${PRE_SRC} ${TEST_TRG}

devdata-raw:	${DEV_SRC} ${DEV_TRG}


MULTEVALHOME = ${APPLHOME}/multeval
MOSESSCRIPTS = ${MOSESHOME}/scripts
TOKENIZER    = ${MOSESSCRIPTS}/tokenizer
SNMTPATH     = ${APPLHOME}/subword-nmt/subword_nmt


include Makefile.data


## parameters for running Marian NMT

MARIAN_GPUS           = 0
MARIAN_EXTRA          = 
MARIAN_VALID_FREQ     = 10000
MARIAN_SAVE_FREQ      = ${MARIAN_VALID_FREQ}
MARIAN_DISP_FREQ      = ${MARIAN_VALID_FREQ}
MARIAN_EARLY_STOPPING = 10

MARIAN_DECODER_GPU    = -b 12 -n1 -d ${MARIAN_GPUS} --mini-batch 8 --maxi-batch 32 --maxi-batch-sort src
MARIAN_DECODER_CPU    = -b 12 -n1 --cpu-threads ${HPC_CORES} --mini-batch 8 --maxi-batch 32 --maxi-batch-sort src
MARIAN_DECODER_FLAGS = ${MARIAN_DECODER_GPU}

ifneq ("$(wildcard ${TRAIN_WEIGHTS})","")
	MARIAN_TRAIN_WEIGHTS = --data-weighting ${TRAIN_WEIGHTS}
endif



ENSEMBLE = ${wildcard ${WORKDIR}/${MODEL}.${MODELTYPE}.model*.npz.best-perplexity.npz}

## work with fine-tuned data
.PHONY: finetune
finetune:
	if [ ! -e ${WORKDIR}/${MODEL}-tuned.${MODELTYPE}.model${NR}.npz ]; then \
	  if [ -e ${WORKDIR}/${MODEL}.${MODELTYPE}.model${NR}.npz.best-perplexity.npz ]; then \
	    cp ${WORKDIR}/${MODEL}.${MODELTYPE}.model${NR}.npz.best-perplexity.npz \
		${WORKDIR}/${MODEL}-tuned.${MODELTYPE}.model${NR}.npz; \
	    if [ -e ${WORKDIR}/${MODEL}.vocab.yml ]; then \
	      if [ ! -e ${WORKDIR}/${MODEL}-tuned.vocab.yml ]; then \
	        cp ${WORKDIR}/${MODEL}.vocab.yml ${WORKDIR}/${MODEL}-tuned.vocab.yml; \
	      fi; \
	    fi; \
	    if [ -e ${WORKDIR}/${MODEL}.${SRC}.yml ]; then \
	      if [ ! -e ${WORKDIR}/${MODEL}-tuned.${SRC}.yml ]; then \
	        cp ${WORKDIR}/${MODEL}.${SRC}.yml ${WORKDIR}/${MODEL}-tuned.${SRC}.yml; \
	      fi; \
	    fi; \
	    if [ -e ${WORKDIR}/${MODEL}.${TRG}.yml ]; then \
	      if [ ! -e ${WORKDIR}/${MODEL}-tuned.${TRG}.yml ]; then \
	        cp ${WORKDIR}/${MODEL}.${TRG}.yml ${WORKDIR}/${MODEL}-tuned.${TRG}.yml; \
	      fi; \
	    fi; \
	    cp ${WORKDIR}/${MODEL}.${MODELTYPE}.model${NR}.npz.yml \
		${WORKDIR}/${MODEL}-tuned.${MODELTYPE}.model${NR}.npz.yml; \
	    sleep 1; \
	  fi \
	fi
	${MAKE} MODEL=${MODEL}-tuned DATASET=${TUNESET} \
		MARIAN_EXTRA="${MARIAN_EXTRA} --no-restore-corpus" ${MODE}; \



## right-to-left model

%-RL:
	${MAKE} MODEL=${MODEL}-RL \
		MARIAN_EXTRA="${MARIAN_EXTRA} --right-left" \
	${@:-RL=}


## run a multigpu job (2 or 4 GPUs)

%-multigpu %-0123:
	${MAKE} NR_GPUS=4 MARIAN_GPUS='0 1 2 3' $(subst -gpu0123,,${@:-multigpu=})

%-twogpu %-gpu01:
	${MAKE} NR_GPUS=2 MARIAN_GPUS='0 1' $(subst -gpu01,,${@:-twogpu=})

%-gpu23:
	${MAKE} NR_GPUS=2 MARIAN_GPUS='2 3' ${@:-gpu23=}



#------------------------------------------------------------------------
# train, translate and evaluate
#------------------------------------------------------------------------


## other model types
train: ${WORKDIR}/${MODEL}.${MODELTYPE}.model${NR}.done
translate: ${WORKDIR}/${TESTSET}.${MODEL}${NR}.${MODELTYPE}.${SRC}.${TRG}
eval: ${WORKDIR}/${TESTSET}.${MODEL}${NR}.${MODELTYPE}.${SRC}.${TRG}.eval
compare: ${WORKDIR}/${TESTSET}.${MODEL}${NR}.${MODELTYPE}.${SRC}.${TRG}.compare

## ensemble of models (assumes to find them in subdirs of the WORKDIR)
translate-ensemble: ${WORKDIR}/${TESTSET}.${MODEL}${NR}.${MODELTYPE}.ensemble.${SRC}.${TRG}
eval-ensemble: ${WORKDIR}/${TESTSET}.${MODEL}${NR}.${MODELTYPE}.ensemble.${SRC}.${TRG}.eval



## run on CPUs (translate-cpu, eval-cpu, translate-ensemble-cpu, ...)
%-cpu:
	${MAKE} MARIAN=${MARIANCPU} \
		LOADMODS='${LOADCPU}' \
		MARIAN_DECODER_FLAGS="${MARIAN_DECODER_CPU}" \
	${@:-cpu=}


## resume training on an existing model
resume:
	if [ -e ${WORKDIR}/${MODEL}.${MODELTYPE}.model${NR}.npz.best-perplexity.npz ]; then \
	  cp ${WORKDIR}/${MODEL}.${MODELTYPE}.model${NR}.npz.best-perplexity.npz \
	     ${WORKDIR}/${MODEL}.${MODELTYPE}.model${NR}.npz; \
	fi
	sleep 1
	rm -f ${WORKDIR}/${MODEL}.${MODELTYPE}.model${NR}.done
	${MAKE} train




### training a model with Marian NMT
##
## NR allows to train several models for proper ensembling
## (with shared vocab)
##
## DANGER: if several models are started at the same time
## then there is some racing issue with creating the vocab!

ifdef NR
  SEED=${NR}${NR}${NR}${NR}
else
  SEED=1234
endif


## reduce training data size if necessary
ifdef TRAINSIZE
${TRAIN_SRC}.${PRE_SRC}${TRAINSIZE}.gz: ${TRAIN_SRC}.${PRE_SRC}.gz
	zcat $< | head -${TRAINSIZE} | gzip -c > $@

${TRAIN_TRG}.${PRE_TRG}${TRAINSIZE}.gz: ${TRAIN_TRG}.${PRE_TRG}.gz
	zcat $< | head -${TRAINSIZE} | gzip -c > $@
endif


## make vocabulary
## - no new vocabulary is created if the file already exists!
## - need to delete the file if you want to create a new one!

vocab: ${MODEL_VOCAB}

${MODEL_VOCAB}:	${TRAIN_SRC}.${PRE_SRC}${TRAINSIZE}.gz \
		${TRAIN_TRG}.${PRE_TRG}${TRAINSIZE}.gz
ifeq ($(wildcard ${MODEL_VOCAB}),)
	mkdir -p ${dir $@}
	${LOADMODS} && zcat $^ | ${MARIAN}/marian-vocab --max-size ${VOCABSIZE} > $@
else
	@echo "$@ already exists!"
	@echo "WARNING! No new vocabulary is created even though the data has changed!"
	@echo "WARNING! Delete the file if you want to start from scratch!"
	touch $@
endif


## train transformer model
${WORKDIR}/${MODEL}.transformer.model${NR}.done: \
		${TRAIN_SRC}.${PRE_SRC}${TRAINSIZE}.gz \
		${TRAIN_TRG}.${PRE_TRG}${TRAINSIZE}.gz \
		${DEV_SRC}.${PRE_SRC} ${DEV_TRG}.${PRE_TRG} \
		${MODEL_VOCAB}
	mkdir -p ${dir $@}
	${LOADMODS} && ${MARIAN}/marian ${MARIAN_EXTRA} \
        --model $(@:.done=.npz) \
	--type transformer \
        --train-sets ${word 1,$^} ${word 2,$^} ${MARIAN_TRAIN_WEIGHTS} \
        --max-length 500 \
        --vocabs ${word 5,$^} ${word 5,$^} \
        --mini-batch-fit \
	-w ${MARIAN_WORKSPACE} \
	--maxi-batch 500 \
        --early-stopping ${MARIAN_EARLY_STOPPING} \
        --valid-freq ${MARIAN_VALID_FREQ} \
	--save-freq ${MARIAN_SAVE_FREQ} \
	--disp-freq ${MARIAN_DISP_FREQ} \
        --valid-sets ${word 3,$^} ${word 4,$^} \
        --valid-metrics perplexity \
        --valid-mini-batch 16 \
        --beam-size 12 --normalize 1 \
        --log $(@:.model${NR}.done=.train${NR}.log) --valid-log $(@:.model${NR}.done=.valid${NR}.log) \
        --enc-depth 6 --dec-depth 6 \
        --transformer-heads 8 \
        --transformer-postprocess-emb d \
        --transformer-postprocess dan \
        --transformer-dropout 0.1 --label-smoothing 0.1 \
        --learn-rate 0.0003 --lr-warmup 16000 --lr-decay-inv-sqrt 16000 --lr-report \
        --optimizer-params 0.9 0.98 1e-09 --clip-norm 5 \
        --tied-embeddings-all \
	--overwrite --keep-best \
	--devices ${MARIAN_GPUS} \
        --sync-sgd --seed ${SEED} \
	--sqlite \
	--tempdir ${TMPDIR} \
        --exponential-smoothing
	touch $@






##-------------------
## ensemble of several models
##-------------------

${WORKDIR}/${TESTSET}.${MODEL}${NR}.${MODELTYPE}.ensemble.${SRC}.${TRG}: ${TEST_SRC}.${PRE_SRC} ${ENSEMBLE}
	mkdir -p ${dir $@}
	${LOADMODS} && ${MARIAN}/marian-decoder -i ${word 1,$^} \
		--models ${ENSEMBLE} \
		--vocabs ${WORKDIR}/${MODEL}.vocab.yml \
			${WORKDIR}/${MODEL}.vocab.yml \
			${WORKDIR}/${MODEL}.vocab.yml \
		${MARIAN_DECODER_FLAGS} \
	| sed 's/\@\@ //g' > $@


##-------------------
## translate
##-------------------

${WORKDIR}/${TESTSET}.${MODEL}${NR}.${MODELTYPE}.${SRC}.${TRG}: ${TEST_SRC}.${PRE_SRC} \
		${WORKDIR}/${MODEL}.${MODELTYPE}.model${NR}.npz
	mkdir -p ${dir $@}
	grep . $< > $@.input
	${LOADMODS} && ${MARIAN}/marian-decoder -i $@.input \
		-c ${word 2,$^}.best-perplexity.npz.decoder.yml \
		-d ${MARIAN_GPUS} \
		${MARIAN_DECODER_FLAGS} \
	| sed 's/\@\@ //g' > $@
	rm -f $@.input

%.eval: % ${TEST_TRG}
	grep . ${TEST_TRG} > $@.ref
	grep . $< | sed 's/ \@\-\@ /-/g' > $@.sys
	cd ${MULTEVALHOME} && ./multeval.sh eval \
		--refs $@.ref \
		--hyps-baseline $@.sys \
		--meteor.language ${TRG} > $@
	rm -f $@.ref $@.sys

%.compare: %.eval
	paste -d "\n" ${TEST_SRC} ${TEST_TRG} ${<:.eval=} |\
	sed 's/ \@\-\@ /-/g' | \
	sed 	-e "s/&apos;/'/g" \
		-e 's/&quot;/"/g' \
		-e 's/&lt;/</g' \
		-e 's/&gt;/>/g' \
		-e 's/&amp;/&/g' |\
	sed 'n;n;G;' > $@



##---------------------------------------------
## submit jobs
##---------------------------------------------


## submit job to gpu queue

%.submit:
	mkdir -p ${WORKDIR}
	echo '#!/bin/bash -l' > $@
	echo '#SBATCH -J "${DATASET}-${@:.submit=}"' >>$@
	echo '#SBATCH -o ${DATASET}-${@:.submit=}.out.%j' >> $@
	echo '#SBATCH -e ${DATASET}-${@:.submit=}.err.%j' >> $@
	echo '#SBATCH --mem=${HPC_MEM}' >> $@
ifdef EMAIL
	echo '#SBATCH --mail-type=END' >> $@
	echo '#SBATCH --mail-user=${EMAIL}' >> $@
endif
	echo '#SBATCH -n 1' >> $@
	echo '#SBATCH -N 1' >> $@
	echo '#SBATCH -p gpu' >> $@
ifeq (${shell hostname --domain},bullx)
	echo '#SBATCH --account=${CSCPROJECT}' >> $@
	echo '#SBATCH --gres=gpu:${GPU}:${NR_GPUS},nvme:${HPC_DISK}' >> $@
else
	echo '#SBATCH --gres=gpu:${GPU}:${NR_GPUS}' >> $@
endif
	echo '#SBATCH -t ${WALLTIME}:00:00' >> $@
	echo 'module use -a /proj/nlpl/modules' >> $@
	for m in ${GPU_MODULES}; do \
	  echo "module load $$m" >> $@; \
	done
	echo 'module list' >> $@
	echo 'cd $${SLURM_SUBMIT_DIR:-.}' >> $@
	echo 'pwd' >> $@
	echo 'echo "Starting at `date`"' >> $@
	echo 'srun ${MAKE} ${MAKEARGS} ${@:.submit=}' >> $@
	echo 'echo "Finishing at `date`"' >> $@
	sbatch $@
	mkdir -p ${WORKDIR}
	mv $@ ${WORKDIR}/$@

# 	echo 'srun ${MAKE} NR=${NR} MODELTYPE=${MODELTYPE} DATASET=${DATASET} SRC=${SRC} TRG=${TRG} PRE_SRC=${PRE_SRC} PRE_TRG=${PRE_TRG} ${MAKEARGS} ${@:.submit=}' >> $@


## submit job to cpu queue

%.submitcpu:
	mkdir -p ${WORKDIR}
	echo '#!/bin/bash -l' > $@
	echo '#SBATCH -J "${@:.submitcpu=}"' >>$@
	echo '#SBATCH -o ${@:.submitcpu=}.out.%j' >> $@
	echo '#SBATCH -e ${@:.submitcpu=}.err.%j' >> $@
	echo '#SBATCH --mem=${HPC_MEM}' >> $@
ifdef EMAIL
	echo '#SBATCH --mail-type=END' >> $@
	echo '#SBATCH --mail-user=${EMAIL}' >> $@
endif
ifeq (${shell hostname --domain},bullx)
	echo '#SBATCH --account=${CSCPROJECT}' >> $@
	echo '#SBATCH --gres=nvme:${HPC_DISK}' >> $@
endif
	echo '#SBATCH -n ${HPC_CORES}' >> $@
	echo '#SBATCH -N ${HPC_NODES}' >> $@
	echo '#SBATCH -p ${HPC_QUEUE}' >> $@
	echo '#SBATCH -t ${WALLTIME}:00:00' >> $@
	echo '${HPC_EXTRA}' >> $@
	echo 'module use -a /proj/nlpl/modules' >> $@
	for m in ${CPU_MODULES}; do \
	  echo "module load $$m" >> $@; \
	done
	echo 'module list' >> $@
	echo 'cd $${SLURM_SUBMIT_DIR:-.}' >> $@
	echo 'pwd' >> $@
	echo 'echo "Starting at `date`"' >> $@
	echo '${MAKE} -j ${HPC_CORES} ${MAKEARGS} ${@:.submitcpu=}' >> $@
	echo 'echo "Finishing at `date`"' >> $@
	sbatch $@
	mkdir -p ${WORKDIR}
	mv $@ ${WORKDIR}/$@


#	echo '${MAKE} -j ${HPC_CORES} DATASET=${DATASET} SRC=${SRC} TRG=${TRG} PRE_SRC=${PRE_SRC} PRE_TRG=${PRE_TRG} ${MAKEARGS} ${@:.submitcpu=}' >> $@
