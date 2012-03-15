#!/usr/bin/python

import visual as v
import serial

ser = serial.Serial('/dev/ttyACM0', 9600)
ser.timeout=0

ball = v.sphere(pos=(-6,0,0), radius=0.5, color=v.color.cyan)
copter = v.box(pos=(0,-5,0), size=(5,0.2,3), color=v.color.green)

ball.velocity = v.vector(25,0,0)
vscale = 1

# x arrow
xarr = v.arrow(pos=copter.pos, axis=vscale*copter.pos, color=v.color.yellow)

deltat = 0.005
t = 0

v.scene.autoscale = False
while t<3:

    v.rate(100)

    line =  ser.readline()
    if len(line) > 0:
        print line

    if ball.pos.x > 6 or ball.pos.x < -6:
        ball.velocity.x = -ball.velocity.x

    #xarr.pos = ball.pos
    #xarr.axis = vscale*ball.velocity

    ball.pos = ball.pos + ball.velocity*deltat
    t = t + deltat

ser.close()
