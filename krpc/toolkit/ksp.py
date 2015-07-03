#! /usr/bin/env python3
# -*- coding: cp1252 -*-
# created on May 15, 2015 by Andreas

import krpc
import builtins

def connect(*args, **kwargs):
    """ primary connection setting global variables """
    cx = krpc.connect(*args, **kwargs)
    print('Connected to server, version {}'.format(cx.krpc.get_status()))
    return cx

def set_globals(cx):
    " add variables to builtins dict "
    builtins.SC = cx.space_center
    builtins.IR = cx.infernal_robotics 
    builtins.KAC = cx.kerbal_alarm_clock
    
