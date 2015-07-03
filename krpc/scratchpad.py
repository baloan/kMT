#! /usr/bin/env python3
# -*- coding: cp1252 -*-
# created on May 22, 2014 by Andreas

import importlib

import krpc

from toolkit import ksp
from toolkit import nodes


cx = ksp.connect(name = 'Console')
ksp.set_globals(cx)
low_orbit = 80000
importlib.reload(nodes); nd = nodes.apoapsis(low_orbit)
importlib.reload(nodes); nodes.execute(nd)

# vec = krpc.schema.Geometry.Vector3()
# cx = krpc.connect(name = 'Console')
# print('Connected to server, version', cx.krpc.get_status().version)

space_center = cx.space_center
vessel = SC.active_vessel
orbit = vessel.orbit
control = vessel.control
auto_pilot = vessel.auto_pilot
flight = vessel.flight()
resources = vessel.resources

print(vessel.name)
print(orbit.body.name)

print(space_center.ReferenceFrame)
print(flight.g_force)

for p in vessel.parts.all:
    if len(p.resources.names) > 0:
        print(p.name)
        for n in p.resources.names:
            print("   {}, {}, ({}/{})".format(p.stage, n, p.resources.amount(n), p.resources.max(n)))

for e in vessel.parts.engines:
    print("{}, {}".format(e.part.name, e.has_fuel))
