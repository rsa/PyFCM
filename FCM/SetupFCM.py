#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os,sys
import time
import argparse
import signal
from FCM import FCM
from FCM import FCMconfig

def run(config):
    setDaemonPID(config)

    fcm = []

    for i in range(int(config.get("Settings", "FansNumber"))):
        fcm.insert(i,FCM.FCM(int(config.getByNum(i, "ManualFreq")),
                         config.getByNum(i, "ContriolGPIO"),
                         config.getByNum(i, "SignalGPIO")))
        fcm[i].start(int(config.getByNum(i, "ManualDuty")))

    while not doStop:
        time.sleep(int(config.get("Settings", "ReactionTimeSec")))

    for i in range(int(config.get("Settings", "FansNumber"))):
        fcm[i].stop()

    del fcm

    clearDaemonPID(config)

    return

def calibrate(config):
    #TODO
    return

def calibratetemp(config):
    #TODO
    return

def configreload(config):
    pid = getDaemonPID(config)
    if pid is not None:
        os.kill(pid, signal.SIGHUP)
    return

def stop(config):
    pid = getDaemonPID(config)
    if pid is not None:
        os.kill(pid, signal.SIGTERM)
    global doStop
    doStop = True
    return

def configReloadHandler(signum, frame):
#    print('Signal handler called with signal', signum)
    global doStop
    doStop = True
    global doReload
    doReload = True

def exitHandler(signum, frame):
#    print('Signal handler called with signal', signum)
    global doStop
    doStop = True

def setDaemonPID(config):
    config.get("Settings", "PidFile")
    try:
        pf = open(config.get("Settings", "PidFile"),'w')
        pid = os.getpid()
        print(pid, file=pf, flush=True)
        pf.close()
    except IOError:
        pass

def clearDaemonPID(config):
    config.get("Settings", "PidFile")
    try:
        os.remove(config.get("Settings", "PidFile"))
    except IOError:
        pass

def getDaemonPID(config):
    try:
        pf = open(config.get("Settings", "PidFile"),'r')
        pid = int(pf.read().strip())
        pf.close()
    except IOError:
        pid = None

    if not pid:
        message = "pidfile %s does not exist. Daemon not running?\n"
        sys.stderr.write(message % self.pidfile)
        return None

    return pid


def sendSignalToDaemon(config):
    # Try killing the daemon process
    pid = getDaemonPID(config)
    if pid is not None:
        try:
            while 1:
                os.kill(pid, SIGHUP)
                time.sleep(0.1)
        except OSError:
            if os.path.exists(self.pidfile):
                os.remove(self.pidfile)


#os.getpid()
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Setup for SBC fan control daemon, based on Python FCM class")

#Common settings
    parser.add_argument('command', type=str, help='Command')

    parser.add_argument("-v", "--verbose", action = "store_true", help = "Be verbose?")
    parser.add_argument("-r", "--reset", action = "store_true", help = "Cleanup current config")
    parser.add_argument("-f", "--force", action = "store_true", help = "Force operations")
    parser.add_argument("-a","--noauto", action = "store_true", help = "NOT Make auto checks")
    parser.add_argument("-n", "--numoffans", type = int, default = 1, help = "Number of fan's")

#config files
    parser.add_argument("--config", type = str, default = "/var/lib/FCM/FCMconfig.ini", help = "Config file")

    args = parser.parse_args()

    config = FCMconfig.FCMconfig(args.config)
    global doStop
    global doReload

    doStop = False
    doReload = True

    signal.signal(signal.SIGTERM, exitHandler)
    signal.signal(signal.SIGINT, exitHandler)
    signal.signal(signal.SIGHUP, configReloadHandler)

    if args.command == "setup":
        if (args.reset):
            _config = config.updateConfig(None,args.numoffans)
        else:
            _config = config.readConfig()

        print("Config board:",_config.get('Settings','BoardName')," Current board:",config.getBoardName())
        config.updateConfig(_config)

    elif args.command == "start" or args.command == "daemon":
        while doReload == True:
            doReload = False
            doStop = False
            config.readConfig()
            run(config)
    elif args.command == "calibrate":
        config.readConfig()
        calibrate(config)
    elif args.command == "calibratetemp":
        config.readConfig()
        calibratetemp(config)
    elif args.command == "reload":
        config.readConfig()
        configreload(config)
    elif args.command == "stop":
        config.readConfig()
        stop(config)
    else:
        print("Command ",args.command," unknown!")

    sys.exit(0)
