PIP=venv/bin/pip
MANAGE=venv/bin/python manage.py

setup: venv frigg/settings/local.py
	${PIP} install -r requirements.txt
	${MANAGE} syncdb --migrate
	${MANAGE} collectstatic --noinput

run:
	${MANAGE} runserver 0.0.0.0:8000

venv:
	virtualenv venv

frigg/settings/local.py:
	touch frigg/settings/local.py

.PHONY: setup run
