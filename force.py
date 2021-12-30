#!/usr/bin/env python3
"""
Shows how to toss a capsule to a container.
"""
from mujoco_py import load_model_from_path, MjSim, MjViewer
import numpy as np
import sys

model = load_model_from_path("xmls/sensor_force.xml")
sim = MjSim(model)

viewer = MjViewer(sim)


global t
t=0
force_list = np.empty([0,3])
pos_list = np.empty([0,3])
save ='False'

x_step = 5
y_step = 5
z_step = 10

x_step_size = 0.001
y_step_size = 0.001
z_step_size = 0.0001

x_list = np.linspace(-2*x_step_size, 2*x_step_size, x_step)
y_list = np.linspace(-2*y_step_size, 2*y_step_size, y_step)
z_list = -np.linspace(0.01+z_step_size, 0.01+z_step*z_step_size, z_step)
gear   = 30

def simulate():
    global t
    sim.step()
    viewer.render()
    t +=1

def move(x,y,z):
    # sensor feedback
    sim.data.get_sensor('F/T')
    force = sim.data.sensordata[:3]
    pos = sim.data.sensordata[3:]
    while np.abs(pos[0]-x-0)>1e-4 or np.abs(pos[1]-y-0.00)>1e-4 or np.abs(pos[2]-z-0.058)>1e-5:
        simulate()

        # sensor feedback
        sim.data.get_sensor('F/T')
        force = sim.data.sensordata[:3]
        pos = sim.data.sensordata[3:]

        sim.data.ctrl[0]=x*gear
        sim.data.ctrl[1]=y*gear
        sim.data.ctrl[2]=z*gear*2
        # if t%100 ==0:
        #     print("time:{}, force: {}, position: {}".format(t,force[2],pos))

def save(force_list,pos_list,x,y,z):
    move(x,y,z)

    sim.data.get_sensor('F/T')
    force = np.reshape(sim.data.sensordata[:3],(1,3))
    pos = np.reshape(sim.data.sensordata[3:],(1,3))

    force_list = np.concatenate((force_list,force))
    pos_list = np.concatenate((pos_list,pos))

    return force_list,pos_list


while True:

    # simulate()


    # move
    for x in x_list[2:3]:
        for y in y_list[2:4]:
            move(x,y,0)
            move(x,y,-0.01)
            # probe
            for z in z_list:
                for i in range(10):
                    move(x,y,z)
                force_list,pos_list = save(force_list,pos_list,x,y,z)
                force = sim.data.sensordata[:3]
                pos = sim.data.sensordata[3:]
                pos = [np.round(pos[0],4),np.round(pos[1],4),np.round(pos[2],5)]
                print("time:{}, force: {}, position: {}".format(t,force[2],pos))
            move(x,y,-0.01)
            move(x,y,0)
    np.savez('data',force=force_list, pos=pos_list)
    sys.exit()



        # simulate()

        # # sensor feedback
        # sim.data.get_sensor('F/T')
        # force = sim.data.sensordata[:3]
        # pos = sim.data.sensordata[3:]

        # # if t<601:
        # #         force_list[t-1]=force
        # #         pos_list[t-1] = pos
        # # elif save =='False':
        # #         save = 'True'
        # #         np.savez('data',force=force_list, pos=pos_list)

        # # gear = 10
        # if t<0.01/0.001*10:
        #         # t:0-100, ctrl:0 -> -0.1
        #         sim.data.ctrl[2] = -t*0.001
        # elif t<0.01/0.001*10+100:
        #         # t:100-200, ctrl:-0.1
        #         sim.data.ctrl[2] = -0.1
        # elif t<0.01/0.001*10+100+100:
        #         # t:200-300, ctrl:-0.1 -> -0.11
        #         sim.data.ctrl[2] = -0.1-(t-200)*0.0001
        # elif t<0.01/0.001*10+100+100+100:
        #         # t:300-400, ctrl:-0.11
        #         sim.data.ctrl[2] = -0.11
        # elif t<0.01/0.001*10+100+100+100+100:
        #         # t:400-500, ctrl:-0.11 -> -0.12
        #         sim.data.ctrl[2] = -0.11-(t-400)*0.0001
        # else:
        #         sim.data.ctrl[2] = -0.12



        # # if pos>0.045 and flag == "no_touch":
        # #         sim.data.ctrl[0] = -t*0.001
        # # else:
        # #         flag="touch"




        # print("time:{}, force: {}, position: {}".format(t,force,pos))

