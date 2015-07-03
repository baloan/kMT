#! /usr/bin/env python3
# -*- coding: cp1252 -*-
# created on May 15, 2015 by Andreas

""" Surveyor class vessels staging sequence """

import krpc
import time


def surveyor1(name_):
    cx = krpc.connect(name=name_)
    print('Connected to server, version', cx.krpc.get_status().version)

    vessel = cx.space_center.active_vessel
    control = vessel.control
    resources = vessel.resources

    # wait for liftoff
    while vessel.situation.name == 'pre-launch':
        time.sleep(1)
        print("Vessel situation: {}".format(vessel.situation.name))

    with cx.stream(resources.amount, 'SolidFuel') as fuel:
        # fuel = resources.amount('SolidFuel')
        while fuel() > 0.1:
            time.sleep(0.1)
            print("Fuel: {}".format(fuel()))
        control.activate_next_stage()


    while True:
        lox = resources.amount('LiquidFuel')
        if lox < 0.1:
            control.activate_next_stage()
            break 
        time.sleep(0.1)
