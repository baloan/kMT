#! /usr/bin/env python3
# -*- coding: cp1252 -*-
# created on May 20, 2015 by Andreas

import krpc
import time


def default(name_):
    cx = krpc.connect(name=name_)
    print('Connected to server, version', cx.krpc.get_status().version)

    vessel = cx.space_center.active_vessel
    control = vessel.control
    resources = vessel.resources

    # wait for liftoff
    while vessel.situation.name == 'pre-launch':
        time.sleep(1)
        print("Vessel situation: {}".format(vessel.situation.name))

    while True:
        for e in vessel.parts.engines:
            if not e.has_fuel:
                control.activate_next_stage()
                break
        time.sleep(0.5)
    