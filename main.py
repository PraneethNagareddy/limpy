from core.builder import SpiderBuilder
from core.spider import Spider

import logging

logging.basicConfig(level=logging.INFO, format='\r%(asctime)s - %(levelname)s - %(message)s\r')

builder = SpiderBuilder()
(builder
 .build_legs()
 .get_spider())

# Now your 2.2kg robot is ready to walk!
Spider.get().startup()


