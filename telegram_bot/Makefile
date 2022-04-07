
## installation tools
INSTALL = install -c
INSTALL_BIN = ${INSTALL} -m 755
INSTALL_DATA = ${INSTALL} -m 644

## installation destinations
PREFIX   = /usr/local
BINDIR   = ${PREFIX}/bin
SHAREDIR = ${PREFIX}/share
CACHEDIR = /var/cache
LOGDIR   = /var/log

OPUSMT_TELEGRAM_BOT_DIR   = ${BINDIR}/opusMT_telegram_bot
OPUSMT_TELEGRAM_BOT       = ${OPUSMT_TELEGRAM_BOT_DIR}/translator_bot.py
OPUSMT_TELEGRAMBOT_TOKEN ?= ${TOKEN}

all: /etc/init.d/opusmt_telegram_bot


## make sure that the TELEGRAMBOT_TOKEN variable is set

ifdef OPUSMT_TELEGRAMBOT_TOKEN
${OPUSMT_TELEGRAM_BOT}: translator_bot.py
	mkdir -p ${dir $@}
	pip install -r requirements.txt
	sed 's#^TOKEN =.*$$#TOKEN = "${OPUSMT_TELEGRAMBOT_TOKEN}"#' < $< > $@
	chmod +x $@
	rsync -zav filters handlers keyboards.py logger.py states.py ${OPUSMT_TELEGRAM_BOT_DIR}/
	mkdir -p ${dir $@}logs


## opusMT service via sysvinit
/etc/init.d/opusmt_telegram_bot: ${OPUSMT_TELEGRAM_BOT} ../service-template
	sed 	-e 's#%%SERVICENAME%%#opusMT_Telegram_translation_bot#' \
		-e 's#%%APPSHORTDESCR%%#opusMT_telegram_bot#' \
		-e 's#%%APPLONGDESCR%%#translation bot for Telegram#' \
		-e 's#%%APPBIN%%#$<#' \
		-e 's#%%APPARGS%%##' \
	< ../service-template > ${notdir $@}
	${INSTALL_BIN} ${notdir $@} $@
	rm -f ${notdir $@}
	update-rc.d ${notdir $@} defaults 80
	rm -f ${notdir $@}
	service ${notdir $@} restart
endif
