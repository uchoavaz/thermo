
FROM dockerregistry.genomika.com/ubuntu-genomika:14.04

WORKDIR /var/www

RUN apt install libpq-dev python-dev -y
RUN apt-get -y install python-pip
RUN apt-get install python-dev -y
RUN pip install gunicorn
RUN git clone git@gitlab.com:genomika/thermo-gnmk.git

WORKDIR thermo-gnmk/thermo_genomika

RUN pip install -r requirements.txt
WORKDIR /var/www
RUN rm -rf thermo-gnmk
