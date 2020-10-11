#!/usr/bin/env python
import numpy as np
import time
import datetime as dt
import math
import pandas as pd
import os, sys
import stat
import matplotlib.pyplot as plt
import smtplib
import ssl
from email.mime.text import MIMEText
import keys
import thresholds as tH
import glob

context = ssl.create_default_context()
curr_dir = os.getcwd()
filename = curr_dir +'/data/dataKeep.csv'
readable = dt.datetime.now()
cList = ['Temp', 'Pressure', 'Humidity', 'Gas Resistance', 'Air Quality']



def initialize():
    checkForFiles()
    newFiles()
    

def checkForFiles():
    img_folder = os.path.isdir('./images')
    data_folder = os.path.isdir('./data')
    path_images = curr_dir+"/images"
    path_data = curr_dir+"/data"

    if img_folder is False:
        os.mkdir(path_images);
        os.chmod(path_images, stat.S_IRWXU)
        print ("Creating image folder...")
    else:
        print("Image folder exists...")
    if data_folder is False:
        os.mkdir(path_data);
        os.chmod(path_data, stat.S_IRWXU)
        print ("Creating data folder...")
#        newFiles()
#        print ("Creating files")
    else:
        print("Data folder exists...")
        
def isCritical(sensorTuple):
 
    tempMax = tH.MaxTemp
    tempMin = tH.MinTemp
    humMax = tH.MaxHumidity
    humMin = tH.MinHumidity
    scoreMin = tH.airScoreLimit
    temp = sensorTuple[0]
    hum = sensorTuple[2]
    score = sensorTuple[4]
    if temp > tempMax or temp < tempMin or hum > humMax or hum < humMin or score < scoreMin  :
        critical = True
        msg = u"Conditions critical. Temp {0}c, Humidity {1}%rh. Air quality: {2}%".format(sensorTuple[0], sensorTuple[2], sensorTuple[4])
        ut.mailer(msg)
    else:
        critical = False
        msg = "*** Conditions Normal. *** \n"
    return msg
    
    

def appendData(data):
    df = pd.DataFrame(data)
    df_tr = df.transpose()
    df_tr.columns = ['Temp', 'Pressure', 'Humidity', 'Gas Resistance', 'Air Quality','Date']
    df_tr.set_index('Date', inplace=True)
    
    with open(filename, 'a') as f:
        df_tr.to_csv(f, header=None, index=True)



def mailer(message):
    subject = 'Conditions Warning!'
    mailIs = 'Subject: {}\n\n{}'.format(subject, message)

    with smtplib.SMTP_SSL(keys.smtp_server, keys.port, context=context) as server:
        server.login(keys.sender_email, keys.password)
            
        for mail in keys.receiver_email :    
            server.sendmail(keys.sender_email, mail, mailIs)


def plotChart(columnName, length):
    
    df = pd.read_csv(filename)
    ma_factor = int(length/4)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Date'] = df['Date'].apply(lambda x: x.replace(microsecond = 0))
    df['MA'] = df[columnName].rolling(ma_factor).mean()
     
    fig,ax=plt.subplots()
    fig.set_size_inches(9, 6)
    ax.plot(df['Date'], df[columnName], color='red')
    ax.set_xlabel('Time', fontsize=14)
    ax.set_ylabel(columnName, color='red', fontsize=14)
    
    ax2=ax.twinx()
    ax2.plot(df['Date'], df['MA'], color='blue')
    ax2.set_ylabel(ma_factor, color='blue', fontsize = 14)
        
    saveAsName = curr_dir+"/images/"+columnName + '_Image_'+str(dt.datetime.now().strftime("%y-%m-%d-%H-%M-%S"))
    fig.savefig(saveAsName, dpi=100)
    
    
def plotAll(columnsList, length):
    for col in columnsList:
        plotChart(col, length)




def removeFiles(ext):
    found = False
    files = glob.glob(curr_dir + '/images/*.'+ ext)
    for file in files:
        try:
            os.remove(file)
            found = True
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))
            found = False
                
    if found is True :
        print ('Cleanup complete!')
    elif found is False :
        print ('File not found')
    else:
        print ('Something went wrong')
        

def newFiles():
    
    found = False
    files = glob.glob(curr_dir + '/data/dataKeep.csv')
    
    for file in files:
        try:
            if file:
                found = True
            
            elif OSError.strerror:
                found = False
   
        except KeyboardInterrupt:
            pass
    
    if found:
        print('Files found!')
    elif not found:
        print('Not found! Creating empties')
        df = pd.DataFrame(columns=list(['Date','Temp', 'Pressure', 'Humidity', 'Gas Resistance', 'Air Quality']), index=range(0))
        df.set_index('Date', inplace=True)
        df.to_csv(filename, encoding='utf-8', index=True)
                




