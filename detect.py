import bluetooth
import time 
import requests
import logging.config
import logging
import yaml

CONFIG = {}

def loadConfigAndLogging():
	global CONFIG

	with open("config.yaml", 'rt') as f:
		CONFIG = yaml.load(f.read())

	with open("logging.yaml", 'rt') as f:
		logging.config.dictConfig(yaml.load(f.read()))

def outOfDaHouse():
	logger = logging.getLogger(__name__)
	logger.info("byebye")
	for url in CONFIG['OFF_REQUEST_PAGES']:
		requests.post(url)

def gotBack():
	logger = logging.getLogger(__name__)
	logger.info("HELLO")
	for url in CONFIG['ON_REQUEST_PAGES']:
		requests.post(url)


def main():

	loadConfigAndLogging()

	logger = logging.getLogger(__name__)
	logger.info("YO, starting detector")

	outOfHomeCounter = 0

	while True:

		result = bluetooth.lookup_name(CONFIG['BLUETOOTH_MAC'], timeout=CONFIG['BLUETOOTH_TIMEOUT_SECS'])

		logger.info("search result:{0}".format(result is not None))

		if result is None:
			if outOfHomeCounter == CONFIG['MAX_COUNTER_FOR_TURN_OFF']:
				outOfDaHouse()
				outOfHomeCounter += 1
			elif outOfHomeCounter < CONFIG['MAX_COUNTER_FOR_TURN_OFF']:
				outOfHomeCounter += 1
				logger.info("{0}".format(outOfHomeCounter))
		else:
			if outOfHomeCounter == CONFIG['MAX_COUNTER_FOR_TURN_OFF'] + 1:
				outOfHomeCounter = 0
				gotBack()

			outOfHomeCounter = 0

		time.sleep(CONFIG['SLEEP_TIME_SECS'])

if __name__ == "__main__":
	main()
