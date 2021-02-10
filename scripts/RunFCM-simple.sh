#! /usr/bin/python3
# -*- coding: utf-8 -*-
from FCM import *

# Set GPIO pin PA6 as PWM output with a frequency of 100 Hz
fcm = FCM(40,'PL8','PH6')
fcm1 = FCM(40,'PL10','PH5')
#fcm = FCM(50,'PL8')
#fcm1 = FCM(50,'PL10')

#fcm = FCM(100,'PL10','PH6')
# Start PWM output with a duty cycle of 20%. The pulse (HIGH state) will have a duration of
# (1 / 100) * (20 / 100) = 0.002 seconds, followed by a low state with a duration of
# (1 / 100) * ((100 - 20) / 100) = 0.008 seconds.
# If a LED is plugged to with GPIO pin, it will shine at 20% of its capacity.
fcm.start(40)
fcm1.start(40)
