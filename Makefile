DEFAULT_VARIANT_ALERT_ROOT=~/variant-alert
DEFAULT_EMAIL_HOST=smtp.yourserver.com
DEFAULT_EMAIL_USER=your@yourserver.com
DEFAULT_EMAIL_PASSWORD=your-email-account-password
DEFAULT_EMAIL_PORT=587
DEFAULT_HOST=0.0.0.0

UNAME_S := $(shell uname -s)
USERID=$(shell id -u)
BRIDGE:=$(shell docker network ls | grep br01)

ifeq ($(UNAME_S), Darwin)
GROUPID=1000
else
GROUPID=$(shell id -g)
endif

ifndef VARIANT_ALERT_ROOT
override VARIANT_ALERT_ROOT = ${DEFAULT_VARIANT_ALERT_ROOT}
endif
ifndef HOST
override HOST = ${DEFAULT_HOST}
endif
ifndef EMAIL_HOST
override EMAIL_HOST = ${DEFAULT_EMAIL_HOST}
endif
ifndef EMAIL_USER
override EMAIL_USER = ${DEFAULT_EMAIL_USER}
endif
ifndef EMAIL_PASSWORD
override EMAIL_PASSWORD = ${DEFAULT_EMAIL_PASSWORD}
endif
ifndef EMAIL_PORT
override EMAIL_PORT = ${DEFAULT_EMAIL_PORT}
endif

help:
	@echo "VariantAlert - a tool to notify updates in genetic variant annotations"
	@echo "https://github.com/next-crs4/VariantAlert"
	@echo " "
	@echo "Please use \`make [optiosn] <target>\` where <target> is one of"
	@echo "  start-local             bring up the variant-alert app in your local/develop environment (0.0.0.0)"
	@echo "  start-prod              bring up the variant-alert app in production environment (with ssl)"
	@echo "  stop                    bring down the variant-alert app"
	@echo "  clean                   remove the variant-alert app from your computer"
	@echo "  "
	@echo "variant-alert will be deployed into ${DEFAULT_VARIANT_ALERT_ROOT}"
	@echo "To set a different path, digit: "
	@echo "  make VARIANT_ALERT_ROOT=/your/path [options] start-*"
	@echo "  "
	@echo "Remember to configure your EMAIL_HOST: "
	@echo "  make \t EMAIL_HOST=${DEFAULT_EMAIL_HOST} \\"
	@echo "\t EMAIL_USER=${DEFAULT_EMAIL_USER} \\"
	@echo "\t EMAIL_PASSWORD=${DEFAULT_EMAIL_PASSWORD} [options] start-*"
	@echo "  "
	@echo "For production environment, configure HOST"
	@echo "  make HOST=example.com [options] start-*"
	@echo " "
	@echo "Docs: https://github.com/next-crs4/VariantAlert/blob/master/README.md"
	@echo " "

init:
	mkdir -p ${VARIANT_ALERT_ROOT}/postgres-data
	crontab ./scripts/cron-query
	sed -i -e 's|${DEFAULT_EMAIL_HOST}|${EMAIL_HOST}|g;' src/variant_alert/settings.py
	sed -i -e 's|${DEFAULT_EMAIL_USER}|${EMAIL_USER}|g;' src/variant_alert/settings.py
	sed -i -e 's|${DEFAULT_EMAIL_PASSWORD}|${EMAIL_PASSWORD}|g;' src/variant_alert/settings.py
	sed -i -e 's|${DEFAULT_EMAIL_PORT}|${EMAIL_PORT}|g;' src/variant_alert/settings.py

init-local: init
	sed -i -e 's|${DEFAULT_VARIANT_ALERT_ROOT}|${VARIANT_ALERT_ROOT}|g;' docker-compose.local.yml

init-prod: init
	sed -i -e 's|${DEFAULT_VARIANT_ALERT_ROOT}|${VARIANT_ALERT_ROOT}|g;' docker-compose.prod.yml
	sed -i -e 's|${DEFAULT_HOST}|${HOST}|g;' src/variant_alert/settings.py

start-local: init-local
	docker-compose -f docker-compose.local.yml build --build-arg USER_ID=${USERID} --build-arg GROUP_ID=${GROUPID}
	docker-compose -f docker-compose.local.yml up -d
	@echo "Point your browser to: http://${HOST}:8000"

start-prod: init-prod
	docker-compose -f docker-compose.prod.yml build --build-arg USER_ID=${USERID} --build-arg GROUP_ID=${GROUPID}
	docker-compose -f docker-compose.prod.yml up -d
	@echo "Point your browser to: https://${HOST}"

stop:
	docker-compose -f docker-compose.prod.yml down

clean: stop
	docker rmi variantalert_web:latest
	docker rmi postgres:latest
	docker rmi nginx:latest
