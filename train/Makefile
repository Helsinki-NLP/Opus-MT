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
  SRC = ${lastword ${SRCLANGS}}
endif
ifndef TRG
  TRG = ${lastword ${TRGLANGS}}
endif

# sorted languages and langpair used to match resources in OPUS
SORTLANGS = $(sort ${SRC} ${TRG})
LANGPAIR  = ${firstword ${SORTLANGS}}-${lastword ${SORTLANGS}}

include Makefile.def

## all of OPUS
OPUSCORPORA  = ${patsubst %/latest/moses/${LANGPAIR}.txt.zip,%,\
		${patsubst ${OPUSHOME}/%,%,\
		${shell ls ${OPUSHOME}/*/latest/moses/${LANGPAIR}.txt.zip}}}


## train/dev/test data

TRAINSET = $(filter-out ${DEVSET} ${TESTSET},${OPUSCORPORA})
DEVSET   = Tatoeba
TESTSET  = ${DEVSET}
TUNESET  = OpenSubtitles


## size of dev data, test data and BPE merge operations

DEVSIZE    = 5000
TESTSIZE   = 5000
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
WORKDIR = ${WORKHOME}/${subst ${SPACE},+,$(SRCLANGS)}-${subst ${SPACE},+,$(TRGLANGS)}
DATADIR = ${WORKHOME}/data


## data sets
TRAIN_SRC = ${WORKDIR}/train/${DATASET}.src
TRAIN_TRG = ${WORKDIR}/train/${DATASET}.trg

TUNE_SRC  = ${WORKDIR}/tune/${TUNESET}.src
TUNE_TRG  = ${WORKDIR}/tune/${TUNESET}.trg

DEV_SRC   = ${WORKDIR}/val/${DEVSET}.src
DEV_TRG   = ${WORKDIR}/val/${DEVSET}.trg

TEST_SRC  = ${WORKDIR}/test/${TESTSET}.src
TEST_TRG  = ${WORKDIR}/test/${TESTSET}.trg



## fiskmo benchmark for sv-fi

FISKMO_SV = ${PWD}/fiskmo_testset.sv
FISKMO_FI = ${PWD}/fiskmo_testset.fi


## benchmark with the fiskmo testset and the current model

evalfiskmo:
	${MAKE} TESTSET=fiskmo_testset eval

all-evalfiskmo: 
	${MAKE} SRCLANGS=sv TRGLANGS=fi SRC=sv TRG=fi evalfiskmo
	${MAKE} TRGLANGS=sv SRCLANGS=fi SRC=fi TRG=sv evalfiskmo
	${MAKE} SRCLANGS="da no nb nn sv" TRGLANGS=fi SRC=sv TRG=fi evalfiskmo
	${MAKE} TRGLANGS="da no nb nn sv" SRCLANGS=fi SRC=fi TRG=sv evalfiskmo
	${MAKE} SRCLANGS="de da en no nb nn nl sv" TRGLANGS=fi SRC=sv TRG=fi evalfiskmo
	${MAKE} TRGLANGS="de da en no nb nn nl sv" SRCLANGS=fi SRC=fi TRG=sv evalfiskmo
	${MAKE} SRCLANGS="da no nb nn sv" TRGLANGS="fi et" SRC=sv TRG=fi evalfiskmo
	${MAKE} TRGLANGS="da no nb nn sv" SRCLANGS="fi et" SRC=fi TRG=sv evalfiskmo
	${MAKE} SRCLANGS="da fo is no nb nn sv" TRGLANGS="fi et hu" SRC=sv TRG=fi evalfiskmo
	${MAKE} TRGLANGS="da fo is no nb nn sv" SRCLANGS="fi et hu" SRC=fi TRG=sv evalfiskmo
	${MAKE} SRCLANGS="da no nb nn sv" TRGLANGS="fi et" SRC=sv TRG=fi evalfiskmo
	${MAKE} TRGLANGS="da no nb nn sv" SRCLANGS="fi et" SRC=fi TRG=sv evalfiskmo


#	${MAKE} SRCLANGS=sv TRGLANGS=fi SRC=sv TRG=fi TRAINSET=Finlex evalfiskmo
#	${MAKE} TRGLANGS=sv SRCLANGS=fi SRC=fi TRG=sv TRAINSET=Finlex evalfiskmo
#	${MAKE} SRCLANGS=sv TRGLANGS=fi SRC=sv TRG=fi TRAINSET=fiskmo evalfiskmo
#	${MAKE} TRGLANGS=sv SRCLANGS=fi SRC=fi TRG=sv TRAINSET=fiskmo evalfiskmo
#	${MAKE} SRCLANGS=sv TRGLANGS=fi SRC=sv TRG=fi TRAINSET=fiskmo TRAINSIZE=100000 evalfiskmo
#	${MAKE} SRCLANGS=sv TRGLANGS=fi SRC=sv TRG=fi TRAINSET=fiskmo TRAINSIZE=500000 evalfiskmo
#	${MAKE} SRCLANGS=sv TRGLANGS=fi SRC=sv TRG=fi TRAINSET=fiskmo TRAINSIZE=1000000 evalfiskmo


nowmt:
	${MAKE} SRCLANGS=en TRGLANGS=fi traindata-nowmt
	${MAKE} HPC_CORES=1 SRCLANGS=en TRGLANGS=fi train-nowmt.submit
	${MAKE} SRCLANGS=fi TRGLANGS=en traindata-nowmt
	${MAKE} HPC_CORES=1 SRCLANGS=fi TRGLANGS=en train-nowmt.submit
	${MAKE} SRCLANGS="de fr sv en" TRGLANGS="et hu fi" traindata-nowmt
	${MAKE} HPC_CORES=1 SRCLANGS="de fr sv en" TRGLANGS="et hu fi" train-nowmt.submit
	${MAKE} TRGLANGS="de fr sv en" SRCLANGS="et hu fi" traindata-nowmt
	${MAKE} HPC_CORES=1 TRGLANGS="de fr sv en" SRCLANGS="et hu fi" train-nowmt.submit

nowmt-eval:
	${MAKE} SRCLANGS=en TRGLANGS=fi SRC=en TRG=fi TESTSET=newstest2017.en-fi DATASET=opus-wmt eval
	${MAKE} SRCLANGS=fi TRGLANGS=en SRC=fi TRG=en TESTSET=newstest2017.en-fi DATASET=opus-wmt eval
	${MAKE} SRCLANGS=en TRGLANGS=fi SRC=en TRG=fi TESTSET=newstest2018.en-fi DATASET=opus-wmt eval
	${MAKE} SRCLANGS=fi TRGLANGS=en SRC=fi TRG=en TESTSET=newstest2018.en-fi DATASET=opus-wmt eval




## models that exclude WMT-News data
## --> make it possible to compare scores
%-nowmt:
	${MAKE} TESTSET=WMT-News DATASET=opus-wmt ${@:-nowmt=}

## run things with individual data sets only
%-fiskmo:
	${MAKE} TRAINSET=fiskmo ${@:-fiskmo=}

%-opensubtitles:
	${MAKE} TRAINSET=OpenSubtitles ${@:-opensubtitles=}

%-finlex:
	${MAKE} TRAINSET=Finlex ${@:-finlex=}



%-fizh:
	${MAKE} DEVSET=wikimedia TESTSET=wikimedia \
		SRCLANGS="fi" TRGLANGS="zh_CN zh_TW zh_HK zh_cn zh_tw zh" ${@:-fizh=}

%-zhfi:
	${MAKE} DEVSET=wikimedia TESTSET=wikimedia \
		TRGLANGS="fi" SRCLANGS="zh_CN zh_TW zh_HK zh_cn zh_tw zh" ${@:-zhfi=}


nordic1:
	${MAKE} TRGLANGS="da fo is no nb nn sv" SRCLANGS="fi et hu" traindata devdata
	${MAKE} HPC_CORES=1 TRGLANGS="da fo is no nb nn sv" SRCLANGS="fi et hu" train.submit
	${MAKE} SRCLANGS="da fo is no nb nn sv" TRGLANGS="fi et hu" traindata devdata
	${MAKE} HPC_CORES=1 SRCLANGS="da fo is no nb nn sv" TRGLANGS="fi et hu" train.submit

european1:
	${MAKE} SRCLANGS="fr ca es gl it la pt ro" TRGLANGS="en de nl fy af da fo is no nb nn sv" traindata devdata
	${MAKE} HPC_CORES=1 SRCLANGS="fr ca es gl it la pt ro" TRGLANGS="en de nl fy af da fo is no nb nn sv" train.submit
	${MAKE} TRGLANGS="fr ca es gl it la pt ro" SRCLANGS="en de nl fy af da fo is no nb nn sv" traindata devdata
	${MAKE} HPC_CORES=1 TRGLANGS="fr ca es gl it la pt ro" SRCLANGS="en de nl fy af da fo is no nb nn sv" train.submit


## a batch of interesting models ....

prepare-all:
	${MAKE} SRCLANGS="da no nb nn sv" TRGLANGS=fi traindata devdata
	${MAKE} TRGLANGS="da no nb nn sv" SRCLANGS=fi traindata devdata
	${MAKE} SRCLANGS=sv TRGLANGS=fi traindata devdata
	${MAKE} TRGLANGS=sv SRCLANGS=fi traindata devdata
	${MAKE} SRCLANGS=en TRGLANGS=fi traindata devdata
	${MAKE} TRGLANGS=en SRCLANGS=fi traindata devdata
	${MAKE} SRCLANGS=de TRGLANGS=fi traindata devdata
	${MAKE} TRGLANGS=de SRCLANGS=fi traindata devdata
	${MAKE} SRCLANGS=fr TRGLANGS=fi traindata devdata
	${MAKE} TRGLANGS=fr SRCLANGS=fi traindata devdata
	${MAKE} SRCLANGS="de da en no nb nn nl sv" TRGLANGS=fi traindata devdata
	${MAKE} TRGLANGS="de da en no nb nn nl sv" SRCLANGS=fi traindata devdata
	${MAKE} SRCLANGS="es it fr pt" TRGLANGS=fi traindata devdata
	${MAKE} TRGLANGS="es it fr pt" SRCLANGS=fi traindata devdata
	${MAKE} SRCLANGS="da no nb nn sv" TRGLANGS="fi et" traindata devdata
	${MAKE} TRGLANGS="da no nb nn sv" SRCLANGS="fi et" traindata devdata

train-all:
	${MAKE} SRCLANGS="da no nb nn sv" TRGLANGS=fi train.submit
	${MAKE} TRGLANGS="da no nb nn sv" SRCLANGS=fi train.submit
	${MAKE} SRCLANGS=sv TRGLANGS=fi train.submit
	${MAKE} TRGLANGS=sv SRCLANGS=fi train.submit
	${MAKE} SRCLANGS=en TRGLANGS=fi train.submit
	${MAKE} TRGLANGS=en SRCLANGS=fi train.submit
	${MAKE} SRCLANGS=de TRGLANGS=fi train.submit
	${MAKE} TRGLANGS=de SRCLANGS=fi train.submit
	${MAKE} SRCLANGS=fr TRGLANGS=fi train.submit
	${MAKE} TRGLANGS=fr SRCLANGS=fi train.submit
	${MAKE} SRCLANGS="de da en no nb nn nl sv" TRGLANGS=fi train.submit
	${MAKE} TRGLANGS="de da en no nb nn nl sv" SRCLANGS=fi train.submit
	${MAKE} SRCLANGS="es it fr pt" TRGLANGS=fi train.submit
	${MAKE} TRGLANGS="es it fr pt" SRCLANGS=fi train.submit
	${MAKE} SRCLANGS="da no nb nn sv" TRGLANGS="fi et" train.submit
	${MAKE} TRGLANGS="da no nb nn sv" SRCLANGS="fi et" train.submit


ALLLANGPAIRS = ${notdir ${shell ls work | grep -- '-'}}

eval-all:
	for l in ${ALLLANGPAIRS}; do \
	  if  [ `ls ${WORKHOME}/$$l/${DATASET}${TRAINSIZE}.${PRE_SRC}-${PRE_TRG}.*.npz | wc -l` -gt 0 ]; then \
	    ${MAKE} SRCLANGS="`echo $$l | cut -f1 -d'-' | sed 's/\\+/ /g'`" \
		    TRGLANGS="`echo $$l | cut -f2 -d'-' | sed 's/\\+/ /g'`" eval; \
	  fi \
	done


#	${MAKE} SRCLANGS="da no nb nn sv" TRGLANGS=fi eval
#	${MAKE} TRGLANGS="da no nb nn sv" SRCLANGS=fi eval
#	${MAKE} SRCLANGS=sv TRGLANGS=fi eval
#	${MAKE} TRGLANGS=sv SRCLANGS=fi eval
#	${MAKE} SRCLANGS=en TRGLANGS=fi eval
#	${MAKE} TRGLANGS=en SRCLANGS=fi eval
#	${MAKE} SRCLANGS=de TRGLANGS=fi eval
#	${MAKE} TRGLANGS=de SRCLANGS=fi eval
#	${MAKE} SRCLANGS=fr TRGLANGS=fi eval
#	${MAKE} TRGLANGS=fr SRCLANGS=fi eval
#	${MAKE} SRCLANGS="de da en no nb nn nl sv" TRGLANGS=fi eval
#	${MAKE} TRGLANGS="de da en no nb nn nl sv" SRCLANGS=fi eval
#	${MAKE} SRCLANGS="es it fr pt" TRGLANGS=fi eval
#	${MAKE} TRGLANGS="es it fr pt" SRCLANGS=fi eval
#	${MAKE} SRCLANGS="da no nb nn sv" TRGLANGS="fi et" eval
#	${MAKE} TRGLANGS="da no nb nn sv" SRCLANGS="fi et" eval



##==========================
## various data set variants
##==========================

.PHONY: data
data:		${TRAIN_SRC}.${PRE_SRC} ${TRAIN_TRG}.${PRE_TRG} \
		${DEV_SRC}.${PRE_SRC} ${DEV_TRG}.${PRE_TRG} \
		${TUNE_SRC}.${PRE_SRC} ${TUNE_TRG}.${PRE_TRG} \
		${TEST_SRC}.${PRE_SRC} ${TEST_TRG}

traindata: 	${TRAIN_SRC}.${PRE_SRC} ${TRAIN_TRG}.${PRE_TRG}
tunedata: 	${TUNE_SRC}.${PRE_SRC} ${TUNE_TRG}.${PRE_TRG}
devdata:	${DEV_SRC}.${PRE_SRC} ${DEV_TRG}.${PRE_TRG}
testdata:	${TEST_SRC}.${PRE_SRC} ${TEST_TRG}

MULTEVALHOME = ${APPLHOME}/multeval
MOSESSCRIPTS = ${MOSESHOME}/scripts
TOKENIZER    = ${MOSESSCRIPTS}/tokenizer
SNMTPATH     = ${APPLHOME}/subword-nmt/subword_nmt


include Makefile.data


## parameters for running Marian NMT

MARIAN_GPUS          = 0
MARIAN_EXTRA         = 
# MARIAN_VALID_FREQ    = 2500
MARIAN_VALID_FREQ    = 10000
MARIAN_SAVE_FREQ     = ${MARIAN_VALID_FREQ}
MARIAN_DISP_FREQ     = ${MARIAN_VALID_FREQ}
MARIAN_DECODER_GPU   = -b 12 -n1 -d ${MARIAN_GPUS} --mini-batch 8 --maxi-batch 32 --maxi-batch-sort src
MARIAN_DECODER_CPU   = -b 12 -n1 --cpu-threads ${HPC_CORES} --mini-batch 8 --maxi-batch 32 --maxi-batch-sort src
MARIAN_DECODER_FLAGS = ${MARIAN_DECODER_GPU}

ifneq ("$(wildcard ${TRAIN_WEIGHTS})","")
	MARIAN_TRAIN_WEIGHTS = --data-weighting ${TRAIN_WEIGHTS}
endif



ENSEMBLE = ${wildcard ${WORKDIR}/${MODEL}.${MODELTYPE}.model*.npz.best-cross-entropy.npz}

## work with fine-tuned data
.PHONY: finetune
finetune:
	if [ ! -e ${WORKDIR}/${MODEL}-tuned.${MODELTYPE}.model${NR}.npz ]; then \
	  if [ -e ${WORKDIR}/${MODEL}.${MODELTYPE}.model${NR}.npz.best-cross-entropy.npz ]; then \
	    cp ${WORKDIR}/${MODEL}.${MODELTYPE}.model${NR}.npz.best-cross-entropy.npz \
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
	if [ -e ${WORKDIR}/${MODEL}.${MODELTYPE}.model${NR}.npz.best-cross-entropy.npz ]; then \
	  cp ${WORKDIR}/${MODEL}.${MODELTYPE}.model${NR}.npz.best-cross-entropy.npz \
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
${TRAIN_SRC}.${PRE_SRC}${TRAINSIZE}: ${TRAIN_SRC}.${PRE_SRC}
	head -${TRAINSIZE} $< > $@

${TRAIN_TRG}.${PRE_TRG}${TRAINSIZE}: ${TRAIN_TRG}.${PRE_TRG}
	head -${TRAINSIZE} $< > $@
endif


## make vocabulary
vocab: ${WORKDIR}/${MODEL}.vocab.yml

${WORKDIR}/${MODEL}.vocab.yml: ${TRAIN_SRC}.${PRE_SRC}${TRAINSIZE} ${TRAIN_TRG}.${PRE_TRG}${TRAINSIZE}
	mkdir -p ${dir $@}
	${LOADMODS} && cat $^ | ${MARIAN}/marian-vocab --max-size ${VOCABSIZE} > $@


## train transformer model
${WORKDIR}/${MODEL}.transformer.model${NR}.done: \
		${TRAIN_SRC}.${PRE_SRC}${TRAINSIZE} ${TRAIN_TRG}.${PRE_TRG}${TRAINSIZE} \
		${DEV_SRC}.${PRE_SRC} ${DEV_TRG}.${PRE_TRG} \
		${WORKDIR}/${MODEL}.vocab.yml
	mkdir -p ${dir $@}
	${LOADMODS} && ${MARIAN}/marian ${MARIAN_EXTRA} \
        --model $(@:.done=.npz) \
	--type transformer \
        --train-sets ${word 1,$^} ${word 2,$^} ${MARIAN_TRAIN_WEIGHTS} \
        --max-length 500 \
        --vocabs ${word 5,$^} ${word 5,$^} \
        --mini-batch-fit -w 13000 --maxi-batch 500 \
        --early-stopping 20 \
        --valid-freq ${MARIAN_VALID_FREQ} \
	--save-freq ${MARIAN_SAVE_FREQ} \
	--disp-freq ${MARIAN_DISP_FREQ} \
        --valid-sets ${word 3,$^} ${word 4,$^} \
        --valid-metrics cross-entropy ce-mean-words perplexity \
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
		-c ${word 2,$^}.best-cross-entropy.npz.decoder.yml \
		-d ${MARIAN_GPUS} \
		${MARIAN_DECODER_FLAGS} \
	| sed 's/\@\@ //g' > $@
	rm -f $@.input

%.eval: % ${TEST_TRG}
	grep . ${TEST_TRG} > $@.ref
	cd ${MULTEVALHOME} && ./multeval.sh eval \
		--refs $@.ref \
		--hyps-baseline $< \
		--meteor.language ${TRG} > $@
	rm -f $@.ref



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
ifeq (${shell hostname --domain},bullx)
	echo '#SBATCH --account=project_2001569' >> $@
endif
	echo '#SBATCH -p gpu' >> $@
	echo '#SBATCH --gres=gpu:${GPU}:${NR_GPUS}' >> $@
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
	echo '#SBATCH --account=project_2001569' >> $@
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
	mv $@ ${WORKDIR}/$@


#	echo '${MAKE} -j ${HPC_CORES} DATASET=${DATASET} SRC=${SRC} TRG=${TRG} PRE_SRC=${PRE_SRC} PRE_TRG=${PRE_TRG} ${MAKEARGS} ${@:.submitcpu=}' >> $@
