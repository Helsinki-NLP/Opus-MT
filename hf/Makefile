#-*-makefile-*-
#
# recipes for converting OPUS-MT models to pyTorch/huggingface
# and for uploading them to the huggingface model hub
#
## TODO:
##
## * list all available languages, unreliable languages, insufficiently tested languages
##   (using some heuristics)
## 
## * vocabularies in SPM files (joint or separate vocabs): e.g
## 	eng-fin/opusTCv20210807+nopar+ft95-jointvoc_transformer-tiny11-align_2022-01-27.zip
##	eng-fin/opusTCv20210807+nopar+ft95-sepvoc_transformer-tiny11-align_2022-01-25.zip
##   --> create yaml-files on the fly for the joint vocab file? (from *.vocab file?)
##   --> different conversion script for separate vocab files?
##


## list all models that need to be converted
##   TODO: find a good way to automatically select reasonable models
##   TODO: some kind of quality control before converting/publishing

## maximum validation ppl score for an acceptable model:
MAX_PPL_SCORE = 7

MARIAN_MODELS = \
	Tatoeba-MT-models/aav-deu+eng+fra+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-29 \
	Tatoeba-MT-models/aav-deu+eng+nld/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/aav-eng/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/aav-fra+ita+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/afa-deu+eng+fra+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-29 \
	Tatoeba-MT-models/afa-deu+eng+nld/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/afa-eng/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/afa-fra+ita+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/alv-deu+eng+fra+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/alv-deu+eng+nld/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/alv-eng/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/alv-fra+ita+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/art-deu+eng+nld/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/art-eng/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/art-fra+ita+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/bat-deu+eng+fra+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/bat-deu+eng+nld/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/bat-eng/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/ber-deu+eng+nld/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-18 \
	Tatoeba-MT-models/ber-eng/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/bnt-deu+eng+fra+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/bnt-deu+eng+nld/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-18 \
	Tatoeba-MT-models/bnt-eng/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/bnt-fra+ita+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/cau-deu+eng+fra+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/cau-deu+eng+nld/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-18 \
	Tatoeba-MT-models/cau-eng/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/cdc-deu+eng+fra+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/cdc-eng/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/cel-deu+eng+fra+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/cel-eng/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/cus-deu+eng+fra+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/deu+eng+fra+por+spa-aav/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-29 \
	Tatoeba-MT-models/deu+eng+fra+por+spa-afa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-29 \
	Tatoeba-MT-models/deu+eng+fra+por+spa-art/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/deu+eng+fra+por+spa-bat/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/deu+eng+fra+por+spa-bnt/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/deu+eng+fra+por+spa-cau/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/deu+eng+fra+por+spa-dra/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/deu+eng+fra+por+spa-fiu/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/deu+eng+fra+por+spa-gem/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/deu+eng+fra+por+spa-gmq/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/deu+eng+fra+por+spa-gmw/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/deu+eng+fra+por+spa-iir/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/deu+eng+fra+por+spa-inc/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/deu+eng+fra+por+spa-ine/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/deu+eng+fra+por+spa-itc/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/deu+eng+fra+por+spa-map/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/deu+eng+fra+por+spa-mkh/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/deu+eng+fra+por+spa-mul/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/deu+eng+fra+por+spa-phi/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/deu+eng+fra+por+spa-poz/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/deu+eng+fra+por+spa-pqe/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/deu+eng+fra+por+spa-pqw/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/deu+eng+fra+por+spa-roa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/deu+eng+fra+por+spa-sem/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/deu+eng+fra+por+spa-sit/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/deu+eng+fra+por+spa-sla/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/deu+eng+fra+por+spa-trk/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/deu+eng+fra+por+spa-urj/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/deu+eng+fra+por+spa-zhx/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/dmn-deu+eng+fra+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/dra-deu+eng+nld/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-18 \
	Tatoeba-MT-models/dra-eng/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/fiu-deu+eng+fra+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/fiu-eng/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/fiu-fra+ita+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/gem-deu+eng+fra+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/gem-eng/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/gem-fra+ita+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/gmq-deu+eng+fra+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/gmq-eng/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/gmw-deu+eng+fra+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/gmw-deu+eng+nld/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-18 \
	Tatoeba-MT-models/gmw-eng/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/gmw-fra+ita+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/iir-deu+eng+fra+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/iir-deu+eng+nld/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-18 \
	Tatoeba-MT-models/iir-eng/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/inc-deu+eng+fra+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/inc-deu+eng+nld/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-18 \
	Tatoeba-MT-models/inc-eng/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/ine-deu+eng+fra+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/ine-deu+eng+nld/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-18 \
	Tatoeba-MT-models/ine-eng/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/ira-deu+eng+fra+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/itc-deu+eng+fra+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/itc-deu+eng+nld/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-18 \
	Tatoeba-MT-models/itc-fra+ita+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/map-deu+eng+nld/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-18 \
	Tatoeba-MT-models/map-eng/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/map-fra+ita+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/mkh-deu+eng+fra+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/mkh-deu+eng+nld/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-18 \
	Tatoeba-MT-models/mkh-eng/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/mkh-fra+ita+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/mul-deu+eng+fra+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/mul-deu+eng+nld/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-18 \
	Tatoeba-MT-models/mul-eng/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/mul-mul/opusTCv20230926+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/nic-deu+eng+fra+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/nic-deu+eng+nld/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-18 \
	Tatoeba-MT-models/nic-eng/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/nic-fra+ita+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/phi-deu+eng+fra+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/phi-deu+eng+nld/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-18 \
	Tatoeba-MT-models/phi-eng/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/poz-deu+eng+fra+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/poz-eng/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/poz-fra+ita+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/pqe-deu+eng+fra+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/pqe-eng/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/pqw-deu+eng+fra+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/pqw-eng/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/pqw-fra+ita+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/roa-deu+eng+fra+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/roa-eng/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/sai-deu+eng+nld/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-18 \
	Tatoeba-MT-models/sai-eng/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/sem-deu+eng+fra+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/sem-deu+eng+nld/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-18 \
	Tatoeba-MT-models/sem-eng/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/sit-deu+eng+fra+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/sit-eng/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/sla-deu+eng+fra+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/sla-deu+eng+nld/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-18 \
	Tatoeba-MT-models/sla-eng/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/tai-deu+eng+fra+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/tai-eng/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/trk-deu+eng+fra+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/tup-deu+eng+nld/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-18 \
	Tatoeba-MT-models/tup-eng/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/urj-deu+eng+fra+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/urj-deu+eng+nld/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-18 \
	Tatoeba-MT-models/urj-eng/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/urj-fra+ita+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/xgn-deu+eng+fra+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/xgn-eng/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17 \
	Tatoeba-MT-models/zhx-deu+eng+fra+por+spa/opusTCv20230926max50+bt+jhubc_transformer-big_2024-05-30 \
	Tatoeba-MT-models/zhx-eng/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17



MARIAN_MODEL_URLS = $(patsubst %,https://object.pouta.csc.fi/%.zip,${MARIAN_MODELS})


# MARIAN_MODEL_URLS = \
#	https://object.pouta.csc.fi/Tatoeba-MT-models/ine-deu+eng+nld/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-18.zip
#	https://object.pouta.csc.fi/Tatoeba-MT-models/sla-eng/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17.zip
#	https://object.pouta.csc.fi/Tatoeba-MT-models/afa-eng/opusTCv20230926max50+bt+jhubc_transformer-big_2024-08-17.zip


# MARIAN_MODEL_URLS = \
# 	https://object.pouta.csc.fi/Tatoeba-MT-models/eng-hbs/opus+bt-2021-04-20.zip

## models released between 2022-07-23 - 2022-08-11

# MARIAN_MODEL_URLS = \
# 	https://object.pouta.csc.fi/Tatoeba-MT-models/itc-itc/opusTCv20210807_transformer-big_2022-08-10.zip \
# 	https://object.pouta.csc.fi/Tatoeba-MT-models/gmw-gmw/opusTCv20210807_transformer-big_2022-08-11.zip \
# 	https://object.pouta.csc.fi/Tatoeba-MT-models/gmq-gmq/opusTCv20210807_transformer-big_2022-07-29.zip \
# 	https://object.pouta.csc.fi/Tatoeba-MT-models/zls-itc/opusTCv20210807_transformer-big_2022-08-10.zip \
# 	https://object.pouta.csc.fi/Tatoeba-MT-models/gmq-itc/opusTCv20210807_transformer-big_2022-08-09.zip \
# 	https://object.pouta.csc.fi/Tatoeba-MT-models/itc-ara/opusTCv20210807_transformer-big_2022-08-09.zip \
# 	https://object.pouta.csc.fi/Tatoeba-MT-models/ara-gmq/opusTCv20210807_transformer-big_2022-08-09.zip \
# 	https://object.pouta.csc.fi/Tatoeba-MT-models/zle-itc/opusTCv20210807_transformer-big_2022-08-03.zip \
# 	https://object.pouta.csc.fi/Tatoeba-MT-models/itc-heb/opusTCv20210807_transformer-big_2022-08-03.zip \
# 	https://object.pouta.csc.fi/Tatoeba-MT-models/gmq-zlw/opusTCv20210807_transformer-big_2022-08-03.zip \
# 	https://object.pouta.csc.fi/Tatoeba-MT-models/zho-jpn/opusTCv20210807-sepvoc_transformer-big_2022-07-28.zip \
# 	https://object.pouta.csc.fi/Tatoeba-MT-models/itc-tur/opusTCv20210807_transformer-big_2022-07-28.zip \
# 	https://object.pouta.csc.fi/Tatoeba-MT-models/gmq-heb/opusTCv20210807_transformer-big_2022-07-28.zip \
# 	https://object.pouta.csc.fi/Tatoeba-MT-models/ara-itc/opusTCv20210807_transformer-big_2022-07-28.zip \
# 	https://object.pouta.csc.fi/Tatoeba-MT-models/itc-bat/opusTCv20210807_transformer-big_2022-07-27.zip \
# 	https://object.pouta.csc.fi/Tatoeba-MT-models/gmq-ara/opusTCv20210807_transformer-big_2022-07-27.zip \
# 	https://object.pouta.csc.fi/Tatoeba-MT-models/zls-deu/opusTCv20210807_transformer-big_2022-07-26.zip \
# 	https://object.pouta.csc.fi/Tatoeba-MT-models/gmq-tur/opusTCv20210807_transformer-big_2022-07-26.zip \
# 	https://object.pouta.csc.fi/Tatoeba-MT-models/deu-spa/opusTCv20210807_transformer-big_2022-07-26.zip \
# 	https://object.pouta.csc.fi/Tatoeba-MT-models/heb-itc/opusTCv20210807_transformer-big_2022-07-25.zip \
# 	https://object.pouta.csc.fi/Tatoeba-MT-models/deu-gmq/opusTCv20210807_transformer-big_2022-07-25.zip \
# 	https://object.pouta.csc.fi/Tatoeba-MT-models/heb-gmq/opusTCv20210807_transformer-big_2022-07-23.zip \
# 	https://object.pouta.csc.fi/Tatoeba-MT-models/itc-eus/opusTCv20210807_transformer-big_2022-07-23.zip \
# 	https://object.pouta.csc.fi/Tatoeba-MT-models/fin-zls/opusTCv20210807_transformer-big_2022-07-23.zip \
# 	https://object.pouta.csc.fi/Tatoeba-MT-models/fas-itc/opusTCv20210807_transformer-big_2022-07-23.zip \
# 	https://object.pouta.csc.fi/Tatoeba-MT-models/fas-gmq/opusTCv20210807_transformer-big_2022-07-23.zip \
# 	https://object.pouta.csc.fi/Tatoeba-MT-models/eus-itc/opusTCv20210807_transformer-big_2022-07-23.zip


# MARIAN_MODEL_URLS = \
# 	https://object.pouta.csc.fi/Tatoeba-MT-models/eng-kor/opusTCv20210807-sepvoc_transformer-big_2022-07-28.zip \
# 	https://object.pouta.csc.fi/Tatoeba-MT-models/kor-eng/opusTCv20210807-sepvoc_transformer-big_2022-07-28.zip

# MARIAN_MODEL_URLS = \
#	https://object.pouta.csc.fi/Tatoeba-MT-models/eng-hun/opusTCv20210807+bt_transformer-big_2022-02-25.zip
# 	https://object.pouta.csc.fi/Tatoeba-MT-models/eng-hun/opus+bt-2021-04-13.zip 
#	https://object.pouta.csc.fi/Tatoeba-MT-models/eng-hun/opusTCv20210807+bt_transformer-big_2022-02-25.zip
# 	https://object.pouta.csc.fi/Tatoeba-MT-models/gmw-gmw/opus-2021-02-23.zip \
#	https://object.pouta.csc.fi/Tatoeba-MT-models/eng-fin/opusTCv20210807+bt-2021-09-01.zip
#	https://object.pouta.csc.fi/Tatoeba-MT-models/eng-fin/opusTCv20210807+bt-2021-12-08.zip \
#	https://object.pouta.csc.fi/Tatoeba-MT-models/eng-fin/opusTCv20210807+bt-2021-09-01.zip \
#	https://object.pouta.csc.fi/Tatoeba-MT-models/gmw-eng/opus4m+btTCv20210807-2021-09-30.zip

## broken yml file:
# 	https://object.pouta.csc.fi/Tatoeba-MT-models/eng-gmw/opus1m+bt-2021-04-10.zip


## models for Ukrainian

# 	https://object.pouta.csc.fi/Tatoeba-MT-models/fin-eng/opusTCv20210807+bt-2021-12-08.zip \
# 	https://object.pouta.csc.fi/Tatoeba-MT-models/eng-fin/opusTCv20210807+bt_transformer-big_2022-03-09.zip
# 	https://object.pouta.csc.fi/Tatoeba-MT-models/zle-eng/opusTCv20210807+bt_transformer-big_2022-03-17.zip \
#	https://object.pouta.csc.fi/Tatoeba-MT-models/eng-zle/opusTCv20210807+bt_transformer-big_2022-03-13.zip


# done for Ukrainian (2022-03-23)

# https://object.pouta.csc.fi/Tatoeba-MT-models/ukr-fin/opusTCv20210807+pft+pbt_transformer-align_2022-03-17.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/ukr-ces+slk/opusTCv20210807+pft_transformer-align_2022-03-17.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/ukr-hun/opusTCv20210807+pft_transformer-align_2022-03-08.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/ukr-ron/opusTCv20210807+pft_transformer-align_2022-03-08.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/ukr-tur/opusTCv20210807+pft_transformer-align_2022-03-07.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/zle-bat/opusTCv20210807_transformer-align_2022-03-14.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/zle-deu/opusTCv20210807_transformer-big_2022-03-19.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/zle-eng/opusTCv20210807+bt_transformer-big_2022-03-17.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/zle-fra/opusTCv20210807_transformer-big_2022-03-23.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/zle-gmq/opusTCv20210807+pft_transformer-big_2022-03-14.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/zle-ita/opusTCv20210807_transformer-big_2022-03-19.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/zle-por/opusTCv20210807_transformer-big_2022-03-23.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/zle-spa/opusTCv20210807_transformer-big_2022-03-23.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/zle-zle/opusTCv20210807+bt_transformer-big_2022-03-07.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/zle-zls/opusTCv20210807+bt_transformer-big_2022-03-23.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/zle-zlw/opusTCv20210807+bt_transformer-big_2022-03-23.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/bat-zle/opusTCv20210807_transformer-align_2022-03-13.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/ces+slk-ukr/opusTCv20210807+pbt_transformer-align_2022-03-08.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/deu-zle/opusTCv20210807_transformer-big_2022-03-23.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/eng-zle/opusTCv20210807+bt_transformer-big_2022-03-13.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/fin-ukr/opusTCv20210807+pbt_transformer-align_2022-03-07.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/fra-zle/opusTCv20210807_transformer-big_2022-03-23.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/gmq-zle/opusTCv20210807+pbt_transformer-big_2022-03-23.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/hun-ukr/opusTCv20210807+pbt_transformer-align_2022-03-08.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/ita-zle/opusTCv20210807_transformer-big_2022-03-23.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/por-zle/opusTCv20210807_transformer-big_2022-03-23.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/ron-ukr/opusTCv20210807+pbt_transformer-align_2022-03-08.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/spa-zle/opusTCv20210807_transformer-big_2022-03-23.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/tur-ukr/opusTCv20210807+pbt_transformer-align_2022-03-07.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/zls-zle/opusTCv20210807+bt_transformer-big_2022-03-23.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/zlw-zle/opusTCv20210807+bt_transformer-big_2022-03-19.zip


## done for English-xxx both directions (big transformer)

# https://object.pouta.csc.fi/Tatoeba-MT-models/eng-fin/opusTCv20210807+bt_transformer-big_2022-03-09.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/zle-eng/opusTCv20210807+bt_transformer-big_2022-03-17.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/eng-zle/opusTCv20210807+bt_transformer-big_2022-03-13.zip \

# MARIAN_MODEL_URLS = \
# https://object.pouta.csc.fi/Tatoeba-MT-models/eng-ara/opusTCv20210807+bt_transformer-big_2022-02-25.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/eng-bul/opusTCv20210807+bt_transformer-big_2022-02-25.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/eng-cat+oci+spa/opusTCv20210807+bt_transformer-big_2022-03-13.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/eng-ces+slk/opusTCv20210807+bt_transformer-big_2022-03-13.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/eng-ell/opusTCv20210807+bt_transformer-big_2022-03-13.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/eng-est/opusTCv20210807+bt_transformer-big_2022-03-13.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/eng-fra/opusTCv20210807+bt_transformer-big_2022-03-09.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/eng-gmq/opusTCv20210807+bt_transformer-big_2022-03-17.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/eng-hun/opusTCv20210807+bt_transformer-big_2022-02-25.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/eng-ita/opusTCv20210807+bt_transformer-big_2022-03-13.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/eng-lav/opusTCv20210807+bt_transformer-big_2022-03-13.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/eng-lit/opusTCv20210807+bt_transformer-big_2022-02-25.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/eng-por/opusTCv20210807+bt_transformer-big_2022-03-13.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/eng-ron/opusTCv20210807+bt_transformer-big_2022-02-25.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/eng-spa/opusTCv20210807+bt_transformer-big_2022-03-13.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/eng-tur/opusTCv20210807+bt_transformer-big_2022-02-25.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/ara-eng/opusTCv20210807+bt_transformer-big_2022-03-09.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/bul-eng/opusTCv20210807+bt_transformer-big_2022-03-09.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/cat+oci+spa-eng/opusTCv20210807+bt_transformer-big_2022-03-13.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/cel-eng/opusTCv20210807+bt_transformer-big_2022-03-13.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/ces+slk-eng/opusTCv20210807+bt_transformer-big_2022-03-17.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/ell-eng/opusTCv20210807+bt_transformer-big_2022-02-25.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/est-eng/opusTCv20210807+bt_transformer-big_2022-03-09.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/fra-eng/opusTCv20210807+bt_transformer-big_2022-03-09.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/gmq-eng/opusTCv20210807+bt_transformer-big_2022-03-09.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/hbs-eng/opusTCv20210807+bt_transformer-big_2022-02-25.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/heb-eng/opusTCv20210807+bt_transformer-big_2022-03-13.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/hun-eng/opusTCv20210807+bt_transformer-big_2022-03-09.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/ita-eng/opusTCv20210807+bt_transformer-big_2022-02-25.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/lav-eng/opusTCv20210807+bt_transformer-big_2022-03-13.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/lit-eng/opusTCv20210807+bt_transformer-big_2022-02-25.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/tur-eng/opusTCv20210807+bt_transformer-big_2022-03-17.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/zls-eng/opusTCv20210807+bt_transformer-big_2022-03-17.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/zlw-eng/opusTCv20210807+bt_transformer-big_2022-03-17.zip


SHELL := bash

MARIAN_MODEL_URL ?= ${firstword ${MARIAN_MODEL_URLS}}

## extract language pair and release data from the URL
LANGPAIR     = $(notdir ${patsubst %/,%,${dir ${MARIAN_MODEL_URL}}})
RELEASE_DATE = ${shell echo '${basename ${MARIAN_MODEL_URL}}' | rev | cut -f1-3 -d\- | cut -f1 -d_ | rev}

## get language names and IDs in various variants
SRCLANGID   := $(firstword $(subst -, ,${LANGPAIR}))
TRGLANGID   := $(lastword $(subst -, ,${LANGPAIR}))
SRCLANG     := $(shell iso639 ${SRCLANGID} | tr '"' ' ' | xargs)
TRGLANG     := $(shell iso639 ${TRGLANGID} | tr '"' ' ' | xargs)

## two-letter codes
LANGPAIR2   := $(shell iso639 -2 -k -p ${LANGPAIR})
SRCLANGID2  := $(firstword $(subst -, ,${LANGPAIR2}))
TRGLANGID2  := $(lastword $(subst -, ,${LANGPAIR2}))

## three-letter codes
LANGPAIR3   := $(shell iso639 -3 -k -p ${LANGPAIR})
SRCLANGID3  := $(firstword $(subst -, ,${LANGPAIR3}))
TRGLANGID3  := $(lastword $(subst -, ,${LANGPAIR3}))

## the name of the workdir with the original MarianNMT model
MARIAN_MODEL     := marian-models/${basename ${notdir ${MARIAN_MODEL_URL}}}/${LANGPAIR2}

ifneq (${wildcard ${MARIAN_MODEL}/README.md},)
  MODEL_TYPE = ${shell grep 'model:' ${MARIAN_MODEL}/README.md | head -1 | cut -f2 -d: | xargs}
  MODEL_DATA = ${shell grep 'dataset:' ${MARIAN_MODEL}/README.md | head -1 | cut -f2 -d: | xargs}
  MODEL_PRE = ${shell grep 'pre-processing:' ${MARIAN_MODEL}/README.md | head -1 | cut -f2 -d: | xargs}
  MODEL_TOK = ${filter-out normalization +,${MODEL_PRE}}
  MODEL_SRCVOCAB = ${shell grep -A2 'vocabs:' ${MARIAN_MODEL}/decoder.yml | tail -2 | head -1 | sed 's/^ *\- *//' | xargs}
  MODEL_TRGVOCAB = ${shell grep -A2 'vocabs:' ${MARIAN_MODEL}/decoder.yml | tail -1 | sed 's/^ *\- *//' | xargs}
  MODEL_SRCSPM    = ${MARIAN_MODEL}/source.spm
  MODEL_TRGSPM    = ${MARIAN_MODEL}/target.spm
##
## extact languages with reasonable test sets and scores
## PROBLEM: we don't always have scores
## 
#  MODEL_SRCLANGS  = ${shell perl extract_reasonable_languages.pl ${MARIAN_MODEL}/README.md | head -1}
#  MODEL_TRGLANGS  = ${shell perl extract_reasonable_languages.pl ${MARIAN_MODEL}/README.md | head -2 | tail -1}
#  MODEL_SRCLANGS  = ${shell grep 'source language(s):' ${MARIAN_MODEL}/README.md | head -1 | cut -f2 -d: | xargs}
#  MODEL_TRGLANGS  = ${shell grep 'target language(s):' ${MARIAN_MODEL}/README.md | head -1 | cut -f2 -d: | xargs}

##
## just rely on the languages listed in the readme!
##
  MODEL_SRCLANGS  = ${shell grep 'raw source language(s):' ${MARIAN_MODEL}/README.md | head -1 | cut -f2 -d: | xargs}
  MODEL_TRGLANGS  = ${shell grep 'raw target language(s):' ${MARIAN_MODEL}/README.md | head -1 | cut -f2 -d: | xargs}
  MODEL_TRGLABELS = $(sort ${shell grep 'valid language labels:' ${MARIAN_MODEL}/README.md | head -1 | cut -f2 -d: | xargs})
  MODEL_VALID_TRGLABELS = ${MODEL_TRGLABELS}
  MODEL_LANGIDS2  = ${shell iso639 -2 -k ${sort ${MODEL_SRCLANGS} ${MODEL_TRGLANGS}}}
  MODEL_VOCAB_TXT = ${wildcard ${MARIAN_MODEL}/*.vocab}
  MODEL_VOCAB_YML = ${patsubst %,%.yml,${MODEL_VOCAB_TXT}}
endif

ifneq (${wildcard ${MARIAN_MODEL}/vocab.json},)
  VOCAB_TRGLABELS = $(sort $(shell tr ':' "\n" < ${MARIAN_MODEL}/vocab.json | grep '>>.*<<' | cut -f2 -d, | tr '"' ' '))
ifneq (${VOCAB_TRGLABELS},)
  USE_LABELS = 1
endif
endif


## get the latest model validation perplexity score from the training logs

ifneq (${wildcard ${MARIAN_MODEL}/*.valid[0-9].log},)
  MODEL_VALID_PPL := $(shell grep 'new best' ${MARIAN_MODEL}/*.valid[0-9].log | tail -1 | rev | cut -f2 -d: | rev)
endif


## multiple target languages always require labels
ifeq (${MODEL_TRGLABELS},)
ifneq ($(words ${MODEL_TRGLANGS}),1)
  USE_LABELS = 1
  MODEL_TRGLABELS = ${patsubst %,>>%<<,${MODEL_TRGLANGS}}
endif
else
  USE_LABELS = 1
endif


BACKGROUND_READING = [Democratizing neural machine translation with OPUS-MT](https://doi.org/10.1007/s10579-023-09704-w) and [OPUS-MT – Building open translation services for the World](https://aclanthology.org/2020.eamt-1.61/)

## base name for huggingface
## tc = trained on tatoeba challenge data
ifeq ($(findstring Tatoeba-MT-models,${MARIAN_MODEL_URL}),)
  HF_BASENAME   = opus-mt
  DATA_SOURCE   = https://opus.nlpl.eu/
  OPUSMT_README = https://github.com/Helsinki-NLP/OPUS-MT-train/tree/master/models/${LANGPAIR}/README.md
else
ifeq ($(findstring +jhubc,${MARIAN_MODEL_URL}),+jhubc)
  HF_BASENAME = opus-mt-tc-bible
else
  HF_BASENAME = opus-mt-tc
endif
  DATA_SOURCE = https://github.com/Helsinki-NLP/Tatoeba-Challenge
  OPUSMT_README = https://github.com/Helsinki-NLP/Tatoeba-Challenge/tree/master/models/${LANGPAIR}/README.md
  BACKGROUND_READING += and [The Tatoeba Translation Challenge – Realistic Data Sets for Low Resource and Multilingual MT](https://aclanthology.org/2020.wmt-1.139/)
endif

## modeltype to be marked in the name
## set to base if no extension to "transformer" is given
HF_MODELTYPE = $(subst transformer-,,$(subst -align,,${MODEL_TYPE}))
ifeq (${HF_MODELTYPE},transformer)
  HF_MODELTYPE = base
endif


HF_NAME       := ${subst +,_,${HF_BASENAME}-${HF_MODELTYPE}-${LANGPAIR2}}
PYTORCH_MODEL := pytorch-models/${HF_NAME}

.PHONY: all
all:
	@for m in ${MARIAN_MODEL_URLS}; do \
	  ${MAKE} MARIAN_MODEL_URL=$$m process; \
	done

.PHONY: login
login:
	huggingface-cli login


## do not fetch again and just refresh the model card
.PHONY: refresh-all
refresh-all:
	@for m in ${MARIAN_MODEL_URLS}; do \
	  ${MAKE} MARIAN_MODEL_URL=$$m convert; \
	  ${MAKE} MARIAN_MODEL_URL=$$m commit; \
	done


.PHONY: convert-all
convert-all:
	@for m in ${MARIAN_MODEL_URLS}; do \
	  ${MAKE} MARIAN_MODEL_URL=$$m fetch-and-convert; \
	done

.PHONY: commit-all
commit-all:
	@for m in ${MARIAN_MODEL_URLS}; do \
	  ${MAKE} MARIAN_MODEL_URL=$$m commit; \
	done

.PHONY: fetch-and-convert
fetch-and-convert:
	${MAKE} fetch
	${MAKE} convert


## process a model (fetch, convert, commit)
## NEW: only do that if the validation perplexity is above a certain threshold!
## NEW: only commit if we have at least one reliable eval result (see extract-task-results.pl)

.PHONY: process
process:
	${MAKE} fetch
	if [ `find ${MARIAN_MODEL}/ -name '*.valid[0-9].log' | wc -l` -gt 0 ]; then \
	  p=`grep 'new best' ${MARIAN_MODEL}/*.valid[0-9].log | tail -1 | rev | cut -f2 -d: | rev`; \
	  if (( $$(echo "$$p < ${MAX_PPL_SCORE}" | bc -l ) )); then \
	    echo "ppl score is OK for ${MARIAN_MODEL} ($$p)"; \
	    ${MAKE} convert; \
	    if [ `./extract-task-results.pl ${PYTORCH_MODEL}/benchmark_results.txt | wc -l` -gt 0 ]; then \
	      ${MAKE} commit; \
	    fi; \
	  else \
	    echo "ppl score for ${MARIAN_MODEL} is too low ($$p)"; \
	  fi \
	fi

## old: just convert and submit
##
#	${MAKE} convert
#	${MAKE} commit




.PHONY: info
info:
	@echo "workdir: ${MARIAN_MODEL}"
	@echo "release: ${RELEASE_DATE}"
	@echo "langpair: ${LANGPAIR} (${SRCLANGID3},${TRGLANGID3}) (${SRCLANGID2},${TRGLANGID2}) (${SRCLANG},${TRGLANG})"
	@echo "type: ${MODEL_TYPE}"
	@echo "data: ${MODEL_DATA}"
	@echo "tokenization: ${MODEL_TOK}"
	@echo "vocab: ${sort ${MODEL_SRCVOCAB} ${MODEL_SRCVOCAB}}"
	@echo "source langs: ${MODEL_SRCLANGS}"
	@echo "target langs: ${MODEL_TRGLANGS}"
	@echo "hfname: ${HF_NAME}"
	@echo
	@echo "testset file: ${TESTSET_TRANSLATIONS_FILE}"

.PHONY: fetch
fetch: ${MARIAN_MODEL}

.PHONY: convert
convert:
	${MAKE} ${PYTORCH_MODEL}/benchmark_results.txt
	${MAKE} ${PYTORCH_MODEL}/README.md

.PHONY: commit
commit: ${PYTORCH_MODEL}.committed


## in case we need to convert vocab files to yaml
.PHONY: vocabs
vocabs: ${MODEL_VOCAB_YML}

${MODEL_VOCAB_YML}: %.yml: %
	./vocab2yaml.py < $< > $@


## huggingface access token

${HOME}/.huggingface/token:
	huggingface-cli login
	git config --global credential.helper store


## create the repository item and upload the model

## token-based authentification:
#	-git clone https://tiedeman:`cat ${HOME}/.huggingface/token`@huggingface.co/Helsinki-NLP/${HF_NAME}
## ssh-based authentification:
#	-git clone git@hf.co:Helsinki-NLP/${HF_NAME}

ifneq (${HF_NAME},)
${PYTORCH_MODEL}.committed: ${PYTORCH_MODEL} ${PYTORCH_MODEL}/README.md ${HOME}/.huggingface/token
	-huggingface-cli repo create ${HF_NAME} --organization Helsinki-NLP --yes
	-git clone https://tiedeman:`cat ${HOME}/.huggingface/token`@huggingface.co/Helsinki-NLP/${HF_NAME}
	cd ${HF_NAME} && git lfs install
	cd ${HF_NAME} && git lfs track "*.spm"
	cd ${HF_NAME} && git config --global user.email "jorg.tiedemann@helsinki.fi"
	cd ${HF_NAME} && git config --global user.name "Joerg Tiedemann"
	mv ${PYTORCH_MODEL}/* ${HF_NAME}/
	rsync ${HF_NAME}/README.md ${PYTORCH_MODEL}/README.md
	cd ${HF_NAME} && git add .
	cd ${HF_NAME} && git commit -m "Initial commit"
	cd ${HF_NAME} && git push
	touch $@
endif



# fetch the original MarianNMT model

${MARIAN_MODEL}:
	mkdir -p $@
	wget -O $@/model.zip ${MARIAN_MODEL_URL}
	cd $@ && unzip model.zip
	rm -f $@/model.zip


transformers:
	git clone https://github.com/huggingface/transformers.git
	cd transformers
	pip install -e .

# convert the model to pyTorch

${PYTORCH_MODEL}: ${MARIAN_MODEL} ${MODEL_VOCAB_YML} transformers
	export PYTHONPATH=transformers/src:${PYTHONPATH} && \
	python convert_to_pytorch.py --model-path $< --dest-path $@
	export PYTHONPATH= && python fix_pytorch_model.py $@


## files with benchmarks and test set translations

ifneq (${wildcard ${MARIAN_MODEL}/README.md},)
  TESTSET_TRANSLATIONS_FILE = ${shell grep 'test set translations:' ${MARIAN_MODEL}/README.md | cut -f2 -d'(' | sed 's/)$$//'}
  TESTSET_OUTPUT_FILE = ${shell grep 'test set scores:' ${MARIAN_MODEL}/README.md | cut -f2 -d'(' | sed 's/)$$//'}
endif

SCORES_FILE = ${MARIAN_MODEL_URL:.zip=.scores.txt}
EVAL_FILE = ${MARIAN_MODEL_URL:.zip=.eval.zip}

.PHONY: benchmarks
benchmarks: ${PYTORCH_MODEL}/benchmark_results.txt ${PYTORCH_MODEL}/benchmark_translations.zip

${PYTORCH_MODEL}/benchmark_results.txt: ${PYTORCH_MODEL}
	-wget -q -O - ${SCORES_FILE} | cut -f1-4,6,7 > $@
	if [ ! -s $@ ]; then \
	  grep '^|' ${MARIAN_MODEL}/README.md | \
	  tail -n +3  | tr "\t" ' ' | tr '|' "\t" | sed 's/ //g' | cut -f2- | \
	  sed 's/^\([^	]*\)\.\([^	]*\)	/\2	\1	/' |\
	  awk '{ t = $$4; $$4 = $$3; $$3 = t; print } ' FS='\t' OFS='\t' |\
	  sed 's/Tatoeba-test/tatoeba-test-v2020-07-28/' |\
	  cut -f1-6 > $@; \
	fi


## verify that there is something in the test set translations
## get an example and example output
## use dummy string if no example can be downloaded

ifdef TESTSET_TRANSLATIONS_FILE
ifeq (${shell wget -q -O - ${TESTSET_TRANSLATIONS_FILE} | head -3 | wc -l | xargs},3)
  TESTSET_INPUT_EXAMPLE   := ${subst ",\",${shell wget -q -O - ${TESTSET_TRANSLATIONS_FILE} | head -1}}
  TESTSET_OUTPUT_EXAMPLE  := ${subst ",\",${shell wget -q -O - ${TESTSET_TRANSLATIONS_FILE} | head -3 | tail -1}}
  TESTSET_INPUT2_EXAMPLE  := ${subst ",\",${shell wget -q -O - ${TESTSET_TRANSLATIONS_FILE} | tail -4 | head -1}}
  TESTSET_OUTPUT2_EXAMPLE := ${subst ",\",${shell wget -q -O - ${TESTSET_TRANSLATIONS_FILE} | tail -2 | head -1}}
else
ifeq (${USE_LABELS},1)
  TESTSET_INPUT_EXAMPLE  := ${firstword ${MODEL_TRGLABELS}} Replace this with text in an accepted source language.
  TESTSET_INPUT2_EXAMPLE := ${lastword ${MODEL_TRGLABELS}} This is the second sentence.
else
  TESTSET_INPUT_EXAMPLE  := Replace this with text in an accepted source language.
  TESTSET_INPUT2_EXAMPLE := This is the second sentence.
endif
endif
endif

## create the model card

FILTER_OUT    = $(foreach v,$(2),$(if $(findstring $(1),$(v)),,$(v)))
FILTER        = $(foreach v,$(2),$(if $(findstring $(1),$(v)),$(v),))
BASIC_LANGIDS = $(sort $(filter-out xx,$(shell echo '${MODEL_LANGIDS2}' | tr ' ' "\n" | cut -f1 -d_)))
BCP47_LANGIDS = $(sort $(call FILTER_OUT,xx,$(call FILTER,_,${MODEL_LANGIDS2})))



${PYTORCH_MODEL}/benchmark_translations.zip:
	-wget -q -O $@ ${EVAL_FILE}
	if [ ! -e $@ ]; then \
	  wget -q -O ${dir $@}${notdir ${TESTSET_OUTPUT_FILE}} ${TESTSET_OUTPUT_FILE}; \
	  cd ${dir $@}; zip $@ ${notdir ${TESTSET_OUTPUT_FILE}}; \
	  rm -f ${notdir ${TESTSET_OUTPUT_FILE}}; \
	fi


## get information from the benchmark file
## - language pairs that have some kind of benchmark
## - source and target languages for which there are some benchmarks
## - reliable language pairs (according to benchmarks and some thresholds)
## - reliable source and target languages

ifneq ($(wildcard ${PYTORCH_MODEL}/benchmark_results.txt),)
  LANGPAIR_BENCHMARKS = $(sort $(shell cut -f1 ${PYTORCH_MODEL}/benchmark_results.txt))
  SRCLANG_BENCHMARKS = $(sort $(shell echo '${LANGPAIR_BENCHMARKS}' | tr ' ' "\n" | cut -f1 -d-))
  TRGLANG_BENCHMARKS = $(sort $(shell echo '${LANGPAIR_BENCHMARKS}' | tr ' ' "\n" | cut -f2 -d-))
# ifeq (${MODEL_VALID_TRGLABELS},)
# ifneq ($(words ${TRGLANG_BENCHMARKS}),1)
#   MODEL_VALID_TRGLABELS = $(filter-out >>xxx<<,${patsubst %,>>%<<,${TRGLANG_BENCHMARKS}})
# endif
# endif
  LANGPAIR_RELIABLE_BLEU = $(sort $(shell grep '	[2-9][0-9]\.[0-9]*	[1-9][0-9][0-9][0-9]*	[0-9][0-9]' ${PYTORCH_MODEL}/benchmark_results.txt | cut -f1))
  LANGPAIR_RELIABLE_CHRF = $(sort $(shell grep '0\.[5-9][0-9]*	[0-9]*\.[0-9]*	[1-9][0-9][0-9][0-9]*	[0-9][0-9]' ${PYTORCH_MODEL}/benchmark_results.txt | cut -f1))
  LANGPAIR_RELIABLE = $(sort ${LANGPAIR_RELIABLE_BLEU} ${LANGPAIR_RELIABLE_CHRF})
  SRCLANG_RELIABLE = $(sort $(shell echo '${LANGPAIR_RELIABLE}' | tr ' ' "\n" | cut -f1 -d-))
  TRGLANG_RELIABLE = $(sort $(shell echo '${LANGPAIR_RELIABLE}' | tr ' ' "\n" | cut -f2 -d-))
  LANGID2_RELIABLE = $(sort $(shell iso639 -2 -k ${SRCLANG_RELIABLE} ${TRGLANG_RELIABLE}))
  LANGID2_BASIC = $(sort $(filter-out xx,$(shell echo '${LANGID2_RELIABLE}' | tr ' ' "\n" | cut -f1 -d_)))
  LANGID2_BCP47 = $(sort $(call FILTER_OUT,xx,$(call FILTER,_,${LANGID2_RELIABLE})))
endif

ifeq (${LANGID2_BASIC},)
  LANGID2_BASIC = $(sort $(shell iso639 -2 -k ${MODEL_TRGLANGS} ${MODEL_SRCLANGS}))
endif

ifeq (${MODEL_VALID_TRGLABELS},)
ifneq ($(words ${MODEL_TRGLANGS}),1)
  MODEL_VALID_TRGLABELS = $(filter-out >>xxx<< >>xx<< >>multi<<,${patsubst %,>>%<<,${MODEL_TRGLANGS}})
endif
endif


print-reliable-langs:
	@echo "reliable BLEU scores:"
	@echo "++++++++++++++++++++++++++++++++++++++++++"
	@grep '	[2-9][0-9]\.[0-9]*	[1-9][0-9][0-9][0-9]*	[0-9][0-9]' ${PYTORCH_MODEL}/benchmark_results.txt
	@echo "reliable CHR-F scores:"
	@echo "++++++++++++++++++++++++++++++++++++++++++"
	@grep '0\.[5-9][0-9]*	[0-9]*\.[0-9]*	[1-9][0-9][0-9][0-9]*	[0-9][0-9]' ${PYTORCH_MODEL}/benchmark_results.txt
	@echo "model source languages: ${MODEL_SRCLANGS}"
	@echo "model target languages: ${MODEL_TRGLANGS}"
	@echo "basic langids: ${BASIC_LANGIDS}"
	@echo ${LANGPAIR_RELIABLE_BLEU}
	@echo ${LANGPAIR_RELIABLE_CHRF}
	@echo ${LANGPAIR_RELIABLE}
	@echo ${SRCLANG_RELIABLE}
	@echo ${TRGLANG_RELIABLE}
	@echo ${LANGID2_RELIABLE}
	@echo ${LANGID2_BASIC}
	@echo ${LANGID2_BCP47}
	@echo ${LANGPAIR_BENCHMARKS}
	@echo ${SRCLANG_BENCHMARKS}
	@echo ${TRGLANG_BENCHMARKS}



.PHONY: readme
readme: ${PYTORCH_MODEL}/README.md

URL_ENCODE = $(shell python -c 'from urllib.parse import quote; print(quote("$(1)"))')
OPUS_MT_DASHBOARD_BASEURL = https://opus.nlpl.eu/dashboard/index.php?pkg=opusmt&test=all&scoreslang=all&chart=standard&model=

${PYTORCH_MODEL}/README.md: ${PYTORCH_MODEL} ${PYTORCH_MODEL}/benchmark_results.txt ${PYTORCH_MODEL}/benchmark_translations.zip
	@echo "..... create $@"
	@echo '---'                 > $@
	@echo 'library_name: transformers' >> $@
	@echo 'language:'          >> $@
## only list reasonable languages (LANGID2_BASIC)
## PROBLEM: sometimes we don't have benchmarks
#	@for l in ${LANGID2_BASIC}; do
## --> run through all languages mentioned in the readme
	@for l in ${BASIC_LANGIDS}; do \
	  echo "- $$l"             >> $@; \
	done
ifneq (${LANGID2_BCP47},)
	@echo 'language_bcp47:'    >> $@
	@for l in ${LANGID2_BCP47}; do \
	  echo "- $$l"             >> $@; \
	done
endif
# ifneq (${BCP47_LANGIDS},)
#	@echo 'language_bcp47:'    >> $@
#	@for l in ${BCP47_LANGIDS}; do \
#	  echo "- $$l"             >> $@; \
#	done
# endif
#	@echo '- ${SRCLANGID2}'    >> $@
#	@echo '- ${TRGLANGID2}'    >> $@
	@echo ''                   >> $@
	@echo 'tags:'              >> $@
	@echo '- translation'      >> $@
ifeq ($(findstring opus-mt-tc,${HF_BASENAME}),opus-mt-tc)
	@echo '- ${HF_BASENAME}'   >> $@
endif
	@echo ''                   >> $@
	@echo 'license: apache-2.0' >> $@
	@echo 'model-index:'       >> $@
	@echo '- name: ${HF_NAME}' >> $@
	@echo '  results:'         >> $@
	./extract-task-results.pl ${PYTORCH_MODEL}/benchmark_results.txt >> $@
	@echo '---'                >> $@
	@echo '# ${HF_NAME}'       >> $@
	@echo ''                   >> $@
	@echo '## Table of Contents'                             >> $@
	@echo '- [Model Details](#model-details)'                >> $@
	@echo '- [Uses](#uses)'                                  >> $@
	@echo '- [Risks, Limitations and Biases](#risks-limitations-and-biases)' >> $@
	@echo '- [How to Get Started With the Model](#how-to-get-started-with-the-model)' >> $@
	@echo '- [Training](#training)'                          >> $@
	@echo '- [Evaluation](#evaluation)'                      >> $@
	@echo '- [Citation Information](#citation-information)'  >> $@
	@echo '- [Acknowledgements](#acknowledgements)'          >> $@
	@echo ''                   >> $@
	@echo '## Model Details'   >> $@
	@echo ''                   >> $@
	@echo 'Neural machine translation model for translating from ${SRCLANG} (${SRCLANGID2}) to ${TRGLANG} (${TRGLANGID2}).' >> $@
	@echo ''                   >> $@
	@echo 'This model is part of the [OPUS-MT project](https://github.com/Helsinki-NLP/Opus-MT), an effort to make neural machine translation models widely available and accessible for many languages in the world. All models are originally trained using the amazing framework of [Marian NMT](https://marian-nmt.github.io/), an efficient NMT implementation written in pure C++. The models have been converted to pyTorch using the transformers library by huggingface. Training data is taken from [OPUS](https://opus.nlpl.eu/) and training pipelines use the procedures of [OPUS-MT-train](https://github.com/Helsinki-NLP/Opus-MT-train).' >> $@

	@echo '**Model Description:**'                              >> $@
	@echo '- **Developed by:** Language Technology Research Group at the University of Helsinki' >> $@
	@echo '- **Model Type:** Translation (${MODEL_TYPE})'        >> $@
#	@echo '* model: ${MODEL_TYPE} (${HF_MODELTYPE})'             >> $@
	@echo '- **Release**: ${RELEASE_DATE}'                       >> $@
	@echo '- **License:** Apache-2.0'                            >> $@
	@echo '- **Language(s):**  '                                 >> $@
	@echo '  - Source Language(s): ${MODEL_SRCLANGS}'            >> $@
	@echo '  - Target Language(s): ${MODEL_TRGLANGS}'            >> $@
#	@echo '  - Source Language(s): ${sort ${MODEL_SRCLANGS} ${SRCLANG_RELIABLE}}'  >> $@
#	@echo '  - Target Language(s): ${sort ${MODEL_TRGLANGS} ${TRGLANG_RELIABLE}}'  >> $@
#	@echo '  - Language Pair(s): ${sort ${LANGPAIR_RELIABLE}}'   >> $@
ifneq ($(words ${VOCAB_TRGLABELS}),1)
ifneq ($(words ${VOCAB_TRGLABELS}),0)
	@echo '  - Valid Target Language Labels: ${VOCAB_TRGLABELS}' >> $@
endif
else ifneq ($(words ${MODEL_VALID_TRGLABELS}),1)
ifneq ($(words ${MODEL_VALID_TRGLABELS}),0)
	@echo '  - Valid Target Language Labels: ${MODEL_VALID_TRGLABELS}' >> $@
endif
endif
	@echo '- **Original Model**: [$(notdir ${MARIAN_MODEL_URL})](${MARIAN_MODEL_URL})' >> $@
	@echo '- **Resources for more information:**'                >> $@
	@echo '  -  [OPUS-MT dashboard](${OPUS_MT_DASHBOARD_BASEURL}$(call URL_ENCODE,$(patsubst https://object.pouta.csc.fi/%.zip,%,${MARIAN_MODEL_URL})))' >>$@
	@echo '  - [OPUS-MT-train GitHub Repo](https://github.com/Helsinki-NLP/OPUS-MT-train)' >> $@
#	@echo '  - More information about released models for this language pair: [OPUS-MT ${LANGPAIR} README](${OPUSMT_README})' >> $@
	@echo "  - [More information about MarianNMT models in the transformers library](https://huggingface.co/docs/transformers/model_doc/marian)" >>$@
ifeq ($(findstring opus-mt-tc,${HF_BASENAME}),opus-mt-tc)
	@echo '  - [Tatoeba Translation Challenge](https://github.com/Helsinki-NLP/Tatoeba-Challenge/)' >> $@
endif
ifeq ($(findstring opusTCv20230926,${MARIAN_MODEL_URL}),opusTCv20230926)
	@echo '  - [HPLT bilingual data v1 (as part of the Tatoeba Translation Challenge dataset)](https://hplt-project.org/datasets/v1)' >> $@
endif
ifeq (${HF_BASENAME},opus-mt-tc-bible)
	@echo '  - [A massively parallel Bible corpus](https://aclanthology.org/L14-1215/)' >> $@
endif
ifeq (${USE_LABELS},1)
	@echo ''                                                        >> $@
	@echo 'This is a multilingual translation model with multiple target languages. A sentence initial language token is required in the form of `>>id<<` (id = valid target language ID), e.g. `>>${firstword ${MODEL_TRGLANGS}}<<`' >> $@
endif
	@echo ''                                                        >> $@
	@echo '## Uses'                                                 >> $@
	@echo ''                                                        >> $@
	@echo 'This model can be used for translation and text-to-text generation.'  >> $@
	@echo ''                                                        >> $@

	@echo '## Risks, Limitations and Biases'                        >> $@
	@echo ''                                                        >> $@
	@echo '**CONTENT WARNING: Readers should be aware that the model is trained on various public data sets that may contain content that is disturbing, offensive, and can propagate historical and current stereotypes.**'                                                          >> $@
	@echo ''                                                        >> $@
	@echo 'Significant research has explored bias and fairness issues with language models (see, e.g., [Sheng et al. (2021)](https://aclanthology.org/2021.acl-long.330.pdf) and [Bender et al. (2021)](https://dl.acm.org/doi/pdf/10.1145/3442188.3445922)).'                                                        >> $@
	@echo ''                                                        >> $@
	@echo '## How to Get Started With the Model'                    >> $@
	@echo ''                                                        >> $@
	@echo 'A short example code:'                                   >> $@
	@echo ''                                                        >> $@
	@echo '```python'                                               >> $@
	@echo 'from transformers import MarianMTModel, MarianTokenizer' >> $@
	@echo ''                                                        >> $@
	@echo 'src_text = ['                                            >> $@
	@echo "    \"${TESTSET_INPUT_EXAMPLE}\","                       >> $@
	@echo "    \"${TESTSET_INPUT2_EXAMPLE}\""                       >> $@
	@echo ']'                                                       >> $@
	@echo ''                                                        >> $@
	@echo 'model_name = "pytorch-models/${HF_NAME}"'     >> $@
	@echo 'tokenizer = MarianTokenizer.from_pretrained(model_name)' >> $@
	@echo 'model = MarianMTModel.from_pretrained(model_name)'       >> $@
	@echo 'translated = model.generate(**tokenizer(src_text, return_tensors="pt", padding=True))' >> $@
	@echo ''                                                        >> $@
	@echo 'for t in translated:'                                    >> $@
	@echo '    print( tokenizer.decode(t, skip_special_tokens=True) )' >> $@
ifdef TESTSET_OUTPUT_EXAMPLE
	@echo ''                                                        >> $@
	@echo '# expected output:'                                      >> $@
	@echo "#     ${TESTSET_OUTPUT_EXAMPLE}"                         >> $@
	@echo "#     ${TESTSET_OUTPUT2_EXAMPLE}"                        >> $@
endif
	@echo '```'                                                     >> $@
	@echo ''                                                        >> $@
	@echo 'You can also use OPUS-MT models with the transformers pipelines, for example:' >> $@
	@echo ''                                                        >> $@
	@echo '```python'                                               >> $@
	@echo 'from transformers import pipeline'                       >> $@
	@echo 'pipe = pipeline("translation", model="Helsinki-NLP/${HF_NAME}")' >> $@
	@echo "print(pipe(\"${TESTSET_INPUT_EXAMPLE}\"))"               >> $@
ifdef TESTSET_OUTPUT_EXAMPLE
	@echo ''                                                        >> $@
	@echo "# expected output: ${TESTSET_OUTPUT_EXAMPLE}"            >> $@
endif
	@echo '```'                                                     >> $@
	@echo ''                                                        >> $@
	@echo '## Training'                                             >> $@
	@echo ''                                                        >> $@
	@echo '- **Data**: ${MODEL_DATA} ([source](${DATA_SOURCE}))'    >> $@
	@echo '- **Pre-processing**: ${MODEL_TOK}'                      >> $@
	@echo '- **Model Type:**  ${MODEL_TYPE}'                        >> $@
	@echo '- **Original MarianNMT Model**: [$(notdir ${MARIAN_MODEL_URL})](${MARIAN_MODEL_URL})' >> $@
	@echo '- **Training Scripts**: [GitHub Repo](https://github.com/Helsinki-NLP/OPUS-MT-train)' >> $@
	@echo ''                                                        >> $@
	@echo '## Evaluation'                                           >> $@
	@echo ''                                                        >> $@
	@echo '* [Model scores at the OPUS-MT dashboard](${OPUS_MT_DASHBOARD_BASEURL}$(call URL_ENCODE,$(patsubst https://object.pouta.csc.fi/%.zip,%,${MARIAN_MODEL_URL})))' >>$@
	@grep 'test set translations:' ${MARIAN_MODEL}/README.md        >> $@
	@grep 'test set scores:' ${MARIAN_MODEL}/README.md              >> $@
	@echo '* benchmark results: [benchmark_results.txt](benchmark_results.txt)' >> $@
	@echo '* benchmark output: [benchmark_translations.zip](benchmark_translations.zip)' >> $@
	@echo ''                                                        >> $@
	@echo '| langpair | testset | chr-F | BLEU  | #sent | #words |' >> $@
	@echo '|----------|---------|-------|-------|-------|--------|' >> $@
	t=`cut -f2 < ${PYTORCH_MODEL}/benchmark_results.txt | grep tatoeba | sort -u | tail -1`; \
	if [ "$$t" != "" ]; then \
	  grep "$$t" ${PYTORCH_MODEL}/benchmark_results.txt |\
	  awk '{if (($$3 > 0.4 || $$4 > 20) && $$5 > 199) print}' |\
	  sed 's/	/ | /g;s/^/| /;s/$$/ |/'                        >> $@; \
	fi
	@cat ${PYTORCH_MODEL}/benchmark_results.txt | \
	grep -v 'flores101-dev	' | grep -v 'tatoeba-test' |\
	awk '{if (($$3 > 0.4 || $$4 > 20) && $$5 > 199) print}' |\
	sed 's/	/ | /g;s/^/| /;s/$$/ |/'                                >> $@
	@echo ''                                                        >> $@
	@echo '## Citation Information'                   >> $@
	@echo ''                                                        >> $@
	@echo '* Publications: ${BACKGROUND_READING} (Please, cite if you use this model.)' >> $@
	@echo ''                                                        >> $@
	@echo '```bibtex'                                               >> $@
	@echo '@article{tiedemann2023democratizing,'                    >> $@
	@echo '  title={Democratizing neural machine translation with {OPUS-MT}},' >> $@
	@echo '  author={Tiedemann, J{\"o}rg and Aulamo, Mikko and Bakshandaeva, Daria and Boggia, Michele and Gr{\"o}nroos, Stig-Arne and Nieminen, Tommi and Raganato, Alessandro and Scherrer, Yves and Vazquez, Raul and Virpioja, Sami},' >> $@
	@echo '  journal={Language Resources and Evaluation},'          >> $@
	@echo '  number={58},'                                          >> $@
	@echo '  pages={713--755},'                                     >> $@
	@echo '  year={2023},'                                          >> $@
	@echo '  publisher={Springer Nature},'                          >> $@
	@echo '  issn={1574-0218},'                                     >> $@
	@echo '  doi={10.1007/s10579-023-09704-w}'                      >> $@
	@echo '}'                                                       >> $@
	@echo ''                                                        >> $@
	@echo '@inproceedings{tiedemann-thottingal-2020-opus,'          >> $@
	@echo '    title = "{OPUS}-{MT} {--} Building open translation services for the World",' >> $@
	@echo '    author = {Tiedemann, J{\"o}rg  and Thottingal, Santhosh},' >> $@
	@echo '    booktitle = "Proceedings of the 22nd Annual Conference of the European Association for Machine Translation",' >> $@
	@echo '    month = nov,'                                        >> $@
	@echo '    year = "2020",'                                      >> $@
	@echo '    address = "Lisboa, Portugal",'                       >> $@
	@echo '    publisher = "European Association for Machine Translation",' >> $@
	@echo '    url = "https://aclanthology.org/2020.eamt-1.61",'    >> $@
	@echo '    pages = "479--480",'                                 >> $@
	@echo '}'                                                       >> $@
ifeq ($(findstring opus-mt-tc,${HF_BASENAME}),opus-mt-tc)
	@echo ''                                                        >> $@
	@echo '@inproceedings{tiedemann-2020-tatoeba,'                  >> $@
	@echo '    title = "The Tatoeba Translation Challenge {--} Realistic Data Sets for Low Resource and Multilingual {MT}",' >> $@
	@echo '    author = {Tiedemann, J{\"o}rg},'                     >> $@
	@echo '    booktitle = "Proceedings of the Fifth Conference on Machine Translation",' >> $@
	@echo '    month = nov,'                                        >> $@
	@echo '    year = "2020",'                                      >> $@
	@echo '    address = "Online",'                                 >> $@
	@echo '    publisher = "Association for Computational Linguistics",' >> $@
	@echo '    url = "https://aclanthology.org/2020.wmt-1.139",'    >> $@
	@echo '    pages = "1174--1182",'                               >> $@
	@echo '}'                                                       >> $@
endif
	@echo '```'                                                     >> $@
	@echo ''                                                        >> $@
	@echo '## Acknowledgements'                                     >> $@
	@echo ''                                                        >> $@
	@echo 'The work is supported by the [HPLT project](https://hplt-project.org/), funded by the European Union’s Horizon Europe research and innovation programme under grant agreement No 101070350. We are also grateful for the generous computational resources and IT infrastructure provided by [CSC -- IT Center for Science](https://www.csc.fi/), Finland, and the [EuroHPC supercomputer LUMI](https://www.lumi-supercomputer.eu/).' >> $@
	@echo ''                                                        >> $@
	@echo '## Model conversion info'                                >> $@
	@echo ''                                                        >> $@
	@echo '* transformers version: ${shell echo "import transformers#print(transformers.__version__)" | tr '#' "\n" | python3}' >> $@
	@echo '* OPUS-MT git hash: ${shell git rev-parse --short HEAD}' >> $@
	@echo '* port time: ${shell date}'                              >> $@
	@echo '* port machine: ${shell hostname}'                       >> $@


