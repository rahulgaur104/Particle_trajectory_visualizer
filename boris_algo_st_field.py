#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 23:03:34 2020


"""

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

#m = 1.;
#q = 1.;
qdm = 1E6   # q/m for electrons for H+ ion q/m ~ 1E5
c = 3E10;
fraim = 50
duration = 500;
dt = 1E1

v = np.array([0., 1., 1E-1]);
x = np.array([0., 0., 0.]);

B = np.array([0., 0., 100]);
E = np.array([0., 0., 0]);

X = np.zeros((duration,3)) 
V = np.zeros((duration,3)) 

for time in range(duration):
    #t = charge / mass * B * 0.5 * dt;
    #s = 2. * t / (1. + t*t);
    #v_minus = v + charge / (mass * vAc) * E * 0.5 * dt;
    c1 = qdm*dt
    c2 = c1/c
    A_plus = np.eye(3) + c2*np.cross(np.eye(3), B)
    A_minus = np.eye(3) - c2*np.cross(np.eye(3), B)
    S = np.linalg.inv(A_plus)
    R = np.dot(S, A_minus)
    v = np.dot(v, R.T) + c1*np.dot(S, E)
    x = x + dt*np.dot(v, R.T) +c1*dt*np.dot(S, E)     
    X[time,:] = x;
    V[time,:] = v; 

"""
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.plot(X[:,0],X[:,1],X[:,2],'k',linewidth=2.0); 
#ax.xlabel(r'$x/d_{\rm p}$',fontsize=16)
#ax.ylabel(r'$y/d_{\rm p}$',fontsize=16)
#ax.zlabel(r'$z/d_{\rm p}$',fontsize=16)
plt.show()
"""
"""
padding = len(str(len(X[:,0])))

p = mlab.plot3d(X[:,0], X[:,1], X[:,2], color = (0, 1, 0), line_width = 5, tube_radius = 10, opacity=1.0)
l = mlab.points3d(X[:,0], X[:,1], X[:,2], color = (1, 0, 0), scale_factor=100, opacity=1.0)
#k = mlab.quiver3d(np.array([ np.max(X[:,0])/2, np.max(X[:,0])/2]), np.array([0, 0]), \
#                  np.array([0, -np.max(X[:,2])]), np.array([0, 0]), \
#                      np.array([0, 0]), np.array([0, np.max(X[:,2])]), line_width = 2, mode='arrow', scale_factor = 1)
#n = 
k = mlab.quiver3d(np.array([ np.max(X[:,0])/2, np.max(X[:,0])/2]), np.array([0, 0]), \
              np.array([0, np.max(X[:,2])]), np.array([0, 0]), \
                  np.array([0, 0]), np.array([0, 1]),  mode='cone', scale_factor = 200, opacity=1.0)
q = mlab.plot3d(np.ones((10,))*np.max(X[:,0])/2, np.zeros((10,)), np.linspace(0, np.max(X[:,2]),10), color = (1, 0, 0), line_width = 5, tube_radius = 10)
#p.actor.property.frontface_culling = True
#l.actor.property.frontface_culling = True
#k.actor.property.frontface_culling = True


len1 = np.shape(X)[0]
ms0 = p.mlab_source
ms1 = l.mlab_source
#ms2 = k.mlab_source
#mlab.options.offscreen = True
view = (120.7348112609312, 114.98066716199945, 2823.318842495628, np.array([168.92115036,  28.89857927, 346.1831355 ]))

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
        #ms2.set(u = np.array([0, 0]),v =  np.array([0, 0]), w = np.array([0, 3*np.max(X[:,2])]))
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

ffmpeg_fname = os.path.join(out_path, '{}_%0{}d{}'.format(prefix, padding, ext))
cmd = 'ffmpeg -f image2 -r {} -i {} -vcodec mpeg4 -y {}.mp4'.format(fps,
                                                                    ffmpeg_fname,
                                                                    prefix)
print(cmd)
subprocess.check_output(['bash','-c', cmd])

# Remove temp image files with extension
[os.remove(f) for f in os.listdir(out_path) if f.endswith(ext)]
"""


"""
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
"""
