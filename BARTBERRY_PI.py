#!/usr/bin/env python

# thanks are owed to Evan Meaney, farptr & audionoobhelpme on Reddit, larsks on stackexchange, and the resources here: 
# Resource A: https://raspberrypi.stackexchange.com/questions/76667/debouncing-buttons-with-rpi-gpio-too-many-events-detected
# Resource B: https://www.reddit.com/r/raspberry_pi/comments/a3c8se/finally_finished_my_shuffler_based_on_the_design/
# Resource C: https://stephencoyle.net/the-pi-zero-simpsons-shuffler

import RPi.GPIO as GPIO
import threading
import os
import random
import subprocess
import time
from datetime import datetime

def bashDelay(mystring):                                            # this function prints one character of the passed string at a time with a short delay in between, and without going to the next line
    for char in mystring:
        os.system('echo -n ' + char)
        time.sleep(0.25)
    time.sleep(0.5)
    os.system('echo DONE')
    os.system('echo \n')

# Just a fun joke to make it look like it's doing stuff as it "loads"
os.system('clear')
os.system('echo -n Building Bartberry Pi')
bashDelay('.....')
os.system('echo -n Writing bad jokes')
bashDelay('.....')
os.system('echo -n Kratzifying mainframe.SeasonOfSecrets')
bashDelay('................')
time.sleep(0.25)
os.system('clear')

# Admittedly I don't have a solid understanding of this, I grabbed it from "Resource A" listed above. Helps debounce my button
class ButtonHandler(threading.Thread):
    def __init__(self, pin, func, edge='both', bouncetime=200):
        #super(ButtonHandler,self).__init__()
        super().__init__(daemon=True)
        self.edge = edge
        self.func = func
        self.pin = pin
        self.bouncetime = float(bouncetime)/1000

        self.lastpinval = GPIO.input(self.pin)
        self.lock = threading.Lock()

    def __call__(self, *args):
        if not self.lock.acquire(blocking=False):
            return

        t = threading.Timer(self.bouncetime, self.read, args=args)
        t.start()

    def read(self, *args):
        pinval = GPIO.input(self.pin)

        if (
                ((pinval == 0 and self.lastpinval == 1) and
                 (self.edge in ['falling', 'both'])) or
                ((pinval == 1 and self.lastpinval == 0) and
                 (self.edge in ['rising', 'both']))
        ):
            self.func(*args)

        self.lastpinval = pinval
        self.lock.release()
    
    
playing = False                                                       # helps the system keep track of whether a video is playing, so it knows what the button press should do
directory = '/home/pi/Desktop/BARTBERRY_PI/RESOURCES/VIDEOS/'         # Where the videos are

# Mister Manager is the main function that the callback calls which determines what to do with a given button press
def misterManager(*args):
    global playing                                                    # I don't know if it's necessary to call the playing variable here since I'm not writing to it
    if not playing:                                                   # if a video isn't currently playing, play a video
        try:
            playVideo()
        except KeyboardInterrupt:
            GPIO.cleanup()
    else:                                                             # if a video is currently playing, stop it by killing omxplayer. In future builds, I'd love to build in functionality to be able to pause with a short button press, and stop altogether with a long button press. Knowing me this will never happen.
        try:
            kill_omxplayer()
        except KeyboardInterrupt:
            GPIO.cleanup()

def kill_omxplayer():                                                               # this kills whatever the player is playing
    global playing
    playing = False                                                                 # when you stop playing, you have to change the "playing" bool so Mister Manager knows what to do on the next button press
    os.system('sudo killall omxplayer.bin')                                         # os killall command

def playVideo():                                                                    # this randomly selects a video, kills the player if it's playing (not really necessary), and restarts with new video
    global playing
    os.system('sudo killall omxplayer.bin')
    playing = True                                                                  # don't forget to help out your ol' pal Mister Manager!
    episode = random.choice(os.listdir(directory))                                  # pick a video and pass it to the episode variable     
    cmd = "sudo omxplayer -b -o both "+"'"+directory+episode+"' &"                  # lays out the complete string that you'll pass to bash when you call the command as a subprocess   
    return subprocess.Popen(cmd, shell=True)                                        # plays the video via shell as a subprocess


GPIO.setmode(GPIO.BCM)                                                   # set your pinmode, children
GPIO.setup(4, GPIO.IN)                                                   # set up your pins, children
cb = ButtonHandler(4, misterManager, edge='rising', bouncetime=100)      # this sets up an instance of the ButtonHandler class for debouncing
cb.start()                                                               # initiates your ButtonHandler instance
os.system('sudo fbi -T 1 -a -noverbose RESOURCES/SPLASH.jpg')            # this calls the "fbi" module to show an image full-screen. I basically call this my splash page, which is what the TV shows when an episode isn't playing. By never actually killing this process, it'll show on screen immediately after the video player ends, without needing to re-call it
os.system('sudo omxplayer /home/pi/Desktop/BARTBERRY_PI/RESOURCES/merryxmas.mp3 -o both')     # Plays the splash screen SFX
GPIO.add_event_detect(4, GPIO.RISING, callback=cb)                       # starts listening for button presses and calls the cb ButtonHandler instance if it hears anything

# ok, this is a total hack and I know it's not great form. Basically, I had written all the above code and everything was working great from within Thonny, but I discovered once I started calling this from the command line that the entire script would STOP RUNNING and return to a command prompt after the previous line, which meant it stopped listening for button presses. So I threw this in at the last minute as a way to prevent the script from ever dying. Don't be like me.
nevertrue = False

def foreverloop():
    time.sleep(1000)
    if nevertrue:
        return
    else:
        foreverloop()
        
foreverloop()                                                    # I am ashamed.