PIP=venv/bin/pip
MANAGE=venv/bin/python manage.py

setup: venv frigg/settings/local.py
	${PIP} install -r requirements/dev.txt
	${MANAGE} migrate

run:
	${MANAGE} runserver 0.0.0.0:8000

production: venv frigg/settings/local.py
	${PIP} install -r requirements/prod.txt
	${MANAGE} migrate
	bower install
	cp ../frigg-frontend/public/bundle.js frigg/files/react-version.js
	cp ../frigg-frontend/public/main.css frigg/files/react-version.css
	${MANAGE} collectstatic --noinput
	sudo supervisorctl restart frigg-hq
	sudo supervisorctl restart frigg-hq-webhook-fetcher
	${MANAGE} post_deploy

deploy:
	${PIP} install -r requirements/prod.txt
	${MANAGE} migrate
	bower install
	${MANAGE} collectstatic --noinput
	sudo supervisorctl restart frigg-hq
	sudo supervisorctl restart frigg-hq-webhook-fetcher
	${MANAGE} post_deploy

clean:
	find . -name "*.pyc" -exec rm -rf {} \;

venv:
	virtualenv venv -p `which python3`

load_prod_data:
	scp web@ron.frigg.io:prod-hourly-dump.json .
	python manage.py loaddata prod-hourly-dump.json
	rm hourly-dump.json

frigg/settings/local.py:
	cp frigg/settings/local_dummy.py frigg/settings/local.py

.PHONY: setup run clean production
