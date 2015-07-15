#! /usr/bin/env python3
# -*- coding: cp1252 -*-
# created on May 15, 2015 by Andreas

import math
import time

import krpc

from toolkit import system


def execute(nd=None):
    if nd is None:
        nd = SC.active_vessel.control.nodes[0]
    vessel = SC.active_vessel
    orbit = vessel.orbit
    control = vessel.control
    auto_pilot = vessel.auto_pilot
    resources = vessel.resources
    flight = vessel.flight()

    body = orbit.body
    mu = body.gravitational_parameter  # gravitational parameter, mu = G mass
    rb = body.equatorial_radius  # radius of toolkit [m]
    # execute maneuver node
    print("Node in: {:.0f}, DeltaV: {:.1f}".format(nd.time_to, nd.delta_v))
    print("Node apoapsis: {:.0f}km, periapsis: {:.0f}km".format(
        nd.orbit.apoapsis / 1000, nd.orbit.periapsis / 1000))
    # print " Duration of burn: " + round(dob).
    print("Warping to maneuver...")
    SC.warp_to(nd.ut - 60)
    # turn does not work during warp - so do now
    print("Turning ship to burn direction.")
    # workaround for steering:pitch not working with node assigned
    auto_pilot.set_direction(
        nd.burn_vector(), roll=0, reference_frame=vessel.orbital_reference_frame)
    # SC.warp_to(nd.ut - 5)
    print("Orbital burn start {:.0f}s before apoapsis.".format(nd.time_to))
    # lock steering to node:prograde which wanders off at small deltav
    control.throttle = 1
    once = True
    done = False
    while not done:
        auto_pilot.set_direction(
            nd.burn_vector(), roll=90, reference_frame=vessel.orbital_reference_frame)
        maxa = vessel.available_thrust / vessel.mass
        tset = min(nd.remaining_delta_v / maxa, 1)
        if once and tset < 1:
            lox = resources.amount('LiquidFuel', cumulative=True)
            print(
                "Throttling down, remain dv {:.1f}m/s, fuel: {:.0f}".format(nd.remaining_delta_v, lox))
            once = False
        if system.vdot(nd.burn_vector(), nd.remaining_burn_vector()) < 0:
            print("End burn, remain dv {:.1f}m/s, vdot: {:.1f}".format(nd.remaining_delta_v,
                                                                       system.vdot(nd.burn_vector(), nd.remaining_burn_vector())))
            control.throttle = 0
            break
        if nd.remaining_delta_v < 0.1:
            print("Finalizing, remain dv {:.1f}m/s, vdot: {:.1f}".format(
                nd.remaining_delta_v, system.vdot(nd.burn_vector(), nd.remaining_burn_vector())))
            while system.vdot(nd.burn_vector(), nd.remaining_burn_vector()) > 0.5:
                pass
            control.throttle = 0
            print("End burn, remain dv {:.1f}m/s, vdot: {:.1f}".format(nd.remaining_delta_v,
                                                                       system.vdot(nd.burn_vector(), nd.remaining_burn_vector())))
            done = True
    control.throttle = 0
    nd.remove()
    print("Burn complete, apoapsis: {:.0f}km, periapsis {:.0f}km".format(
        orbit.apoapsis / 1000, orbit.periapsis / 1000))
    lox = resources.amount('LiquidFuel', cumulative=True)
    print("Fuel after burn: {}".format(lox))


def apoapsis(alt):
    # set context
    vessel = SC.active_vessel
    orbit = vessel.orbit
    control = vessel.control
    body = orbit.body
    flight = vessel.flight(reference_frame=body.non_rotating_reference_frame)
    body = orbit.body
    mu = body.gravitational_parameter  # gravitational parameter, mu = G mass
    rb = body.equatorial_radius  # radius of toolkit [m]
    # create apoapsis maneuver node
    print("Apoapsis maneuver, orbiting {}".format(body.name))
    print("Apoapsis: {:.0f}km".format(orbit.apoapsis / 1000))
    print("Periapsis: {:.0f}km -> {:.0f}km".format(orbit.periapsis / 1000, alt / 1000))
    # present lko properties
    vom = flight.speed  # actual velocity
    r = rb + flight.mean_altitude  # actual distance to toolkit
    ra = orbit.apoapsis  # radius in apoapsis
    # velocity in apoapsis
    va = math.sqrt(vom**2 + 2 * mu * (1 / ra - 1 / r))
    a = (orbit.periapsis + orbit.apoapsis) / 2  # semi major axis present lko
    # future lko properties
    r2 = orbit.apoapsis  # distance after burn at apoapsis
    a2 = (alt + rb + orbit.apoapsis) / 2  # semi major axis target lko
    v2 = math.sqrt(vom**2 + (mu * (2 / r2 - 2 / r + 1 / a - 1 / a2)))
    # setup node
    deltav = v2 - va
    print("Apoapsis burn: {:.1f}, dv: {:.1f} -> {:.1f} m/s".format(va, deltav, v2))
    nd = control.add_node(SC.ut + orbit.time_to_apoapsis, deltav, 0, 0)
    print("Node created.")
    return nd


def perinode(alt):
    pass


def hohnode():
    pass


def incnode():
    pass
