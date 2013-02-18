# Imports
import RPi.GPIO as GPIO
import sys, re, ConfigParser
import subprocess as sp
# End Imports

version = "1.0.0"

# Save Config Method
def saveConfig():
    with open('stored_values.ini', 'w') as configfile:
        parser.write(configfile)
# End Save Config Method

# Run Command Method
def runCommand(command):
	p = sp.Popen(['/bin/bash', '-c', command], stdin = sp.PIPE, stdout = sp.PIPE, close_fds = True)
	(stdout, stdin) = (p.stdout, p.stdin)
	data = stdout.readline()
	valz = parser.sections()
	out = ""
	while data:
		out += data
		data = stdout.readline()
	stdout.close()
	stdin.close()
	return out
# End Command Method

# Setup ConfigParser
parser = ConfigParser.ConfigParser()
parser.read('stored_values.ini')

# Contains Digits Method
def containsDigits(d):
	_digits = re.compile('\d')
	return bool(_digits.search(d))
# End Contains Digits Method

# Setting GPIO Up
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# End Setting GPIO Up

# Make sure only available IO pins can be used
def update():
	need_save = False
	p = sp.Popen(['/bin/bash', '-c', "gpio readall"], stdin = sp.PIPE, stdout = sp.PIPE, close_fds = True)
	(stdout, stdin) = (p.stdout, p.stdin)
	data = stdout.readline()
	valz = parser.sections()
	while data:
		if containsDigits(data) and "GPIO" in data:
			values = data[1:].split("|")
			for i, f in enumerate(values):
				values[i] = values[i].strip()
				#print values[i]
			if not parser.has_section(values[1]):
				parser.add_section(values[1])
				parser.set(values[1], 'name', values[2])
				parser.set(values[1], 'status', "True" if values[3] == "High" else "False")
				need_save = True
				#saveConfig()
			#for w in values:
				#print w.strip()
			for i, f in enumerate(valz):
				if values[1] == f:
					del valz[i]
		data = stdout.readline()
	stdout.close()
	stdin.close()
	for f in valz:
		parser.remove_section(f)
		need_save = True
	if need_save:
		saveConfig()
# End I/O pin check

# Run Update
if sys.argv[1] != "version":
	update()
# End Run Update

# Reset Method
def reset():
	temp = parser.sections()
	for f in temp:
		parser.remove_section(f)
	update()
# End Reset Method

# Check all store_value entries
# Make sure that each one has both data points
need_save = False
for i, f in enumerate(parser.sections()):
	if len(parser.options(f)) < 2:
		if parser.options(f)[0] == "name":
			temp = runCommand("gpio -g read " + f)
			parser.set(f, "status", "False" if temp != "0" else "True")
			need_save = True
		else:
			parser.set(f, "name", "Change")
			need_save = True
if need_save:
	saveConfig()
# End data point check
	
# Make sure there are enough arguements
# Perform Input
if len(sys.argv) > 1:
	if sys.argv[1] == "enable" and sys.argv[2].isdigit():
		GPIO.setup(int(sys.argv[2]), GPIO.OUT)
		GPIO.output(int(sys.argv[2]), True)
		parser.set(sys.argv[2], "status", "True")
		saveConfig()
	elif sys.argv[1] == "disable" and sys.argv[2].isdigit():
		GPIO.setup(int(sys.argv[2]), GPIO.OUT)
		GPIO.output(int(sys.argv[2]), False)
		parser.set(sys.argv[2], "status", "False")
		saveConfig()
	elif sys.argv[1] == "name" and sys.argv[2].isdigit() and sys.argv[3]:
		i = 3
		temp = ""
		while i < len(sys.argv):
			temp +=  (" " if i != 3 else "") + sys.argv[i]
			i += 1
		parser.set(sys.argv[2], 'name', temp)
		saveConfig()
	elif sys.argv[1] == "info":
		msg = ""
		for i, f in enumerate(parser.sections()):
			msg += f
			#print 'Section:', f
			#print '  Options:', parser.options(f)
			for name, value in parser.items(f):
				msg += "*^*^*" + value
				#print '  %s = %s' % (name, value)
			msg += ("%^%^%" if not i == int(len(parser.sections()) - 1) else "")
		#print f, parser.get(f, 'status',), parser.get(f, 'name')
		print msg
	elif sys.argv[1] == "reset":
		reset()
	elif sys.argv[1] == "version":
		print version
	#print 'Number of arguments:', len(sys.argv), 'arguments.'
	#print 'Argument List:', str(sys.argv)
# End Perform Input