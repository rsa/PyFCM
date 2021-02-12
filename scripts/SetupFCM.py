#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
from FCMconfig import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Setup for SBC fan control daemon, based on Python FCM class")
#Common settings
    parser.add_argument("-v", "--verbose", action = "store_true", help = "Be verbose?")
    parser.add_argument("-r", "--reset", action = "store_true", help = "Cleanup current config")
    parser.add_argument("-f", "--force", action = "store_true", help = "Force operations")
    parser.add_argument("-a","--noauto", action = "store_true", help = "NOT Make auto checks")

#config files
    parser.add_argument("--config", type = str, default = "/var/lib/FCM/FCMconfig.ini", help = "Default config.")

    args = parser.parse_args()
    config = FCMconfig(args.config)
    if (args.reset):
        _config = config.updateConfig()
    else:
        _config = config.readConfig()

    for section in _config.sections():
        print(str(section))
    print("Config board:",_config.get('Settings','BoardName')," Current board:",config.getBoardName())

    config.updateConfig(_config)
