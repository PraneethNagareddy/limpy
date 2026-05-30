import RPi.GPIO as GPIO # Import RPi.GPIO
from core.builder import SpiderBuilder
from core.spider import Spider

import logging

logging.basicConfig(level=logging.INFO, format='\r%(asctime)s - %(levelname)s - %(message)s\r')

GPIO.setmode(GPIO.BCM)

builder = SpiderBuilder()
(builder
 .build_legs()
 .add_feedback_communicator()
 .get_spider())

# Now your 2.2kg robot is ready to walk!
Spider.get().startup()
