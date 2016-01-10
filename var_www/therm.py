#!/usr/bin/python
import cgi
import os
import time
import re

def getSensorValue(id):
	fileContent = os.popen("sensors | grep 'Core\|temp1\|fan1'").read()
	rows = fileContent.split("\n")
	for row in rows:
		if row.find(id) == 0:
			#print row
			#print "___"
			m = re.search(': +\+?([\d\.].*?) ', row)
			value = m.group(1)
			#print value
			#print "___"
			return value
	
def getSmartValue(id):
	fileName = "smartctl -a -d ata /dev/{0} | grep '194 Te'".format(id)
	fileContent = os.popen(fileName).read()
	print "___"+fileContent+"___"
	return ""

print "Content-Type: text/html\n"

config = {}

config["core0"] = {}
config["core0"]["param"]="Core 0"
config["core0"]["type"]="sensor"
config["core0"]["mesaure"]="C"

config["core1"] = {}
config["core1"]["param"]="Core 1"
config["core1"]["type"]="sensor"
config["core1"]["mesaure"]="C"

config["mb"] = {}
config["mb"]["param"]="temp1"
config["mb"]["type"]="sensor"
config["mb"]["mesaure"]="C"

config["fan"] = {}
config["fan"]["param"]="fan1"
config["fan"]["type"]="sensor"
config["fan"]["mesaure"]="RPM"

config["hdd"] = {}
config["hdd"]["param"]="sda"
config["hdd"]["type"]="smart"
config["hdd"]["mesaure"]="C"

params = cgi.FieldStorage()

id = params["id"].value
item = config[id]
#print item

value=0
#print  os.popen("cat /sys/bus/w1/devices/28-0000066a9cc9/w1_slave").read().split("\n")[1].split("=")[1]
if (item["type"] == "sensor"):
	value = getSensorValue(item["param"])
else:
	value = getSmartValue(item["param"])

timeValue = time.time();
#print value
print ("{{\"id\":\"{0}\",\"type\":\"{1}\",\"value\":{2},\"mesaure\":\"{4}\",\"time\":{3}}}".format(id,item["type"],value,timeValue,item["mesaure"]))