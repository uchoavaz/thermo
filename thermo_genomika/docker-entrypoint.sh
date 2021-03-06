#!/bin/bash

echo "America/Recife" > /etc/timezone
dpkg-reconfigure -f noninteractive tzdata

cd /var/www

if [ "$settings" = prod ]; then
	cd /var/www/thermo-gnmk/thermo_genomika
	git checkout $thermo_gnmk_branch
	make clean
	pip install -r requirements.txt

	if [ "$makemig" = true ] ; then
	        python manage.py makemigrations
	fi

	if [ "$migrate" = true ] ; then
	        python manage.py migrate
	fi

	celery -A thermo_genomika worker --loglevel=info --beat >> /logs/celery_beat.log 2>&1 &!
else
	pip install -r requirements.txt
	make clean
fi

python manage.py runserver 0.0.0.0:$port