#! /usr/bin/env python3
# -*- coding: cp1252 -*-
# created on May 16, 2015 by Andreas

import math


def warpday():
    """ wait for sunrise 
    prerequisite: on the ground
    use importlib.reload(warp) in interactive mode 
    """
    vessel = SC.active_vessel
    # x axis points anti-radial, i.e. towards the Sun
    frm = vessel.orbit.body.orbital_reference_frame
    ps = vessel.position(frm)
    a = math.degrees(math.atan2(ps[1], ps[0]))
    # adjust atan negative results to a [0, 360] interval
    if a < 0:
        a = 360 + a
    # 0 degrees means sun is in zenith, Kerbin rotates counterclockwise
    if a > 90 and a < 270:
        print("Waiting for sunrise...")
        rs = math.degrees(vessel.orbit.body.rotational_speed)
        waita = a - 90
        wt = waita / rs
        SC.warp_to(SC.ut + wt)
    else:
        print("Nothing to do during daytime.")
