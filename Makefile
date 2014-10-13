PIP=venv/bin/pip
MANAGE=venv/bin/python manage.py

setup: venv frigg/settings/local.py fab_local.py
	${PIP} install -r requirements/dev.txt
	${MANAGE} migrate

run:
	${MANAGE} runserver 0.0.0.0:8000

production: venv
	echo "from frigg.settings.production import *" > frigg/settings/local.py
	${PIP} install -r requirements/prod.txt
	${MANAGE} migrate
	${MANAGE} collectstatic --noinput

venv:
	virtualenv venv

frigg/settings/local.py:
	touch frigg/settings/local.py

fab_local.py:
	@echo "We need to set up the fab scripts..."; \
	 echo "settings = {" > fab_local.py; \
	 echo "What user do you login with to deploy?"; \
	 read user; \
	 echo "    'USER': '$$user'," >> fab_local.py; \
	 echo "..and on which host?"; \
	 read host; \
	 echo "    'HOST': '$$host'," >> fab_local.py; \
	 echo "..and what is the path to the project?"; \
	 read path; \
	 echo "    'PROJECT_PATHS': {'prod': '$$path'}," >> fab_local.py; \
	 echo "..and what is the restart command for the app server?"; \
	 read restart_command; \
	 echo "    'RESTART_COMMAND': {'prod': '$$restart_command'}," >> fab_local.py; \
	 echo "..and what is the the url used to reach the project?"; \
	 read url; \
	 echo "    'URL': {'prod': '$$url/accounts/login/'}," >> fab_local.py; \
	 echo "}" >> fab_local.py
	@echo "\nYou can now deploy with fab deploy:prod"

.PHONY: setup run
