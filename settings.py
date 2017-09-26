#!/usr/bin/env python
 
"""
This file defines the configuration settings for doorchecker.py
change them according to your environment, or use a local_settings.py
file which is excluded from source control.
 
"""
 
DOOR_PIN    = 8
WIN0        = 9
WIN1        = 10
WIN2        = 11
SLEEP_TIME  = 0.01
NOTIFY_LIST = ['*******@*******.com', '*********@**********.com']
 
# Override any of the above settings for your local environment in a
# separate local_settings.py file which is *not* checked into  source
# control
 
try:
    from local_settings import *
except ImportError:
    pass
