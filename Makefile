migrate:
	python3 manage.py makemigrations --settings=kessel.settings.common
	python3 manage.py migrate --settings=kessel.settings.common


run:
	python3 manage.py runserver --settings=kessel.settings.common
