import RPi.GPIO as GPIO
import sys, re, socket, ConfigParser
from Crypto.Cipher import AES

USERNAME = "username"
PASSWORD = "password"
MAXLINE = 100

# GPIO Pin Class
class GPIO_PIN(object):
    def __init__(self, status = None, name = None, num = None):
        self.status = status
        self.name = name
        self.num = num
    def enable(self, pos):
        GPIO.setup(pos, GPIO.OUT)
        GPIO.output(pos, True)
        pins[pos].status = True
        parser.set('pin' + str(pos), 'status', 'True')
        saveConfig()
    def disable(self, pos):
        GPIO.setup(pos, GPIO.OUT)
        GPIO.output(pos, False)
        pins[pos].status = False
        parser.set('pin' + str(pos), 'status', 'False')
        saveConfig()
# End GPIO Class

def linesplit(sock, maxline=0):
    buf = sock.recv(16)
    done = False
    while not done:
        # mid line check
        if maxline and len(buf) > maxline:
            yield buf, True
        if "\n" in buf:
            (line, buf) = buf.split("\n", 1)
            err = maxline and len(line) > maxline
            yield line+"\n", err
        else:
            more = sock.recv(16)
            if not more:
                done = True
            else:
                buf = buf+more
    if buf:
        err = maxline and len(buf) > maxline
        yield buf, err

# Decrypt String Method
def decrypted(temp):
    orig = ""
    for code in re.findall('..', temp):
        orig += chr(int(code, 16))
        obj = AES.new('0123456789abcdef', AES.MODE_CBC, IV="fedcba9876543210")
    return obj.decrypt(orig).strip()
# End Decrypt String Method

# Save Config Method
def saveConfig():
    with open('/usr/sbin/raspberryGPIO/stored_values.ini', 'w') as configfile:
        parser.write(configfile)
# End Save Config Method

# Setting GPIO Up
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# End Setting GPIO Up

# Setting Up Array
length = 28
pins = [None] * length
for index in range(len(pins)):
    pins[index] = GPIO_PIN(False, str(index))
# End Setting Up Array

# On Startup
parser = ConfigParser.SafeConfigParser()
parser.read('/usr/sbin/rasbperryGPIO/stored_values.ini')
counter = 1
# Restore previous pin values
while counter < len(pins):
    status = parser.get('pin' + str(counter), 'status')
    name = parser.get('pin' + str(counter), 'name')
    GPIO.setup(counter, GPIO.OUT)
    # Use pin status to change output
    GPIO.output(counter, False if status == "False" else True)
    pins[counter].status = status
    pins[counter].name = name
    counter += 1
# End On Startup

# Socket Handler
HOST = ''
PORT = 9001
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(1)
while True:
    conn, addr = s.accept()
    #print 'Connected device at', addr
    # Default authorization to False
    auth = False
    for line, err in linesplit(conn, MAXLINE):
        try:
            temp = line.strip()
            bytes = temp.split(";")
            cmd = bytes[0]
            # Checks first sent line to see if authorized
            if cmd == "auth":
                login = decrypted(bytes[1]) + ";" + decrypted(bytes[2])
                if login == USERNAME + ";" + PASSWORD:
                    auth = True
            # Once authorized, proceed
            elif auth:
                try:
                    num = int(bytes[1])
                except:
                    pass
                # If command = enable
                if cmd == "enable":
                    pins[num].enable(num)
                    #print num, pins[num].status
                    passed = True
                    #print "Enabled " + bytes[1]
                # If command = disable
                elif cmd == "disable":
                    if not num == 6:
			 pins[num].disable(num)
                    #print num, pins[num].status
                    passed = True
                    #print "Disabled " + bytes[1]
                # If command = name
                elif cmd == "name":
                    pins[num].name = bytes[2]
                    #print "Name " + str(num) + " = " + pins[num].name
                    parser.set('pin' + str(num), 'Name', bytes[2])
                    saveConfig()
                # Send data to device
                elif cmd == "currentPins":
                    # Send data pin by pin
                    temp = ""
                    counter = 1
                    # Itterate through all of the pins and compile a string to send
                    while counter < len(pins):
                        strToSend = str(counter) + ";" + str(pins[counter].status) + ';' + str(pins[counter].name)
                        # Don't at string to split if it is the last one, simplifies Java code
                        if counter == len(pins) - 1:
                            temp += strToSend
                        else:
                            temp += strToSend + "%^%"
                        counter += 1
                    #print temp
                    # Send compiled string of pin data
                    conn.send(temp + "\n")
            # Allow for pinging of device
            elif cmd == "youAlive?":
				# Respond when pinged
				conn.sent("yeahBruh!")
        except:
            print "Unexpected error:", sys.exc_info()
            passed = False
            pass
conn.close()
