import bluetooth
import time 
import requests
import logging.config
import logging
import yaml

isHome = None
outOfHomeCounter = 0

CONFIG = {}

def loadConfigAndLogging():
	global CONFIG

	with open("config.yaml", 'rt') as f:
		CONFIG = yaml.load(f.read())

	with open("logging.yaml", 'rt') as f:
		logging.config.dictConfig(yaml.load(f.read()))

def outOfDaHouse():
	logger.info("byebye")
	for url in CONFIG['OFF_REQUEST_PAGES']:
		requests.post(url)

def gotBack():
	logger.info("HELLO")
	for url in config['ON_REQUEST_PAGES']:
		requests.post(url)

while True:

	loadConfigAndLogging()

	logger = logging.getLogger(__name__)
	logger.info("YO, starting detector")

	result = bluetooth.lookup_name(CONFIG['BLUETOOTH_MAC'], timeout=config['BLUETOOTH_TIMEOUT_SECS'])
	
	if result is None:
		if outOfHomeCounter == config['MAX_COUNTER_FOR_TURN_OFF']:
			outOfDaHouse()
			outOfHomeCounter += 1
		elif outOfHomeCounter < config['MAX_COUNTER_FOR_TURN_OFF']:
			outOfHomeCounter += 1
			logger.info("{0}".format(outOfHomeCounter))
	else:
		if outOfHomeCounter == config['MAX_COUNTER_FOR_TURN_OFF'] + 1:
			outOfHomeCounter = 0
			gotBack()
		
		outOfHomeCounter = 0
	
	time.sleep(config['SLEEP_TIME_SECS'])
