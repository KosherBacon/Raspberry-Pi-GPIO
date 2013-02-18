Raspberry Pi Remote GPIO
====
Remote control your Raspberry Pi's GPIO from an Android application.

## How to Install

* All instructions assume you are using a version of Debian.
* I am working on an all in one .sh script to install and setup the program.
* These instructions assume some technical know-how, if you do not meet this requirement, it may be difficult to setup.

Firstly you will need python.
```bash
sudo apt-get install python2.7
```

You will need to install the GPIO library module with python.
You will also need the feedparser module and python-crypto module.
```bash
sudo apt-get install python-pip
sudo pip install RPi.GPIO
```

I am using the wiringPi library, I recommend using the provided instructions.
The following methods are provided on the library's website.
wiringPi website: https://projects.drogon.net/raspberry-pi/wiringpi/download-and-install/

Git:
```bash
sudo apt-get install git-core
sudo apt-get update
sudo apt-get upgrade
git clone git://git.drogon.net/wiringPi
cd wiringPi
./build
```

Move the files into the correct directories:
```bash
sudo mv RemotePi_2/ /usr/bin/
```

Now you need to give remoteGPIO.sh and remoteGPIOstart.sh the ability to be executed.
```bash
cd /usr/bin/RemotePi_2/
sudo chmod +x remotePi.py
sudo chmod 777 remotePi.py
```

## Start Using

Now that the server side is set up as a Linux command, we can now start using the it.

Check to make sure that all of the setup was done correctly:
```bash
cd /usr/bin/RemotePi_2/; sudo python remotePi.py info
```
If you received a long odd looking string, good, it means the program is working!

I have written an app for Android that I will be releasing to the Play Store soon.
I encourage everyone to write their own method that is compatible with the backend of this application.

## Upcoming Updates / Work in Progress

I am working on a more efficient method of accessing the server from a device. I plan on utilizing ssh instead of my current method.
This allows for the system to be more efficient, and eliminates some setup steps for a better user experience.
