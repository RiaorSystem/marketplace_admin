set -o errexit 

pip install -r requirements.txt 

python django_app/manage.py migrate

python django_app/manage.py collectstatic --noinput