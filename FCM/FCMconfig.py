#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import configparser

class FCMconfig():

  def __init__(self, filename='/var/lib/FCM/FCMconfig.ini'):
    self.config = configparser.ConfigParser()
    self.config.optionxform = str
    self.optionxform = str
    self.filename = filename

  def __del__(self):
    del self.config

  def makeDefaultConfig(self, fansNum=1):
    config = configparser.ConfigParser()
    config.optionxform = str

    config.add_section('Settings')
    config.set('Settings','BoardType','SUNXI')
    config.set('Settings','BoardName',self.getBoardName())
    config.set('Settings','FansNumber',str(fansNum))
    config.set('Settings','PidFile','/run/FCM.pid')
    config.set('Settings','TargetTemperature','55')
    config.set('Settings','ReactionTimeSec','10')
    config.set('Settings','RPMMeasureSec','60')
    config.set('Settings','RPMMeasureIntervalSec','600')
    config.set('Settings','RPMCalibrate','True')
    config.set('Settings','TemperatureCalibrate','False')

    for i in range(fansNum):
        config.add_section('Fan'+str(i))
        config.set('Fan'+str(i),'Mode','auto')
        config.set('Fan'+str(i),'ContriolGPIO','PL8')
        config.set('Fan'+str(i),'SignalGPIO','PH6')
        config.set('Fan'+str(i),'CalibratedFreq','40')
        config.set('Fan'+str(i),'CalibratedMinDuty','40')
        config.set('Fan'+str(i),'CalibratedMaxDuty','60')
        config.set('Fan'+str(i),'ManualFreq','40')
        config.set('Fan'+str(i),'ManualDuty','40')

        config.set('Fan'+str(i),'CalibrateForce','False')
        config.set('Fan'+str(i),'CalibrateFreqs','20,40,60,80,100')
        config.set('Fan'+str(i),'CalibrateDutys','0,10,20,30,40,50,60,70,80,90,100')
        config.set('Fan'+str(i),'CalibrateRPMs','0,0,0,0,0,0,0,0,0,0,0')
        config.set('Fan'+str(i),'CalibrateCalculatedFreq','0')
        config.set('Fan'+str(i),'CalibrateTemperatureDelta','0,0,0,0,0,0,0,0,0,0,0')
        config.set('Fan'+str(i),'CalibrateCalculatedDutyMin','40')
        config.set('Fan'+str(i),'CalibrateCalculatedDutyMax','80')

    return config


  def updateConfig(self, config = None, fansNum=1 ):

    """
    Create, read, update, delete config
    """
    path=os.path.dirname(self.filename)
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    if config == None:
        if os.path.isfile(self.filename):
            os.remove(self.filename)
        self.config = self.makeDefaultConfig(fansNum)

    # Вносим изменения в конфиг. файл.
    with open(self.filename, "w") as config_file:
        self.config.write(config_file)
        config_file.close()

    return self.config

  def readConfig(self):

    if not os.path.exists(self.filename):
        self.config = self.updateConfig(fansNum)
    else:
        self.config = configparser.ConfigParser()
        self.config.optionxform = str
        self.config.read(self.filename)

    return self.config

  def getBoardName(self):
    boardName=os.popen('cat /etc/armbian-release |grep "BOARD=" |sed "s/.*=//"|tr -d "\n"').read()
    return boardName

  def get(self, sectionName, valueName):
    value = self.config.get(sectionName,valueName)
    return value

  def getByNum(self, FanNum, valueName):
    value = self.config.get("Fan"+str(FanNum),valueName)
    return value

  def getListValue(self, valueName, fanNum = 0):
    valueList = self.config.get("Fan"+str(fanNum),valueName).replace(' ', '').split(',')
    return valueList
