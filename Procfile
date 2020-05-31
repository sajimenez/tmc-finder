release: python src/manage.py migrate; python src/manage.py compilemessages
web: gunicorn --chdir src TmcFinder.wsgi
