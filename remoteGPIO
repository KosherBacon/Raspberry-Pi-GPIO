#!/bin/sh
# Execute the actual python script 
# The "$@" passes in any parameters into the python exectuable 
# The '&' puts the process into background (as a daemon) 
# The 'echo $! > mydaemon.pid'  write the process id to a file

python /usr/sbin/gpio_server.py "$@" &
echo $! > /usr/sbin/remoteGPIO.pid
