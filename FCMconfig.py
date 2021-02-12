#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import configparser

class FCMconfig():

  def __init__(self, filename='/var/lib/FCM/FCMconfig.ini'):
    self.filename = filename
    self.config = configparser.ConfigParser()
    self.config.optionxform = str

  def __del__(self):
    del self.config

  def makeDefaultConfig(self):
    config = configparser.ConfigParser()
    config.optionxform = str

    config.add_section('Settings')
    config.set('Settings','BoardType','SUNXI')
    config.set('Settings','BoardName',self.getBoardName())
    config.set('Settings','FansNumber','1')
    config.set('Settings','TargetTemperature','55')
    config.set('Settings','RPMCalibrate','True')
    config.set('Settings','TemperatureCalibrate','False')

    config.add_section('Fun-0')
    config.set('Fun-0','Mode','auto')
    config.set('Fun-0','ContriolGPIO','L8')
    config.set('Fun-0','SignalGPIO','H5')
    config.set('Fun-0','CalibratedFreq','40')
    config.set('Fun-0','CalibratedMinDuty','40')
    config.set('Fun-0','CalibratedMaxDuty','60')
    config.set('Fun-0','ManualFreq','40')
    config.set('Fun-0','ManualDuty','40')

    config.add_section('Calibrate-0')
    config.set('Calibrate-0','Force','False')
    config.set('Calibrate-0','Freqs','20,40,60,80,100')
    config.set('Calibrate-0','Dutys','0,10,20,30,40,50,60,70,80,90,100')
    config.set('Calibrate-0','RPMs','0,0,0,0,0,0,0,0,0,0,0')
    config.set('Calibrate-0','CalculatedFreq','0')
    config.set('Calibrate-0','TemperatureDelta','0,0,0,0,0,0,0,0,0,0,0')
    config.set('Calibrate-0','CalculatedDutyMin','40')
    config.set('Calibrate-0','CalculatedDutyMax','80')

    return config


  def updateConfig(self, config = None):

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
        self.config = self.makeDefaultConfig()

    # Вносим изменения в конфиг. файл.
    with open(self.filename, "w") as config_file:
        self.config.write(config_file)
        config_file.close()

    return self.config

  def readConfig(self):

    if not os.path.exists(self.filename):
        self.config = self.updateConfig()
    else:
        self.config = configparser.ConfigParser()
        self.config.optionxform = str
        self.config.read(self.filename)

    return self.config

  def getBoardName(self):
    boardName=os.popen('cat /etc/armbian-release |grep "BOARD=" |sed "s/.*=//"|tr -d "\n"').read()
    return boardName
