#!/usr/bin/env bash

set -e
PROJECT_ROOT="usr/sbin/remote_gpio"

mkdir -p "$PROJECT_ROOT"
cd "$PROJECT_ROOT"

echo "**** Downloading the latest version of the server side ****"
curl -L https://github.com/downloads/arcen1k/Raspberry-Pi-GPIO/server.tar.gz | tar xzf -

echo "**** Installing required libraries ****"
echo "**** (python-pip, RPi.GPIO, feedparser, python-crypto) ****"

apt-get update
apt-get install python-pip, python-crypto -y
pip install RPi.GPIO, feedparser

mv remoteGPIO.sh /etc/init.d

echo "**** Adding server as a service ****"

update-rc.d remoteGPIO.sh defaults

echo "**** Force starting service ****"

service remoteGPIO.sh start
