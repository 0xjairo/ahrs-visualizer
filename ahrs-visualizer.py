#!/usr/bin/python
# Code downloaded from on MAR-2012: 
# http://edge.rit.edu/content/P11015/public/Visual%20Python%20for%20Gyroscope%20Utilization.py
# The original code has been modified to read the output from the tricopter at
# https://github.com/jyros/tricopter

# Test for Razor 9DOF IMU
# Jose Julio @2009
# This script needs VPhyton, pyserial and pywin modules

# First Install Python 2.6.4
# Install pywin from http://sourceforge.net/projects/pywin32/
# Install pyserial from http://sourceforge.net/projects/pyserial/files/
# Install Vphyton from http://vpython.org/contents/download_windows.html

from visual import *
import serial
import string
import math
import sys
import datetime

# LeafLabs Maple serial port
serialport = '/dev/ttyacm0'

# Check your COM port and baud rate
try:
    ser = serial.serial(serialport)
except serial.SerialException:
    print "Serial port not found"
    sys.exit(0)

# Main scene
scene=display(title="9DOF Razor IMU test")
scene.range=(1.2,1.2,1.2)
#scene.forward = (0,-1,-0.25)
scene.forward = (1,0,-0.25)
scene.up=(0,0,1)

# Second scene (Roll, Pitch, Yaw)
scene2 = display(title='9DOF Razor IMU test',x=0, y=0, width=500, height=200,center=(0,0,0), background=(0,0,0))
scene2.range=(1,1,1)
scene.width=500
scene.y=200

scene2.select()
#Roll, Pitch, Yaw
cil_roll = cylinder(pos=(-0.4,0,0),axis=(0.2,0,0),radius=0.01,color=color.red)
cil_roll2 = cylinder(pos=(-0.4,0,0),axis=(-0.2,0,0),radius=0.01,color=color.red)
cil_roll_bg = cylinder(pos=(-0.4,0,0),axis=(0.2,0,0),radius=0.01,color=(1,1,1),opacity=0.25)#color.yellow)
cil_roll2_bg = cylinder(pos=(-0.4,0,0),axis=(-0.2,0,0),radius=0.01,color=(1,1,1),opacity=0.25)#color.yellow)
cil_pitch = cylinder(pos=(0.1,0,0),axis=(0.2,0,0),radius=0.01,color=color.green)
cil_pitch2 = cylinder(pos=(0.1,0,0),axis=(-0.2,0,0),radius=0.01,color=color.green)
#cil_course = cylinder(pos=(0.6,0,0),axis=(0.2,0,0),radius=0.01,color=color.blue)
#cil_course2 = cylinder(pos=(0.6,0,0),axis=(-0.2,0,0),radius=0.01,color=color.blue)
arrow_course = arrow(pos=(0.6,0,0),color=color.cyan,axis=(-0.2,0,0), shaftwidth=0.02, fixedwidth=1)

#Roll,Pitch,Yaw labels
label(pos=(-0.4,0.3,0),text="Roll",box=0,opacity=0)
label(pos=(0.1,0.3,0),text="Pitch",box=0,opacity=0)
label(pos=(0.55,0.3,0),text="Yaw",box=0,opacity=0)
label(pos=(0.6,0.22,0),text="N",box=0,opacity=0,color=color.yellow)
label(pos=(0.6,-0.22,0),text="S",box=0,opacity=0,color=color.yellow)
label(pos=(0.38,0,0),text="W",box=0,opacity=0,color=color.yellow)
label(pos=(0.82,0,0),text="E",box=0,opacity=0,color=color.yellow)
label(pos=(0.75,0.15,0),height=7,text="NE",box=0,color=color.yellow)
label(pos=(0.45,0.15,0),height=7,text="NW",box=0,color=color.yellow)
label(pos=(0.75,-0.15,0),height=7,text="SE",box=0,color=color.yellow)
label(pos=(0.45,-0.15,0),height=7,text="SW",box=0,color=color.yellow)

L1 = label(pos=(-0.4,0.22,0),text="-",box=0,opacity=0)
L2 = label(pos=(0.1,0.22,0),text="-",box=0,opacity=0)
L3 = label(pos=(0.7,0.3,0),text="-",box=0,opacity=0)

# Main scene objects
scene.select()
# Reference axis (x,y,z)
arrow(color=color.green,axis=(1,0,0), shaftwidth=0.02, fixedwidth=1)
arrow(color=color.green,axis=(0,-1,0), shaftwidth=0.02 , fixedwidth=1)
arrow(color=color.green,axis=(0,0,-1), shaftwidth=0.02, fixedwidth=1)
# labels
label(pos=(0,0,0.8),text="9DOF Razor IMU test",box=0,opacity=0)
label(pos=(1,0,0),text="X",box=0,opacity=0)
label(pos=(0,-1,0),text="Y",box=0,opacity=0)
label(pos=(0,0,-1),text="Z",box=0,opacity=0)
# IMU object
platform = box(length=1, height=0.05, width=1, color=color.red)
p_line = box(length=1,height=0.08,width=0.1,color=color.yellow)
plat_arrow = arrow(color=color.green,axis=(1,0,0), shaftwidth=0.06, fixedwidth=1)

now = datetime.datetime.now()

f = open("Serial_"+ now.strftime("%Y%m%d%H%M%S") +".txt", 'w')

roll=0
pitch=0
yaw=0

line = ser.readline()
while len(line)>0:
    #rate(10)

    #line = line.replace("!RAW:","")   # Delete "!ANG:"
    #print line
    f.write(line)                     # Write to the output log file

    # split line
    s = line.split(' ')
    d = dict()

    # go through key/value pairs (i.e.: roll:3.4)
    for token in s:
        kv = token.split(':')
        if(kv != -1 and len(kv) == 2):
            d[kv[0]] = kv[1]

    try:
        roll = round(radians(float(d['yRoll'])),2)
        pitch = round(radians(float(d['yPitch'])),2)
        yaw = radians(180) #round(radians(float(d['yYaw'])),2)
        uroll = round(radians(float(d['uRoll'])),2)
        #print line,
    except KeyError:
        print 'invalid line'
        roll = 0
        pitch = 0
        yaw = radians(180)
        ''' do nothing '''


    if True:
        axis=(cos(pitch)*cos(yaw),-cos(pitch)*sin(yaw),sin(pitch)) 
        up=(sin(roll)*sin(yaw)+cos(roll)*sin(pitch)*cos(yaw),sin(roll)*cos(yaw)-cos(roll)*sin(pitch)*sin(yaw),-cos(roll)*cos(pitch))
        platform.axis=axis
        platform.up=up
        platform.length=1.0
        platform.width=0.65
        plat_arrow.axis=axis
        plat_arrow.up=up
        plat_arrow.length=0.8
        p_line.axis=axis
        p_line.up=up
        cil_roll.axis=(0.2*cos(roll),0.2*sin(roll),0)
        cil_roll2.axis=(-0.2*cos(roll),-0.2*sin(roll),0)
        cil_roll_bg.axis=(0.2*cos(uroll),0.2*sin(uroll),0)
        cil_roll2_bg.axis=(-0.2*cos(uroll),-0.2*sin(uroll),0)
        cil_pitch.axis=(0.2*cos(pitch),0.2*sin(pitch),0)
        cil_pitch2.axis=(-0.2*cos(pitch),-0.2*sin(pitch),0)
        arrow_course.axis=(0.2*sin(yaw),0.2*cos(yaw),0)
        L1.text = str(roll)
        L2.text = str(pitch)
        L3.text = str(yaw)        
        #L1.text = str(float(words[0]))
        #L2.text = str(float(words[1]))
        #L3.text = str(float(words[2]))        
    line = ser.readline()

print 'done'
ser.close
f.close

