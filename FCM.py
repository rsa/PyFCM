#! /usr/bin/python3
# -*- coding: utf-8 -*-
import os,sys
import OPi.GPIO as GPIO
import threading
import time

"""
Based on OrangePWM - Python software PWM for Orange Pi
https://github.com/evergreen-it-dev/orangepwm.git
"""


class FCM(threading.Thread):

  def __init__(self, frequency, channelOUT='PL8', channelIN=None):
    """ 
    Init the OrangePwm instance. Expected parameters are :
    - frequency : the frequency in Hz for the PWM pattern. A correct value may be 100.
    - channelOUT : the gpio.port which will act as PWM ouput
    """
    self.terminated = False
    self.toTerminate = False
    self.terminatedCounter = False
    self.toTerminateCounter = False

    self.initBaseValues(frequency)

    self.Counter = 0
    self.RPM = 0.0
    self.RPMdelta = 10.0
    self.lastTemp = 0.0

    self.channelOUT=channelOUT
    self.channelIN=channelIN

    self.iter_start = time.perf_counter()

    GPIO.setmode(GPIO.SUNXI)
    GPIO.setwarnings(False)

  def __del__(self):
    if self.toTerminate == True:
        self.stop()
    GPIO.cleanup()

  def initBaseValues(self, frequency, maxCycle=100.0):
    self.baseTime = 1.0 / float(frequency)
    self.maxCycle = maxCycle
    self.sliceTime = self.baseTime / self.maxCycle

  def getTemp(self):
    with open('/etc/armbianmonitor/datasources/soctemp', "r") as tempfile:
      temp = tempfile.read()
      tempfile.close()
      return float(temp)/1000.0
    return 0.0

  def getLastTemp(self):
    return self.lastTemp

  def getLastRPM(self):
    return self.RPM

  def getMaxCycle(self):
    return self.maxCycle

  def getdutyCycle(self):
    return self.dutyCycle

  def start(self, dutyCycle):
    """
    Start PWM output. Expected parameter is :
    - dutyCycle : percentage of a single pattern to set HIGH output on the GPIO pin

    Example : with a frequency of 1 Hz, and a duty cycle set to 25, GPIO pin will 
    stay HIGH for 1*(25/100) seconds on HIGH output, and 1*(75/100) seconds on LOW output.
    """
    self.dutyCycle = dutyCycle
    GPIO.setup(self.channelOUT, GPIO.OUT)
    self.lock = threading.Lock()
    self.thread = threading.Thread(None, self.run, None, (), {})
    self.thread.start()

    if self.channelIN is not None:
        self.startCounter()

  def startCounter(self):
    """
    Start PWM counter
    """
    GPIO.setup(self.channelIN, GPIO.IN)
    self.lockCounter = threading.Lock()
    self.thread = threading.Thread(None, self.runCounter, None, (), {})
    self.thread.start()


  def run(self):
    """
    Run the PWM pattern into a background thread. This function should not be called outside of this class.
    """
    self.lock.acquire()
    while self.toTerminate == False:
      if self.dutyCycle > 0:
        if GPIO.input(self.channelOUT) == GPIO.LOW:
            GPIO.output(self.channelOUT, GPIO.HIGH)
        time.sleep(self.dutyCycle * self.sliceTime)
 
      if self.dutyCycle < self.maxCycle:
        if GPIO.input(self.channelOUT) == GPIO.HIGH:
            GPIO.output(self.channelOUT, GPIO.LOW)
        time.sleep((self.maxCycle - self.dutyCycle) * self.sliceTime)

      if self.channelIN is not None:
        now = time.perf_counter()
        iter_elapsed = now - self.iter_start

        if iter_elapsed > self.RPMdelta:
          self.iter_start = now
          self.countRPM(iter_elapsed)

    self.lock.release()

  def runCounter(self):
    """
    Run the PWM counter.
    """
    self.lockCounter.acquire()

    while self.toTerminateCounter == False:
      GPIO.wait_for_edge(self.channelIN,GPIO.FALLING, timeout=1000)
      self.doCounter()

#    GPIO.remove_event_detect(self.channelIN)
    self.lockCounter.release()

  def doCounter(self):
    self.Counter += 1

  def countRPM(self, delta):
    """
    count RPM of
    """
    tempCounter=float(self.Counter)
    self.Counter = 0
    self.RPM = tempCounter/delta*60.0
    self.lastTemp = self.getTemp()
#    print(self.RPM, self.getTemp())


  def changeDutyCycle(self, dutyCycle):
    """
    Change the duration of HIGH output of the pattern. Expected parameter is :
    - dutyCycle : percentage of a single pattern to set HIGH output on the GPIO pin

    Example : with a frequency of 1 Hz, and a duty cycle set to 25, GPIO pin will 
    stay HIGH for 1*(25/100) seconds on HIGH output, and 1*(75/100) seconds on LOW output.
    """
    self.dutyCycle = dutyCycle


  def changeFrequency(self, frequency):
    """
    Change the frequency of the PWM pattern. Expected parameter is :
    - frequency : the frequency in Hz for the PWM pattern. A correct value may be 100.

    Example : with a frequency of 1 Hz, and a duty cycle set to 25, GPIO pin will 
    stay HIGH for 1*(25/100) seconds on HIGH output, and 1*(75/100) seconds on LOW output.
    """
    self.baseTime = 1.0 / frequency
    self.sliceTime = self.baseTime / self.maxCycle


  def stop(self):
    """
    Stops PWM output.
    """
    self.toTerminate = True

    self.lock.acquire()

    GPIO.output(self.channelOUT, GPIO.LOW)
    if self.channelIN is not None:
        self.stopCounter()

    self.lock.release()
    GPIO.cleanup(self.channelOUT)

    self.toTerminate = False


  def stopCounter(self):
    """
    Stops Counter.
    """
    self.toTerminateCounter = True
    self.lockCounter.acquire()


    self.lockCounter.release()
    GPIO.cleanup(self.channelIN)

