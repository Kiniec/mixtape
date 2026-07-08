## python env setup
python3 -m venv venv
source venv/bin/activate
deactivate

## check env
git ls-files .env
git rm --cached .env

## git ignore

# Virtual environments
.venv/
venv/
ENV/
env/

# Python cache files
__pycache__/
*.pyc


## to start this app
FLASK_APP=app:create_app flask run
