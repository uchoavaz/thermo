
FROM ubuntu:16.04

WORKDIR /var/www

RUN apt-get update
RUN apt install libpq-dev python-dev -y
RUN apt-get -y install python-pip
RUN apt-get install python-dev -y
RUN apt-get install git-all -y
RUN apt-get install wget -y
RUN mkdir /rancher \
	&& wget https://github.com/rancher/cli/releases/download/v0.6.1rancher-linux-amd64-v0.6.1.tar.gz -P /rancher \
	&& tar -zxvf /rancher/rancher-linux-amd64-v0.6.1.tar.gz -C /rancher \
    && mv /rancher/rancher-v0.6.1/rancher /usr/bin/rancher \
	&& rm -rf /rancher


WORKDIR /var/www
