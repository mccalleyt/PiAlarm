#!/usr/bin/env python
 
from settings import DOOR_PIN, SLEEP_TIME, NOTIFY_LIST, WIN0, WIN1, WIN2
 
import time
from datetime import datetime
import subprocess
from string import Template
 
#
# Notification by email
 
def current_date (fmt="%a %d-%m-%Y @ %H:%M:%S"):
    return datetime.strftime(datetime.now(), fmt)
 
NOTIFY_CMD = {DOOR_PIN: Template("""echo "$date door $state" | mail -s "Pi: door $state" $email"""), 
              WIN0:     Template("""echo "$date East Window $state" | mail -s "Pi: East Window $state" $email"""),
              WIN1:     Template("""echo "$date North Window $state" | mail -s "Pi: North Window $state" $email"""),
              WIN2:     Template("""echo "$date West Window $state" | mail -s "Pi: West Window $state" $email""")}
 
def notify (id, state):
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
 
io.setup([DOOR_PIN, WIN0, WIN1, WIN2], io.IN,
         pull_up_down=io.PUD_UP) # activate the reed input with PullUp
 
STATE = {}
for id in [DOOR_PIN, WIN0, WIN1, WIN2]:
  STATE[id] = {'current': 'closed',
               'prior'  : 'closed'}

while True:
    notification_list = []
    for id in [DOOR_PIN, WIN0, WIN1, WIN2]:
        STATE[id]['prior'] = STATE[id]['current']
        STATE[id]['current'] = 'opened' if io.input(id) else 'closed'
        if STATE[id]['current'] != STATE[id]['prior']: # only need to do anything on change
            notification_list.append((id, STATE[id]['current']))
    # maybe do all the emailing together at the end - or less frequently
    for id, state in notification_list:
        notify(id, state)
 
    time.sleep(SLEEP_TIME)
