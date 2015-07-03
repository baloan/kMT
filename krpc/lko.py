#!/usr/bin/env python3
# -*- coding: cp1252 -*-
# created on May 21, 2014 by baloan

"""
Launch to orbit (with atmosphere)
"""

from threading import Thread

import krpc

from toolkit import ksp
from toolkit import launch
from toolkit import system
from toolkit import warp
from vessels import surveyor, stock

STAGING_DICT = {
        "Surveyor 1": surveyor.surveyor1,
        "Kerbal X": stock.default,
    } 

def main():
    cx = ksp.connect(name='Trajectory')
    ksp.set_globals(cx)
    # system.checkvessel("Surveyor 1")
    # warp.warpday()
    # setup staging
    try:
        staging = STAGING_DICT[SC.active_vessel.name]
    except KeyError:
        staging = stock.default
    stage = Thread(target=staging, args=["Staging", ])
    # launch to orbit
    stage.start()
    launch.ltoa()
    system.tts()
    

if __name__ == "__main__":
    main()
