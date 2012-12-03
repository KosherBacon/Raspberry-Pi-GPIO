Raspberry Pi Remote GPIO
====
Remote control your Raspberry Pi's GPIO from an Android application.

## How to Install

* All instructions assume you are using a version of Debian.
* I am working on an all in one .sh script to install and setup the program.

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

Move the files into the correct directories:
```bash
sudo mv remoteGPIO.sh /etc/init.d/
sudo mv remoteGPIOstart.sh /usr/sbin/
sudo mv stored_values.ini /usr/sbin/
sudo mv gpio_server.py /usr/sbin/
```

Now you need to give remoteGPIO.sh and remoteGPIOstart.sh the ability to be executed.
```bash
sudo chmod +x remoteGPIO.sh
sudo chmod +x remoteGPIOstart.sh
```

Add remoteGPIO.sh as a service.
```bash
sudo update-rc.d remoteGPIO.sh defaults
```

Make sure it is running.
```bash
sudo service remoteGPIO.sh start
```

## Start Using

Now that the server side is set up as a Linux service, we can now start using the it.
If the service is not on already, start it now by running the command:
```bash
sudo service remoteGPIO.sh start
```

I have written an app for Android that I will be releasing to the Play Store soon.
I encourage everyone to write their own method that is compatible with the backend of this application.

## Upcoming Updates / Work in Progress

I am working on a more efficient method of accessing the server from a device. I plan on utilizing ssh instead of my current method.
This allows for for the system to be more efficient, and eliminates some setup steps for a better user experience.
