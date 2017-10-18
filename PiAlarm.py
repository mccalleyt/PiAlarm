#!/usr/bin/env python
 
import time
from datetime import datetime
import subprocess
from string import Template
from operator import itemgetter

# It counts the lines to determine how many times the loop runs to activate the
# input pins according to the pipins.conf file.

actspins = []
sensor = []

pins = []
with open('pipins.conf') as my_file:
    for line in my_file:
        pins.append(line)
    #Reads the index 0 of each subarray and makes a new array of the active pins.
    pins(map(itemgetter(0), actpins))
    #Reads the index 1 of each subarray and makes a new array of the active pin's name.
    pins(map(itemgetter(1), sensor))

#
# Notification by email
 
def current_date (fmt="%a %d-%m-%Y @ %H:%M:%S"):
    return datetime.strftime(datetime.now(), fmt)
 
NOTIFY_CMD = {actpins: Template("""echo "$date $sensor $state" | mail -s "Pi: $sensor $state" $email""")}
 
def notify (id, state, sensor):
    """Send each of the email addresses in NOTIFY_LIST a message"""
 
    for email in NOTIFY_LIST:
        shell_cmd = NOTIFY_CMD[id].substitute(date=current_date(),
                                          state=state,
                                          email=email)
        proc = subprocess.Popen(shell_cmd,
                                shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        stdout_value, stderr_value = proc.communicate()
 
#
# GPIO logic
 
import RPi.GPIO as io
io.setmode(io.BCM)
 
io.setup([actpins], io.IN,
         pull_up_down=io.PUD_UP) # activate the reed input with PullUp
 
STATE = {}
for id in [actpins]:
  STATE[id] = {'current': 'closed',
               'prior'  : 'closed'}

while True:
    notification_list = []
    for id in [actpins, sensor]:
        STATE[id]['prior'] = STATE[id]['current']
        STATE[id]['current'] = 'opened' if io.input(id) else 'closed'
        if STATE[id]['current'] != STATE[id]['prior']: # only need to do anything on change
            notification_list.append((id, STATE[id]['current'], sensor[id]))
    # maybe do all the emailing together at the end - or less frequently
    for id, state in notification_list:
        notify(id, state, sensor)
 
    time.sleep(
