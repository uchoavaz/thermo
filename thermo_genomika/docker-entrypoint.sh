#!/bin/bash

echo "America/Recife" > /etc/timezone
dpkg-reconfigure -f noninteractive tzdata

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
python manage.py runserver 0.0.0.0:$port