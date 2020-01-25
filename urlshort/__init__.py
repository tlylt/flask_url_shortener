from flask import Flask
# enter env by pipenv shell, out by exit
# 1. initializing: set FLASK_APP=hello
# 2. set FLASK_ENV=development
# 3. flask run
# renamed to app.py and it will be the default app to run without step 1
def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key = 'randomstringforpassingflash'

    from . import urlshort
    app.register_blueprint(urlshort.bp)

    return app