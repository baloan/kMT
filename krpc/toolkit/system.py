#! /usr/bin/env python3
# -*- coding: cp1252 -*-
# created on May 15, 2015 by Andreas

import time

def checkvessel(name):
    try:
        vessel = SC.active_vessel
        if vessel.name != name:
            print("WARNING! This script maybe incompatible")
            print("Designed to work with {}".format(name))
            print("         Current ship {}".format(vessel.name))
            print("Press Ctrl-C within 5s to abort")
            print("-------------------------------------------------")
            time.sleep(5)
    except AttributeError as e:
        print("No active vessel!")
        print(e)

def tts():
    """ turn to sun - make sure solar panels are exposed """
    ap = SC.active_vessel.auto_pilot
    ap.set_rotation(-90, 0, 0, wait=True)
    
def met(secs):
    year = int(round(secs) / 7689600)
    day = int(round(secs) / 21600)
    hh = int((round(secs) % 21600) / 3600)
    mm = int((round(secs) % 3600) / 60)
    ss = int(round(secs) % 60)
    ts = "T+%1i.%02i %02i:%02i:%02i" % (year, day, hh, mm, ss)
    return ts

def mag(v):
    "magnitude"
    return v[0] * v[0] + v[1] * v[1] + v[2] * v[2]

def norm(v):
    m = mag(v)
    return (v[0] / mag, v[1] / mag, v[2] / mag) 

def vdot(v1, v2):
    " scalar vector product"
    return v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]
     
def vcross(v1, v2):
    " vector cross product "
    vr = (0, 0, 0)
    return vr
