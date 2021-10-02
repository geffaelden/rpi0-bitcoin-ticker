#!/usr/bin/env python
# coding: utf-8

# In[62]:


from pycoingecko import CoinGeckoAPI
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

import sys
import os
#libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
#if os.path.exists(libdir):
#    sys.path.append(libdir)
    
import logging
#from waveshare_epd import epd2in13_V2
import time
from PIL import Image, ImageDraw, ImageFont
import traceback

#logging.basicConfig(level=logging.DEBUG)
cg = CoinGeckoAPI()


# In[23]:


def get_chart_prices():
    prices = cg.get_coin_market_chart_range_by_id(id='bitcoin',vs_currency='usd',from_timestamp=int(datetime.now().timestamp())-86400,to_timestamp=int(datetime.now().timestamp()))
    x = []
    y = []
    for price in prices['prices']:
        x.append(price[0])
        y.append(price[1])
    
    return x, y

def thousands(x, pos):
    'The two args are the value and tick position'
    return '$%1.1fK' % (x*1e-3)

def gen_graph(x, y):
    formatter = FuncFormatter(thousands)
    fig, ax = plt.subplots(figsize=(2, .9),dpi=130)
    
    ax.yaxis.set_major_formatter(formatter)
    ax.tick_params(axis="y", labelsize=6.4, width =.5)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_linewidth(0.5)
    ax.spines['left'].set_linewidth(0.5)
    
    fig.patch.set_facecolor('white')
    plt.plot(x, y, color='black', linewidth='.7')
    plt.xticks([])
    fig.savefig('chart.png',bbox_inches='tight')

def crop_image(path='chart.png'):
    try:
        image = Image.open(path)
    except Exception as e:
        print(e)
    
    w, h = image.size
    image.crop((13,9,w-17,h-15)).save('chart_cropped.png')


# In[67]:


try:
    # start prog
    logging.info("epd2in13_V2 Demo")
    epd = epd2in13_V2.EPD()
    logging.info("init and Clear")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)
    
    # fotnts
    font15 = ImageFont.truetype(('Font.ttc'), 15)
    font24 = ImageFont.truetype(('Font.ttc'), 24)
    
    # get prices
    x, y = get_chart_prices()
    gen_graph(x, y)
    time.sleep(1)
    crop_image()
    
    # start partial updates
    epd.init(epd.PART_UPDATE)
    # read bmp file 
        
    logging.info("read chartfile file...")
    image = Image.new('1', (epd.height, epd.width), 255) 
    draw = ImageDraw.Draw(image)
    bmp = Image.open('chart_cropped.png')
    image.paste(bmp, (0,0))
    epd.displayPartBaseImage(epd.getbuffer(image))
    time.sleep(2)
      
    num = 0 
    while (True):
        price_now = cg.get_exchange_rates()['rates']['usd']['value']
        
        draw.rectangle((0, 96, 250, 122), fill = 255)
        draw.text((54, 96), 'BTC: ${0:,.2f}'.format(price_now), font = font24, fill = 0)
        epd.displayPartial(epd.getbuffer(image))
        num = num + 1
        
        if num >= 5:
            x, y = get_chart_prices()
            gen_graph(x, y)
            time.sleep(1)
            crop_image()
            
            draw.rectangle((0, 96, 250, 122), fill = 255)
            bmp = Image.open('chart_cropped.png')
            image.paste(bmp, (0,0))
            epd.displayPartial(epd.getbuffer(image))
            
            num = 0
            time.sleep(59)
        else:
            time.sleep(60)
            
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    logging.info("Clear...")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)
    time.sleep(2)
    epd2in13_V2.epdconfig.module_exit()
    exit()
    

