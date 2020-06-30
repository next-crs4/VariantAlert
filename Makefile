DEFAULT_VARIANT_ALERT_ROOT=~/variant-alert
DUMMY_EMAIL_HOST=smtp.yourserver.com
DUMMY_EMAIL_USER=your@yourserver.com
DUMMY_EMAIL_PASSWORD=your-email-account-password
DUMMY_EMAIL_PORT=587
DUMMY_HOST=0.0.0.0

UNAME_S := $(shell uname -s)

USERID=$(shell id -u)

ifeq ($(UNAME_S), Darwin)
GROUPID=1000
else
GROUPID=$(shell id -g)
endif

ifndef VARIANT_ALERT_ROOT
override VARIANT_ALERT_ROOT = ${DEFAULT_VARIANT_ALERT_ROOT}
endif
ifndef HOST
override HOST = ${DUMMY_HOST}
endif
ifndef EMAIL_HOST
override EMAIL_HOST = ${DUMMY_EMAIL_HOST}
endif
ifndef EMAIL_USER
override EMAIL_USER = ${DUMMY_EMAIL_USER}
endif
ifndef EMAIL_PASSWORD
override EMAIL_PASSWORD = ${DUMMY_EMAIL_PASSWORD}
endif
ifndef EMAIL_PORT
override EMAIL_PORT = ${DUMMY_EMAIL_PORT}
endif

help:
	@echo "Please use \`make <target>\` where <target> is one of"
	@echo "  start                   bring up the variant-alert app"
	@echo "  stop                    bring down the variant-alert app"
	@echo "  clean                   remove the variant-alert app from your computer"
	@echo "  "
	@echo "  variant-alert will be deployed into ${DEFAULT_VARIANT_ALERT_ROOT}"
	@echo "  To set a different path, digit: "
	@echo "  make VARIANT_ALERT_ROOT=/your/path <target>"
	@echo "  "
	@echo "  Remember to configure your EMAIL_HOST: "
	@echo "  make EMAIL_HOST=${DUMMY_EMAIL_HOST} EMAIL_HOST_USER=${DUMMY_EMAIL_USER} EMAIL_HOST_PASSWORD=${DUMMY_EMAIL_PASSWORD} EMAIL_PORT=${DUMMY_PORT} HOST=${DUMMY_HOST} start"


init:
	mkdir -p ${VARIANT_ALERT_ROOT}/postgres-data 
	crontab ./scripts/cron-query
	sed -i -e 's|${DUMMY_EMAIL_HOST}|${EMAIL_HOST}|g;' src/variant_alert/settings.py
	sed -i -e 's|${DUMMY_EMAIL_USER}|${EMAIL_USER}|g;' src/variant_alert/settings.py
	sed -i -e 's|${DUMMY_EMAIL_PASSWORD}|${EMAIL_PASSWORD}|g;' src/variant_alert/settings.py
	sed -i -e 's|${DUMMY_EMAIL_PORT}|${EMAIL_PORT}|g;' src/variant_alert/settings.py

init-local: init
	sed -i -e 's|${DEFAULT_VARIANT_ALERT_ROOT}|${VARIANT_ALERT_ROOT}|g;' docker-compose.local.yml

init-prod: init
	sed -i -e 's|${DEFAULT_VARIANT_ALERT_ROOT}|${VARIANT_ALERT_ROOT}|g;' docker-compose.prod.yml
	sed -i -e 's|${DUMMY_HOST}|${HOST}|g;' src/variant_alert/settings.py
	sed -i -e 's|info@example.com|${EMAIL_USER}|g;' init-letsencrypt.sh
	sed -i -e 's|example.com|${HOST}|g;' init-letsencrypt.sh
	sed -i -e 's|example.com|${HOST}|g;' config/nginx/prod/variant-alert.conf
	chmod +x init-letsencrypt.sh

start-local: init-local
	docker-compose -f docker-compose.local.yml build --build-arg USER_ID=${USERID} --build-arg GROUP_ID=${GROUPID}
	docker-compose -f docker-compose.local.yml up -d
	@echo "Point your browser to: http://${HOST}:8000"

start-prod: init-prod
	docker-compose -f docker-compose.prod.yml build --build-arg USER_ID=${USERID} --build-arg GROUP_ID=${GROUPID}
	./init-letsencrypt.sh
	docker-compose -f docker-compose.prod.yml up -d
	@echo "Point your browser to: https://${HOST}"

stop:
	docker-compose -f docker-compose.prod.yml down

clean: stop
	docker rmi variantalert_web:latest
	docker rmi postgres:latest
	docker rmi nginx:latest
	docker rmi certbot/certbot

