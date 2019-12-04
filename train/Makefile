# -*-makefile-*-
#
# multi-source models with Marian
# see https://arxiv.org/pdf/1706.04138.pdf
# and https://marian-nmt.github.io/faq
#
#
# MT models using MarianNMT
#
# general parameters / variables (see Makefile.config)
#   SRCLANGS ............ set source language(s)      (en)
#   TRGLANGS ............ set target language(s)      (de)
#
# 
# submit jobs by adding suffix to make-target to be run
#   .submit ........ job on GPU nodes (for train and translate)
#   .submitcpu ..... job on CPU nodes (for translate and eval)
#
# for example:
#    make train.submit
#
# run a multigpu job, for example
#    make train-multigpu.submit
#    make train-twogpu.submit
#    make train-gpu01.submit
#    make train-gpu23.submit
#
#
# typical procedure: train and evaluate en-de with 3 models in ensemble
#
# make data.submitcpu
# make vocab.submit
# make NR=1 train.submit
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
# make NR=1 train-RL.submit
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


# check and adjust Makfile.env and Makfile.config
# add specific tasks in Makefile.tasks


include Makefile.env
include Makefile.config
include Makefile.dist
include Makefile.tasks
include Makefile.data
include Makefile.doclevel
include Makefile.slurm


#------------------------------------------------------------------------
# make various data sets
#------------------------------------------------------------------------


.PHONY: data
data:	${TRAIN_SRC}.${PRE_SRC}.gz ${TRAIN_TRG}.${PRE_TRG}.gz \
	${DEV_SRC}.${PRE_SRC} ${DEV_TRG}.${PRE_TRG}
	${MAKE} ${TEST_SRC}.${PRE_SRC} ${TEST_TRG}
	${MAKE} ${TRAIN_BASE}${TRAINSIZE}.${PRE_SRC}-${PRE_TRG}.src-trg.alg.gz


traindata: 	${TRAIN_SRC}.${PRE_SRC}.gz ${TRAIN_TRG}.${PRE_TRG}.gz
tunedata: 	${TUNE_SRC}.${PRE_SRC} ${TUNE_TRG}.${PRE_TRG}
devdata:	${DEV_SRC}.${PRE_SRC} ${DEV_TRG}.${PRE_TRG}
testdata:	${TEST_SRC}.${PRE_SRC} ${TEST_TRG}
wordalign:	${TRAIN_ALG}

devdata-raw:	${DEV_SRC} ${DEV_TRG}


#------------------------------------------------------------------------
# train, translate and evaluate
#------------------------------------------------------------------------


## other model types
vocab: ${MODEL_VOCAB}
train: ${WORKDIR}/${MODEL}.${MODELTYPE}.model${NR}.done
translate: ${WORKDIR}/${TESTSET}.${MODEL}${NR}.${MODELTYPE}.${SRC}.${TRG}
eval: ${WORKDIR}/${TESTSET}.${MODEL}${NR}.${MODELTYPE}.${SRC}.${TRG}.eval
compare: ${WORKDIR}/${TESTSET}.${MODEL}${NR}.${MODELTYPE}.${SRC}.${TRG}.compare

## ensemble of models (assumes to find them in subdirs of the WORKDIR)
translate-ensemble: ${WORKDIR}/${TESTSET}.${MODEL}${NR}.${MODELTYPE}.ensemble.${SRC}.${TRG}
eval-ensemble: ${WORKDIR}/${TESTSET}.${MODEL}${NR}.${MODELTYPE}.ensemble.${SRC}.${TRG}.eval


## resume training on an existing model
resume:
	if [ -e ${WORKDIR}/${MODEL}.${MODELTYPE}.model${NR}.npz.best-perplexity.npz ]; then \
	  cp ${WORKDIR}/${MODEL}.${MODELTYPE}.model${NR}.npz.best-perplexity.npz \
	     ${WORKDIR}/${MODEL}.${MODELTYPE}.model${NR}.npz; \
	fi
	sleep 1
	rm -f ${WORKDIR}/${MODEL}.${MODELTYPE}.model${NR}.done
	${MAKE} train


#------------------------------------------------------------------------
# translate and evaluate all test sets in testsets/
#------------------------------------------------------------------------

## testset dir for all test sets in this language pair
## and all trokenized test sets that can be found in that directory
TESTSET_DIR  = ${PWD}/testsets/${SRC}-${TRG}
TESTSETS     = $(patsubst ${TESTSET_DIR}/%.${SRC}.tok.gz,%,${wildcard ${TESTSET_DIR}/*.${SRC}.tok.gz})
TESTSETS_PRE = $(patsubst %.gz,%.${PRE}.gz,${sort $(subst .${PRE},,${wildcard ${TESTSET_DIR}/*.${SRC}.gz})})

## eval all available test sets
eval-testsets:
	for s in ${SRCLANGS}; do \
	  for t in ${TRGLANGS}; do \
	    ${MAKE} SRC=$$s TRG=$$t compare-testsets-langpair; \
	  done \
	done

%-testsets-langpair: ${TESTSETS_PRE}
	for t in ${TESTSETS}; do \
	  ${MAKE} TESTSET=$$t ${@:-testsets-langpair=}; \
	done



#------------------------------------------------------------------------
# some helper functions
#------------------------------------------------------------------------


## check whether a model is converged or not
finished:
	@if grep -q 'stalled ${MARIAN_EARLY_STOPPING} times' ${WORKDIR}/${MODEL_VALIDLOG}; then\
	   echo "${WORKDIR}/${MODEL_BASENAME} finished"; \
	else \
	   echo "${WORKDIR}/${MODEL_BASENAME} unfinished"; \
	fi


## extension -all: run something over all language pairs, e.g.
##   make wordalign-all
## this goes sequentially over all language pairs
## for the parallelizable version of this: look at %-all-parallel
%-all:
	for l in ${ALL_LANG_PAIRS}; do \
	    ${MAKE} SRCLANGS="`echo $$l | cut -f1 -d'-' | sed 's/\\+/ /g'`" \
		    TRGLANGS="`echo $$l | cut -f2 -d'-' | sed 's/\\+/ /g'`" ${@:-all=}; \
	done

# run something over all language pairs that have trained models
## - make eval-all
## - make dist-all
%-allmodels:
	for l in ${ALL_LANG_PAIRS}; do \
	  if  [ `find ${WORKHOME}/$$l -name '${DATASET}${TRAINSIZE}.${PRE_SRC}-${PRE_TRG}.*.npz' | wc -l` -gt 0 ]; then \
	    ${MAKE} SRCLANGS="`echo $$l | cut -f1 -d'-' | sed 's/\\+/ /g'`" \
		    TRGLANGS="`echo $$l | cut -f2 -d'-' | sed 's/\\+/ /g'`" ${@:-allmodels=}; \
	  fi \
	done


## run something over all language pairs but make it possible to do it in parallel
%-all-parallel:
	${MAKE} $(subst -all-parallel,,${patsubst %,$@__%-run-for-langpair,${ALL_LANG_PAIRS}})

## run a command that includes the langpair, for example
##   make wordalign__en-da+sv-run  ...... runs wordalign with SRCLANGS="en" TRGLANGS="da sv"
## What is this good for?
## ---> can run many lang-pairs in parallel instead of having a for loop and run sequencetially
%-run-for-langpair:
	${MAKE} SRCLANGS='$(subst +, ,$(firstword $(subst -, ,${lastword ${subst __, ,${@:-run-for-langpair=}}})))' \
		TRGLANGS='$(subst +, ,$(lastword $(subst -, ,${lastword ${subst __, ,${@:-run-for-langpair=}}})))' \
	${shell echo $@ | sed 's/__.*$$//'}


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


## run on CPUs (translate-cpu, eval-cpu, translate-ensemble-cpu, ...)
%-cpu:
	${MAKE} MARIAN=${MARIANCPU} \
		LOADMODS='${LOADCPU}' \
		MARIAN_DECODER_FLAGS="${MARIAN_DECODER_CPU}" \
	${@:-cpu=}


## document level models
%-doc:
	${MAKE} WORKHOME=${shell realpath ${PWD}/work-spm} \
		PRE=norm \
		PRE_SRC=spm${SRCBPESIZE:000=}k.doc${CONTEXT_SIZE} \
		PRE_TRG=spm${TRGBPESIZE:000=}k.doc${CONTEXT_SIZE} \
	${@:-doc=}


## sentence-piece models
%-spm:
	${MAKE} WORKHOME=${shell realpath ${PWD}/work-spm} \
		PRE=norm \
		PRE_SRC=spm${SRCBPESIZE:000=}k \
		PRE_TRG=spm${TRGBPESIZE:000=}k \
	${@:-spm=}


## BPE models
%-bpe:
	${MAKE} WORKHOME=${shell realpath ${PWD}/work-bpe} \
		PRE=tok \
		MODELTYPE=transformer \
		PRE_SRC=bpe${SRCBPESIZE:000=}k \
		PRE_TRG=bpe${TRGBPESIZE:000=}k \
	${@:-bpe=}

%-bpe-align:
	${MAKE} WORKHOME=${shell realpath ${PWD}/work-bpe-align} \
		PRE=tok \
		PRE_SRC=bpe${SRCBPESIZE:000=}k \
		PRE_TRG=bpe${TRGBPESIZE:000=}k \
	${@:-bpe-align=}

%-bpememad:
	${MAKE} WORKHOME=${shell realpath ${PWD}/work-bpe-memad} \
		PRE=tok \
		MODELTYPE=transformer \
		PRE_SRC=bpe${SRCBPESIZE:000=}k \
		PRE_TRG=bpe${TRGBPESIZE:000=}k \
	${@:-bpememad=}

%-bpeold:
	${MAKE} WORKHOME=${shell realpath ${PWD}/work-bpe-old} \
		PRE=tok \
		MODELTYPE=transformer \
		PRE_SRC=bpe${SRCBPESIZE:000=}k \
		PRE_TRG=bpe${TRGBPESIZE:000=}k \
	${@:-bpeold=}


## for the inbuilt sentence-piece segmentation:
#		PRE_SRC=txt PRE_TRG=txt
#		MARIAN=${MARIAN}-spm
#		MODEL_VOCABTYPE=spm








## continue document-level training with a new context size

ifndef NEW_CONTEXT
  NEW_CONTEXT = $$(($(CONTEXT_SIZE) + $(CONTEXT_SIZE)))
endif

continue-doctrain:
	mkdir -p ${WORKDIR}/${MODEL}
	cp ${MODEL_VOCAB} ${WORKDIR}/${MODEL}/$(subst .doc${CONTEXT_SIZE},.doc${NEW_CONTEXT},${notdir ${MODEL_VOCAB}})
	cp ${MODEL_FINAL} ${WORKDIR}/${MODEL}/$(subst .doc${CONTEXT_SIZE},.doc${NEW_CONTEXT},$(notdir ${MODEL_BASENAME})).npz
	${MAKE} MODEL_SUBDIR=${MODEL}/ CONTEXT_SIZE=$(NEW_CONTEXT) train-doc




## continue training with a new dataset

ifndef NEW_DATASET
  NEW_DATASET = OpenSubtitles
endif

continue-datatrain:
	mkdir -p ${WORKDIR}/${MODEL}
	cp ${MODEL_VOCAB} ${WORKDIR}/${MODEL}/$(patsubst ${DATASET}%,${NEW_DATASET}%,${notdir ${MODEL_VOCAB}})
	cp ${MODEL_FINAL} ${WORKDIR}/${MODEL}/$(patsubst ${DATASET}%,${NEW_DATASET}%,${MODEL_BASENAME}).npz
	if [ -e ${BPESRCMODEL} ]; then \
	  cp ${BPESRCMODEL} $(patsubst ${WORKDIR}/train/${DATASET}%,${WORKDIR}/train/${NEW_DATASET}%,${BPESRCMODEL}); \
	  cp ${BPETRGMODEL} $(patsubst ${WORKDIR}/train/${DATASET}%,${WORKDIR}/train/${NEW_DATASET}%,${BPETRGMODEL}); \
	fi
	if [ -e ${SPMSRCMODEL} ]; then \
	  cp ${SPMSRCMODEL} $(patsubst ${WORKDIR}/train/${DATASET}%,${WORKDIR}/train/${NEW_DATASET}%,${SPMSRCMODEL}); \
	  cp ${SPMTRGMODEL} $(patsubst ${WORKDIR}/train/${DATASET}%,${WORKDIR}/train/${NEW_DATASET}%,${SPMTRGMODEL}); \
	fi
	${MAKE} MODEL_SUBDIR=${MODEL}/ DATASET=$(NEW_DATASET) train


# MARIAN_EXTRA="${MARIAN_EXTRA} --no-restore-corpus"



#------------------------------------------------------------------------
# training MarianNMT models
#------------------------------------------------------------------------


## make vocabulary
## - no new vocabulary is created if the file already exists!
## - need to delete the file if you want to create a new one!

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


## NEW: take away dependency on ${MODEL_VOCAB}
## (will be created by marian if it does not exist)

## train transformer model
${WORKDIR}/${MODEL}.transformer.model${NR}.done: \
		${TRAIN_SRC}.${PRE_SRC}${TRAINSIZE}.gz \
		${TRAIN_TRG}.${PRE_TRG}${TRAINSIZE}.gz \
		${DEV_SRC}.${PRE_SRC} ${DEV_TRG}.${PRE_TRG}
	mkdir -p ${dir $@}
	${LOADMODS} && ${MARIAN}/marian ${MARIAN_EXTRA} \
        --model $(@:.done=.npz) \
	--type transformer \
        --train-sets ${word 1,$^} ${word 2,$^} ${MARIAN_TRAIN_WEIGHTS} \
        --max-length 500 \
        --vocabs ${MODEL_VOCAB} ${MODEL_VOCAB} \
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







## NEW: take away dependency on ${MODEL_VOCAB}

## train transformer model with guided alignment
${WORKDIR}/${MODEL}.transformer-align.model${NR}.done: \
		${TRAIN_SRC}.${PRE_SRC}${TRAINSIZE}.gz \
		${TRAIN_TRG}.${PRE_TRG}${TRAINSIZE}.gz \
		${TRAIN_ALG} \
		${DEV_SRC}.${PRE_SRC} ${DEV_TRG}.${PRE_TRG}
	mkdir -p ${dir $@}
	${LOADMODS} && ${MARIAN}/marian ${MARIAN_EXTRA} \
        --model $(@:.done=.npz) \
	--type transformer \
        --train-sets ${word 1,$^} ${word 2,$^} ${MARIAN_TRAIN_WEIGHTS} \
        --max-length 500 \
        --vocabs ${MODEL_VOCAB} ${MODEL_VOCAB} \
        --mini-batch-fit \
	-w ${MARIAN_WORKSPACE} \
	--maxi-batch 500 \
        --early-stopping ${MARIAN_EARLY_STOPPING} \
        --valid-freq ${MARIAN_VALID_FREQ} \
	--save-freq ${MARIAN_SAVE_FREQ} \
	--disp-freq ${MARIAN_DISP_FREQ} \
        --valid-sets ${word 4,$^} ${word 5,$^} \
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
        --exponential-smoothing \
	--guided-alignment ${word 3,$^}
	touch $@



#------------------------------------------------------------------------
# translate with an ensemble of several models
#------------------------------------------------------------------------

ENSEMBLE = ${wildcard ${WORKDIR}/${MODEL}.${MODELTYPE}.model*.npz.best-perplexity.npz}

${WORKDIR}/${TESTSET}.${MODEL}${NR}.${MODELTYPE}.ensemble.${SRC}.${TRG}: ${TEST_SRC}.${PRE_SRC} ${ENSEMBLE}
	mkdir -p ${dir $@}
	grep . $< > $@.input
	${LOADMODS} && ${MARIAN}/marian-decoder -i $@.input \
		--models ${ENSEMBLE} \
		--vocabs ${WORKDIR}/${MODEL}.vocab.yml \
			${WORKDIR}/${MODEL}.vocab.yml \
			${WORKDIR}/${MODEL}.vocab.yml \
		${MARIAN_DECODER_FLAGS} > $@.output
ifeq (${PRE_TRG},spm${TRGBPESIZE:000=}k)
	sed 's/ //g;s/▁/ /g' < $@.output > $@
else
	sed 's/\@\@ //g;s/ \@\@//g;s/ \@\-\@ /-/g' < $@.output |\
	$(TOKENIZER)/detokenizer.perl -l ${TRG} > $@
endif
	rm -f $@.input $@.output


#------------------------------------------------------------------------
# translate, evaluate and generate a file 
# for comparing system to reference translations
#------------------------------------------------------------------------

${WORKDIR}/${TESTSET}.${MODEL}${NR}.${MODELTYPE}.${SRC}.${TRG}: ${TEST_SRC}.${PRE_SRC} ${MODEL_FINAL}
	mkdir -p ${dir $@}
	grep . $< > $@.input
	${LOADMODS} && ${MARIAN}/marian-decoder -i $@.input \
		-c ${word 2,$^}.decoder.yml \
		-d ${MARIAN_GPUS} \
		${MARIAN_DECODER_FLAGS} > $@.output
ifeq (${PRE_TRG},spm${TRGBPESIZE:000=}k)
	sed 's/ //g;s/▁/ /g' < $@.output > $@
else
	sed 's/\@\@ //g;s/ \@\@//g;s/ \@\-\@ /-/g' < $@.output |\
	$(TOKENIZER)/detokenizer.perl -l ${TRG} > $@
endif
	rm -f $@.input $@.output


%.eval: % ${TEST_TRG}
	grep . ${TEST_TRG} > $@.ref
	grep . $< > $@.sys
	cat $@.sys | sacrebleu $@.ref > $@
	cat $@.sys | sacrebleu --metrics=chrf --width=3 $@.ref >> $@
	rm -f $@.ref $@.sys


%.compare: %.eval
	paste -d "\n" ${TEST_SRC} ${TEST_TRG} ${<:.eval=} |\
	sed 	-e "s/&apos;/'/g" \
		-e 's/&quot;/"/g' \
		-e 's/&lt;/</g' \
		-e 's/&gt;/>/g' \
		-e 's/&amp;/&/g' |\
	sed 'n;n;G;' > $@
