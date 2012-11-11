Raspberry Pi Remote GPIO
====
Remote control your Raspberry Pi's GPIO from an Android application.

## How to Install

Firstly you will need python.
```bash
sudo apt-get install python2.7
```

You will need to install the GPIO library module with python.
You will also need the feedparser module and python-crypto module.
```bash
sudo apt-get install python-pip
sudo pip install RPi.GPIO
sudo pip install feedparser
sudo apt-get install python-crypto
```

## Start Using

Now that the server side is set up as a Linux service, we can now start using the it.
If the service is not on already, start it now by running the command:
```bash
sudo service remoteGPIO.sh start
```