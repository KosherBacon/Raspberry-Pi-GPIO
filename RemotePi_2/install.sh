#!/bin/bash

set -e
PROJECT_ROOT="usr/bin/RemotePi_2"

mkdir -p "$PROJECT_ROOT"
cd "$PROJECT_ROOT"

echo "**** Downloading the latest server side version ****"
curl -L https://github.com/arcen1k/Raspberry-Pi-GPIO/blob/master/RemotePi_2/RemotePi_2.tar.gz?raw=true | tar xzf -

echo "**** Installing the required libraries ****"
echo "**** (wiringPi, git) ****"

apt-get update
apt-get install git -y

cd ~/
mkdir Git
cd ~/Git
git clone git://git.drogon.net/wiringPi
cd wiringPi
./build

cd /usr/bin/RemotePi_2; python remotePi.py reset

echo "**** Finished installing ****"
