#!/usr/bin/env python3
"""
Shows how to toss a capsule to a container.
"""
from mujoco_py import load_model_from_path, MjSim, MjViewer
import numpy as np
import sys

model = load_model_from_path("xmls/sensor_force_xy.xml")
sim = MjSim(model)

viewer = MjViewer(sim)


global t
t=0
force_list = np.empty([0,3])
pos_list = np.empty([0,3])
save ='False'

x_step = 2
y_step = 1
z_step = 1

x_step_size = 0.04
y_step_size = 0.001
z_step_size = 0.001

x_list = np.linspace(0, (x_step-1)*x_step_size, x_step)
y_list = np.linspace(0, (y_step-1)*y_step_size, y_step)
z_list = -np.linspace(z_step_size, (z_step)*z_step_size, z_step)
gear   = 50

def simulate():
    global t
    sim.step()
    viewer.render()
    t +=1

def move(force_list,pos_list,x,y,z):
    # sensor feedback
    sim.data.get_sensor('F/T')
    force = sim.data.sensordata[:3]
    pos = sim.data.sensordata[3:]
    while np.abs(pos[0]-x-(-0.02))>4e-5 or np.abs(pos[1]-y-0.002)>4e-5 or np.abs(pos[2]-z-0.0480)>4e-6:
        simulate()

        # sensor feedback
        sim.data.get_sensor('F/T')
        force = sim.data.sensordata[:3]
        pos = sim.data.sensordata[3:]

        
        sim.data.ctrl[1]=y*gear
        sim.data.ctrl[2]=z*gear*2
        if np.abs(pos[2] -0.048+z_step_size)>4e-6:
            sim.data.ctrl[0]=x*gear
            # print(np.abs(pos[2] -0.001))
        else:
            sim.data.ctrl[3]=0.5

        force_list,pos_list = save(force_list,pos_list,x,y,z)

        if t%100 ==0:
            print("time:{}, force: {}, position: {}".format(t,force[2],pos))
    return force_list,pos_list

def save(force_list,pos_list,x,y,z):
    # move(x,y,z)

    sim.data.get_sensor('F/T')
    force = np.reshape(sim.data.sensordata[:3],(1,3))
    pos = np.reshape(sim.data.sensordata[3:],(1,3))

    force_list = np.concatenate((force_list,force))
    pos_list = np.concatenate((pos_list,pos))

    return force_list,pos_list


while True:



    # move
    for z in z_list:
        for x in x_list:
            # probe
            for y in y_list:
                force_list,pos_list = move(force_list,pos_list,x,y,z)
                force = sim.data.sensordata[:3]
                pos = sim.data.sensordata[3:]
                pos = [np.round(pos[0],4),np.round(pos[1],4),np.round(pos[2],5)]
                print("time:{}, force: {}, position: {}".format(t,force[2],pos))
    np.savez('data',force=force_list, pos=pos_list)
    sys.exit()

