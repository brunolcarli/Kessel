# Local Settigns
install_local:
	pip3 install -r kessel/requirements/development.txt

migrate:
	python3 manage.py makemigrations --settings=kessel.settings.common
	python3 manage.py migrate --settings=kessel.settings.common

local:
	python3 manage.py runserver 0.0.0.0:5666 --settings=kessel.settings.common

# Docker dev
docker_dev:
	docker-compose -f docker-compose-dev.yml build
	docker-compose -f docker-compose-dev.yml up

# Docker prod
docker:
	docker-compose build
	docker-compose up
