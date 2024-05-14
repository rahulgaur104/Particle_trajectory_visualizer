#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21  2020

@author:  Rahul Gaur

Based on the application of the Boris algorithm for straight magnetic and electric field.

This code will have radially varying B field to show the effect of grad B drift.

Since one doesn't need any derivatives of the fields while time marching,
using r, theta, phi(orthogonal) coordinates shouldn't be dificult at all.
The only thing we need to ensure is that B is divergence-less.
"""

import math as mx
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mayavi import mlab
import os
import subprocess

#from matplotlib import rc

#rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
#rc('text', usetex=True)


out_path = './'
out_path = os.path.abspath(out_path)
fps = 20
prefix = 'ani'
ext = '.png'

qdm = 1E7   # q/m for electrons for H+ ion q/m ~ 1E5
c = 3E10;
fraim = 50
duration = 1250;
dt = 1.5E2

#v = np.array([6E-3, 9E-3, 8E-4]);
v = np.array([-3E-2, 7E-2, -3E-2])
x = np.array([800., 0., 0.]);

E = np.array([0., 0., 0.]);
En = np.zeros((duration,))
X = np.zeros((duration,3)) 
V = np.zeros((duration,3)) 

c1 = qdm*dt
c2 = c1/c

C = 5000


for time in range(duration):
    r = mx.sqrt(x[0]**2 + x[1]**2)
    th = mx.atan2(x[1], x[0])
    B = np.array([-C/r*mx.sin(th), C/r*mx.cos(th), 0]);
    #print(np.linalg.norm(B))
    A_plus = np.eye(3) + c2*np.cross(np.eye(3), B)
    A_minus = np.eye(3) - c2*np.cross(np.eye(3), B)
    S = np.linalg.inv(A_plus)
    R = np.dot(S, A_minus)
    v = np.dot(v, R.T) + c1*np.dot(S, E)
    x = x + dt*np.dot(v, R.T) +c1*dt*np.dot(S, E)     
    X[time,:] = x;
    V[time,:] = v; 
    En[time] = np.linalg.norm(V[time,:])





padding = len(str(len(X[:,0])))

p = mlab.plot3d(X[:,0], X[:,1], X[:,2], color = (0, 1, 0), line_width = 2, tube_radius = 8, opacity=1.0)
l = mlab.points3d(X[:,0], X[:,1], X[:,2], color = (1, 0, 0), scale_factor=20, opacity=1.0)
#k = mlab.quiver3d(np.array([ np.max(X[:,0])/2, np.max(X[:,0])/2]), np.array([0, 0]), \
#                  np.array([0, -np.max(X[:,2])]), np.array([0, 0]), \
#                      np.array([0, 0]), np.array([0, np.max(X[:,2])]), line_width = 2, mode='arrow', scale_factor = 1)
#n = 
#k = mlab.quiver3d(np.array([ np.max(X[:,0])/2, np.max(X[:,0])/2]), np.array([0, 0]), \
#              np.array([0, np.max(X[:,2])]), np.array([0, 0]), \
#                  np.array([0, 0]), np.array([0, 1]),  mode='cone', scale_factor = 200, opacity=1.0)
q = mlab.plot3d(810*np.cos(np.linspace(0, 2*np.pi, 100)), -810*np.sin(np.linspace(0, 2*np.pi, 100)), -0*np.ones((100,)), color = (0, 0, 1), line_width = 2, tube_radius = 2)
#p.actor.property.frontface_culling = True
#l.actor.property.frontface_culling = True
#k.actor.property.frontface_culling = True


len1 = np.shape(X)[0]
ms0 = p.mlab_source
ms1 = l.mlab_source
#ms2 = k.mlab_source
#mlab.options.offscreen = True

view = (-19.50365831538248, 69.25854702395637, 2524.5257190021084, np.array([ 51.08986294, -29.24448555, -88.22708967]))

#@mlab.animate(delay = 10)
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
        #ms2.set(u = np.array([0, 0]),v =  np.array([0, 0]), w = np.array([0, 3*np.max(X[:,2])]))
        ms0.reset(x = X[0:i+1, 0], y= X[0:i+1, 1], z= X[0:i+1, 2])
        ms1.set(x = X[i, 0], y = X[i, 1], z = X[i, 2])
        #fig.scene.reset_zoom()
        
        # create zeros for padding index positions for organization
        zeros = '0'*(padding - len(str(i)))
        
        # concate filename with zero padded index number as suffix
        filename = os.path.join(out_path, '{}_{}{}{}'.format(prefix, zeros, i, ext))

        mlab.savefig(filename=filename)
        
        #yield
        
    scene.disable_render = False
  
updateAnimation()
#mlab.show()


#ffmpeg_fname = os.path.join(out_path, '{}_%0{}d{}'.format(prefix, padding, ext))
#cmd = 'ffmpeg -f image2 -r {} -i {} -vcodec mpeg4 -y {}.mp4'.format(fps,
#                                                                    ffmpeg_fname,
#                                                                    prefix)
#print(cmd)
#subprocess.check_output(['bash','-c', cmd])

# Remove temp image files with extension
#[os.remove(f) for f in os.listdir(out_path) if f.endswith(ext)]


def display_animation(anim):
    plt.close(anim._fig)
    return HTML(anim_to_html(anim))
    

def init():
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    
# animation function.  This is called sequentially
def animate(i):
    current_index = int(X.shape[0] / frames * i)
    ax.cla()
    ax.plot3D(X[:current_index, 0], 
              X[:current_index, 1], 
              X[:current_index, 2])
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
# call the animator.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=fraim, interval=100)

# call our new function to display the animation
display_animation(anim)
