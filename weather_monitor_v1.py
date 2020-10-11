#!/usr/bin/env python

import bme680
import os
import sys
import time
import datetime as dt
import numpy as np
from demo_opts import get_device
from luma.core.render import canvas
from luma.core.virtual import viewport
from PIL import ImageFont
import math
import utils as ut


def make_font(name, size):
    font_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'fonts', name))
    return ImageFont.truetype(font_path, size)


def getBaselines ():
    start_time = time.time()
    curr_time = time.time()
    burn_in_time=10
    burn_in_data=[]
    
    try:
    # Collect gas resistance burn-in values, then use the average
    # of the last 50 values to set the upper limit for calculating
    # gas_baseline.
        print("Collecting gas resistance burn-in data for 5 mins\n")
        while curr_time - start_time < burn_in_time:
            curr_time = time.time()
            if sensor.get_sensor_data() and sensor.data.heat_stable:
                gas = sensor.data.gas_resistance
                burn_in_data.append(gas)
                print("Gas: {0} Ohms".format(gas))
                time.sleep(1)

        gas_baseline = sum(burn_in_data[-50:]) / 50.0

    # Set the humidity baseline to 40%, an optimal indoor humidity.
        hum_baseline = 40.0

    # This sets the balance between humidity and gas reading in the 
    # calculation of air_quality_score (25:75, humidity:gas)
        hum_weighting = 0.25

#        print("Gas baseline: {0} Ohms, humidity baseline: {1:.2f} %RH\n".format(gas_baseline, hum_baseline))
        return gas_baseline, hum_baseline
    except KeyboardInterrupt:
        pass

def getData (gasBase, humBase):
    weight=0.25
    try:
        while True:
            if sensor.get_sensor_data() and sensor.data.heat_stable :
                print(sensor.data.gas_resistance)
                isNow = dt.datetime.now()
                l = sensor.data.temperature, sensor.data.pressure, sensor.data.humidity, sensor.data.gas_resistance
                gas_offset = gasBase - l[3]
                hum_offset = humBase - l[2]
                
                if hum_offset > 0:
                    hum_score = (100 - humBase - hum_offset) / (100 - humBase) * (weight * 100)

                else:
                    hum_score = (humBase + hum_offset) / humBase * (weight * 100)

            # Calculate gas_score as the distance from the gas_baseline.
                if gas_offset > 0:
                    gas_score = (l[3] / gasBase) * (100 - (weight * 100))

                else:
                    gas_score = 100 - (weight * 100)

            # Calculate air_quality_score. 
                airScore = round((hum_score + gas_score), 2)
                l = l + (airScore, isNow)
                
                message = u"Temp: {0}c, Pressure: {1}hPa, Humidity: {2}%RH, Air quality: {3}%. ".format(l[0], l[1], l[2], l[4])

                time.sleep(3)
                return message, l
            
                
    except KeyboardInterrupt:
        pass


def scroll_message(message, font=None, speed=7):
    msg = message

    x = device.width

    # First measure the text size
    with canvas(device) as draw:
        w, h = draw.textsize(msg, font)

    virtual = viewport(device, width=max(device.width, w + x + x), height=max(h, device.height))
    with canvas(virtual) as draw:
        draw.text((x, 60), msg, font=font, fill="white")
        
    i = 0
    while i < x + w:
        virtual.set_position((i, 0))
        i += speed
        time.sleep(0.025)

#    print (msg)
    return msg
        
    
sensor = bme680.BME680()
device = get_device()        

if device.height >= 16:
    font = make_font("code2000.ttf", 25)
else:
    font = make_font("pixelmix.ttf", 8)        

r = getBaselines()
ut.initialize()

try:
    # These oversampling settings can be tweaked to
    # change the balance between accuracy and noise in
    # the data.
    sensor.set_humidity_oversample(bme680.OS_2X)
    sensor.set_pressure_oversample(bme680.OS_4X)
    sensor.set_temperature_oversample(bme680.OS_8X)
    sensor.set_filter(bme680.FILTER_SIZE_3)
    sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

    sensor.set_gas_heater_temperature(320)
    sensor.set_gas_heater_duration(150)
    sensor.select_gas_heater_profile(0)
    while True:
            if sensor.get_sensor_data():
                
                k = getData(r[0], r[1])
                ut.appendData(k[1])
                criticalMessage = ut.isCritical(k[1])
                scroll_message(k[0], font)
                scroll_message(criticalMessage, font)
                
    
            
except KeyboardInterrupt:
    pass
