#!/usr/bin/env python
from gpiozero import Button
from signal import pause
from datetime import datetime
import subprocess
from string import Template

emails = open('email.conf', 'r')
pipins = open('pipins.conf', 'r')

notifylist = []
for word in emails.read().split():
    notifylist.append(word)

actpins = {}
for line in pipins:
    l_split = line.split()
    actpins[int(l_split[0])] = l_split[1]


def current_date(fmt="%a %d-%m-%Y @ %H:%M:%S"):
    return datetime.strftime(datetime.now(), fmt)


notifycmd = {pin: Template("""echo "$date $sensor $state" | mail -s "Pi: $sensor $state" $email""") for pin in ACTPINS}


def notify(id, state, sensor_name):
    """Send each of the email addresses in NOTIFY_LIST a message"""
    for email in notifylist:
        shell_cmd = notifycmd[id].substitute(date=current_date(), state=state, sensor=sensor_name, email=email)
        proc = subprocess.Popen(shell_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout_value, stderr_value = proc.communicate()
        # This is where the sensor state changes are written to a file called sensor.log
        with open('sensor.log', 'a') as f:
            f.write('{}\n'.format(shell_cmd))


def dostate(button):
    # function to send email etc will only run when opened or closed
    state = 'closed' if button.is_pressed else 'opened'
    notify(button.pin, state, actpins[button.pin])
    print(state)


buttons = {}
for id in actpins:
    buttons[id] = Button(id)
    buttons[id].when_pressed = dostate
    buttons[id].when_released = dostate

pause()
