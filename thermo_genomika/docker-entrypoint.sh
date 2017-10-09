#!/bin/bash

echo "America/Recife" > /etc/timezone
dpkg-reconfigure -f noninteractive tzdata

/usr/sbin/sshd -D &!

git checkout $thermo_gnmk_branch

make clean

if [ "$makemig" = true ] ; then
        python manage.py makemigrations
fi

if [ "$migrate" = true ] ; then
        python manage.py migrate
fi
python manage.py runserver 0.0.0.0:$port