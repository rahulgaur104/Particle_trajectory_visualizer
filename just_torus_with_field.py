
import numpy as np
from mayavi import mlab

R_0 = 150
# Torus and geodesic potting routine
angle = np.linspace(0, 2 * np.pi, 60)
th1, phi1 = np.meshgrid(angle, angle)
r = 50 
X1 = (R_0 + r * np.cos(th1)) * np.cos(phi1)
Y1 = (R_0 + r * np.cos(th1)) * np.sin(phi1)
Z1 = r * np.sin(th1)

k = mlab.mesh(X1, Y1, Z1, color=(0, 1, 0), opacity=1.0)


nu = 1
om1 = 5
om2 = 5*nu*np.sqrt(2)
t = np.linspace(0, 8, 1000)
th2  = om1*t
phi2 = om2*t

X2 = (R_0 + r * np.cos(th2)) * np.cos(phi2)
Y2 = (R_0 + r * np.cos(th2)) * np.sin(phi2)
Z2 = r * np.sin(th2)

n = mlab.plot3d(X2, Y2, Z2, color = (1, 0, 0), line_width = 2, tube_radius = 1)
mlab.savefig('check.png')

