migrate:
	python3 manage.py makemigrations --settings=kessel.settings.development
	python3 manage.py migrate --settings=kessel.settings.development


run:
	python3 manage.py runserver --settings=kessel.settings.development
