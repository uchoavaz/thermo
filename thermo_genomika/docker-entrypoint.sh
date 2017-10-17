#!/bin/bash

echo "America/Recife" > /etc/timezone
dpkg-reconfigure -f noninteractive tzdata

/usr/sbin/sshd -D &!

if [ ! -d "/var/www/thermo-gnmk/thermo_genomika" ]; then
  git clone git@gitlab.com:genomika/thermo-gnmk.git
fi
cd /var/www/thermo-gnmk/thermo_genomika
git checkout $thermo_gnmk_branch
make clean

if [ "$makemig" = true ] ; then
        python manage.py makemigrations
fi

if [ "$migrate" = true ] ; then
        python manage.py migrate
fi
python manage.py runserver 0.0.0.0:$port