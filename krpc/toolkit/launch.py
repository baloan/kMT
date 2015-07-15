#! /usr/bin/env python3
# -*- coding: cp1252 -*-
# created on May 15, 2015 by Andreas

from toolkit.system import met
from toolkit import nodes

import sys
import krpc
import time
import math

# convert to dict with altitude and linear coefficients
# angle = a * altitude + b
# y = a x + b

DEFAULT_PROFILE = [
    (0, 90),
    (7000, 80),
    (25000, 30),
    (50000, 0),
]


def ltoa(ascent_profile=DEFAULT_PROFILE):
    """ launch to lko in atmosphere
    target_periapsis
    target_apoapsis
    target_inclination
    """
    vessel = SC.active_vessel
    orbit = vessel.orbit
    control = vessel.control
    auto_pilot = vessel.auto_pilot
    flight = vessel.flight()
    # parts = vessel.parts
    # resources = vessel.resources

    # calculate pitch legs
    pitch_legs = []
    for i in range(len(ascent_profile) - 1):
        j = i + 1
        dx = ascent_profile[j][0] - ascent_profile[i][0]
        dy = ascent_profile[j][1] - ascent_profile[i][1]
        a = dy / dx
        b = ascent_profile[i][1] - a * ascent_profile[i][0]
        pitch_legs.insert(0, (ascent_profile[i][0], (a, b)))
    pitch_legs.insert(0, (ascent_profile[j][0], (0, 0)))

    print(pitch_legs)
    # sys.exit(0)

    body = orbit.body
    mu = body.gravitational_parameter  # gravitational parameter, mu = G mass
    rb = body.equatorial_radius  # radius of body [m]
    ha = body.atmosphere_depth  # atmospheric height [m]

    # gravity turn parameters
    low_orbit = 80000  # low lko altitude [m]
    # velocity parameters
    maxq = 8000

    print("Launch program start at: {:.0}".format(SC.ut))
    control.throttle = 1
    auto_pilot.set_rotation(90, 90)
    vsfc = vessel.velocity(vessel.surface_reference_frame)
    vobt = vessel.velocity(body.non_rotating_reference_frame)
    # lock steering to up + R(0, 0, -180)
    print("T-1  All systems GO. Ignition!")
    # control.activate_next_stage()
    time.sleep(1)
    print(met(vessel.met) + " Ignition.")
    control.activate_next_stage()
    print(met(vessel.met) + " Liftoff.")
    # control speed and attitude
    while orbit.apoapsis_altitude < low_orbit:
        facing = flight.direction
        vel = flight.velocity
        speed = flight.speed
        ma = flight.mean_altitude
        # control attitude
        # target pitch
        for mina, coeff in pitch_legs:
            if ma > mina:
                a, b = coeff
                target_pitch = a * ma + b
                break
        pitch = flight.pitch
        auto_pilot.set_rotation(target_pitch, 90, 90)
        # dynamic pressure q
        q = flight.dynamic_pressure
        vl = maxq * 0.9
        vh = maxq * 1.1
        if q < vl:
            qfac = 1
        if q > vl and q < vh:
            qfac = (vh - q) / (vh - vl)
        if q > vh:
            qfac = 0
        control.throttle = qfac
        print("q: {:5.0f} pitch: flight {:2.1f}, target {:2.1f}".format(q, pitch, target_pitch))
        #print("tta: {:3.0f} q: {:5.0f} pitch: flight {:2.1f}, target {:2.1f}".format(tta, q, pitch, target_pitch))
        time.sleep(0.5)
    control.throttle = 0
    # auto_pilot.set_direction(flight.direction, roll=90, wait=True)
    auto_pilot.set_direction(flight.direction, roll=0, wait=True)
    print("Waiting to leave atmosphere {:.0f}km".format(body.atmosphere_depth / 1000))
    while flight.mean_altitude < body.atmosphere_depth:
        time.sleep(1)
    nd = nodes.apoapsis(low_orbit)
    nodes.execute(nd)
    auto_pilot.disengage()
    print("attitude control terminated.")
