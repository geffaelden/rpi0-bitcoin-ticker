#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = '/pic'
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd2in13_V2 Demo")
    
    epd = epd2in13_V2.EPD()
    logging.info("init and Clear")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)
   
    # read bmp file 
    logging.info("1.read bmp file...")
    image = Image.new('1', (epd.height, epd.width), 255) 
    bmp = Image.open('test.bmp')
    image.paste(bmp, (2,2))
    epd.display(epd.getbuffer(image))
    time.sleep(10)
    
    # epd.Clear(0xFF)
    logging.info("Clear...")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)
    epd.sleep()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13_V2.epdconfig.module_exit()
    exit()
