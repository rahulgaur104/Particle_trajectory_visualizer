#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 16:24:12 2020

Solves the equation of motion for a static background magnetic field,
the tangent plane of which can be described analytically, as a bunch
of nested circular tori.

Provision for adding the electric field.

Used to trace path of charged particles by solving the equation of 
motion using a famous algorithm called the Boris algorithm in plasma
physics.

Note that this code uses mayavi package to create animations and 3D 
graphics which only works with a specific system configuration. 

Don't use python >3.6 with qt5 backend as it renders incorrect 
visualization. For more information look up the issue #656 with 
Mayavi on Github

@author: ralap
"""

import numpy as np
from mayavi import mlab
import math as mx
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import os
import math as mx
import pdb


out_path = './'
out_path = os.path.abspath(out_path)
fps = 20
prefix = 'ani'
ext = '.png'

#Radial postion of the magnetic axis in cylindrical coords
R_0 = 150.0

qdm = 1E7   # q/m for electrons for H+ ion q/m ~ 1E5

c = 3E10    # speed of light in cgs
r = 50      # radius of the circular tangent surface from 
            # the magnetic axis

duration = 8000  # number of steps
dt = 150         # time step. There is probably an upper limit?

nu = 1           # the local safety factor also = q for large eps

tilt = r/(nu*(R_0+r)) # tilt of the magnetic field line at the 
                      # starting point. Not neccesary but I wanted
                      # the particle to have 0 v_perp

#v = np.array([6E-3, 9E-3, 8E-4]);
v = np.array([0, 5E-3, 0.])
v[2] = tilt*v[1]                # shooting the particle with no 
                                # v_perp

x = np.array([R_0+r, 0., 0.])   # particle initial position vector

E = np.array([0., 0., 0.])      # particle initial energy
En = np.zeros((duration,))      # particl energy at each time step
r_diff = np.zeros((duration,))  # radial displacement from a flux 
                                # surface
X = np.zeros((duration,3))      # array to store all the positions 
V = np.zeros((duration,3))      #   "    "   "    "   "  velocities

c1 = qdm*dt             
c2 = c1/c
A = 5


for time in range(duration):
    
    # calculating coordiante values in a different coord system
    r = mx.sqrt((mx.sqrt(x[0]**2 + x[1]**2)-R_0)**2 + x[2]**2)
    th = mx.atan2(x[2], (mx.sqrt(x[0]**2 + x[1]**2)-R_0))   
    phi = mx.atan2(x[1], x[0])  #Y/X
    
    sth, cth = mx.sin(th), mx.cos(th)
    sphi,  cphi = mx.sin(phi), mx.cos(phi)
    
    r_diff[time] = r - 50 

    R = R_0 + r*cth
    fac1 = -r/(nu*R)
    
    # Poloidal current
    I = A*r
    
    #Magnetic field vector in cartesian coords
    B = I/R*np.array([fac1*sth*cphi - sphi, fac1*sth*sphi + cphi, -fac1*cth])
    
    # Boris algorithm at work 
    A_plus = np.eye(3) + c2*np.cross(np.eye(3), B)
    A_minus = np.eye(3) - c2*np.cross(np.eye(3), B)
    S = np.linalg.inv(A_plus)
    R = np.dot(S, A_minus)
    v = np.dot(v, R.T) + c1*np.dot(S, E)
    x = x + dt*np.dot(v, R.T) +c1*dt*np.dot(S, E)     
    
    X[time,:] = x;
    V[time,:] = v; 
    
   
padding = len(str(len(X[:,0])))
p = mlab.plot3d(X[:,0], X[:,1], X[:,2], color = (0, 1, 0), line_width = 0.5, tube_radius = 1.5, opacity=1.0)
l = mlab.points3d(X[:,0], X[:,1], X[:,2], color = (1, 0, 0), scale_factor=3, opacity=1.0)


# Torus and geodesic potting routine
angle = np.linspace(0, 2 * np.pi, 60)
th1, phi1 = np.meshgrid(angle, angle)
r = 50 
X1 = (R_0 + r * np.cos(th1)) * np.cos(phi1)
Y1 = (R_0 + r * np.cos(th1)) * np.sin(phi1)
Z1 = r * np.sin(th1)

k = mlab.mesh(X1, Y1, Z1, color=(0, 0, 1), opacity=0.05)


om1 = 5
om2 = 5*nu
t = np.linspace(0, 1.3, 1000)
th2  = om1*t
phi2 = om2*t

X2 = (R_0 + r * np.cos(th2)) * np.cos(phi2)
Y2 = (R_0 + r * np.cos(th2)) * np.sin(phi2)
Z2 = r * np.sin(th2)

n = mlab.plot3d(X2, Y2, Z2, line_width = 1, tube_radius = 1)
view =(45.0, 54.735610317245346, 922.1768108681829, np.array([ 8.72923975e-01,  1.42108547e-14, -9.06810760e-02]))

mlab.view(*view)

#mlab.savefig('check.png')



len1 = np.shape(X)[0]
ms0 = p.mlab_source
ms1 = l.mlab_source
ms2 = k.mlab_source
#mlab.options.offscreen = True



@mlab.animate(delay = 10)
def updateAnimation():
    fig = mlab.gcf()
    scene = fig.scene
    scene.disable_render = True
    mlab.view(*view)
    #scene.renderer.set(use_depth_peeling=True)

    for i in range(len1):
        #x1 = np.asarray(X[0:i+1, 0], 'd')
        #y1 = np.asarray(X[0:i+1, 1], 'd') 
        #z1 = np.asarray(X[0:i+1, 2], 'd')    
        ms2.set(u = np.array([0, 0]),v =  np.array([0, 0]), w = np.array([0, 3*np.max(X[:,2])]))
        ms0.reset(x = X[0:i+1, 0], y= X[0:i+1, 1], z= X[0:i+1, 2])
        ms1.set(x = X[i, 0], y = X[i, 1], z = X[i, 2])
        #fig.scene.reset_zoom()
        
        # create zeros for padding index positions for organization
        zeros = '0'*(padding - len(str(i)))
        
        # concate filename with zero padded index number as suffix
        filename = os.path.join(out_path, '{}_{}{}{}'.format(prefix, zeros, i, ext))

        mlab.savefig(filename=filename)
        yield
        
    scene.disable_render = False
  
updateAnimation()

mlab.show()


"""
fig1 = plt.figure()
plt.plot(dt*np.linspace(1,duration,duration), r_diff, '-k', linewidth=1.5)
plt.savefig("test.png")
ax = plt.axes(xlim=(0, duration), ylim=(-0.5,0.5))
line, = ax.plot([], [], lw=3) 

def initial():
    line.set_data([], [])
    return line,

#pdb.set_trace()
def anim(i):
    #r_diff = r*np.ones((i+1,)) - np.sqrt((np.sqrt(X[0:i+1,0]**2 + X[0:i+1,1]**2)-R_0)**2 + X[0:i+1,2]**2)
    dt_vec = dt*np.linspace(1,i,i+1)
    line.set_data(dt_vec, r_diff[0:i+1])
    return line,

anim = FuncAnimation(fig1, anim, init_func=initial, frames = 5000, interval = 1, blit=True)
anim.save('distance_torus.gif', writer='imagemagick')
"""



















    
    
