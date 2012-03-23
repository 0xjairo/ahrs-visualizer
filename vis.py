#!/usr/bin/python

import visual as v
import serial

try:
    ser = serial.Serial('/dev/ttyACM0', 9600)
    ser.timeout=0
except : #SerialException:
    ser = None

if ser == None:
    #f = open('log-short.0', 'r')
    f = open('screenlog.0', 'r')

#ball = v.sphere(pos=(-6,0,0), radius=0.5, color=v.color.cyan)
copter = v.box(pos=(0,-5,0), size=(5,0.2,3), color=v.color.green)

#ball.velocity = v.vector(25,0,0)
vscale = 1

# x arrow
xarr = v.arrow(pos=copter.pos, axis=vscale*copter.pos, color=v.color.yellow)

deltat = 0.005
t = 0

if ser == None:
    line =  f.readline()
else:
    line =  ser.readline()

v.scene.autoscale = False
i=0
while len(line)>0:

    v.rate(10)

    if ser == None:
        line =  f.readline()
    else:
        line =  ser.readline()

    s = line.split(' ')
    d = dict()
    for token in s:
        kv = token.split(':')
        if(kv != -1 and len(kv) == 2):
            d[kv[0]] = kv[1]

    try:
        roll = float(d['y'])
    except KeyError:
        roll = 0
        ''' do nothing '''

    print roll

    #copter.rotate(angle=v.radians(i))
    copter.rotate(angle=v.radians(roll))
    i += 0.1
    t = t + deltat

print 'Done!'

if ser == None:
    f.close()
else:
    ser.close()

