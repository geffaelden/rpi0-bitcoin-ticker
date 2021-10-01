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
    draw = ImageDraw.Draw(image)
    bmp = Image.open('test.png')
    image.paste(bmp, (0,0))
    epd.displayPartBaseImage(epd.getbuffer(image))
    time.sleep(2)

    # Drawing on the image
    font15 = ImageFont.truetype(('Font.ttc'), 15)
    font24 = ImageFont.truetype(('Font.ttc'), 24)
       
    epd.init(epd.PART_UPDATE)
    num = 0
    while (True):
        draw.rectangle((0, 87, 250, 122), fill = 255)
        draw.text((54, 96), 'BTC: ${0:,.2f}'.format(40000.00+num), font = font24, fill = 0)
        epd.displayPartial(epd.getbuffer(image))
        num = num + 1
        if(num == 10):
            break
        time.sleep(1)
    
    time.sleep(30)
    logging.info("Clear...")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13_V2.epdconfig.module_exit()
    exit()
