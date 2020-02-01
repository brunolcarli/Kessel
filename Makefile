migrate:
	python manage.py makemigrations --settings=kessel.settings.common
	python manage.py migrate --settings=kessel.settings.common


run:
	python manage.py runserver --settings=kessel.settings.common
