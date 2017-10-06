
#!/bin/bash

echo "America/Recife" > /etc/timezone
dpkg-reconfigure -f noninteractive tzdata

/usr/sbin/sshd -D &!
cd /var/www

git clone git@gitlab.com:genomika/thermo-gnmk.git
cd thermo-gnmk
git checkout $thermo_gnmk_branch
cd thermo_genomika

make clean

if [ "makemig" = true ] ; then
        python manage.py makemigrations
fi

if [ "$migrate" = true ] ; then
        python manage.py migrate
fi
python manage.py runserver 0.0.0.0:$port