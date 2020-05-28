# visPT

**Author:** Rahul Gaur\
**email:** rgaur@terpmail.umd.edu\
Copyright Rahul Gaur 2020

This is a collection of scripts to visualize trajectories of charged particles under static electric and magnetic fields.

## Configuration

It has only been tested on a Linux machine(Ubuntu 18.04) with an intel graphics card and the following package configuration:

* python 3.5
* mayavi 4.6.2 
* vtk 8.1.2
* pyqt 4.11.4

and after setting the following environment variables:

* ETS_TOOLKIT=qt4
* QT_API=pyqt

Note that this configuration may not be unique for the code to work properly.[Some issues with vtk and/or mayavi](https://github.com/enthought/mayavi/issues/656)

## Physics

The code uses the famous Boris algorithm to solve the Lorentz equation of motion:

<a href="https://www.codecogs.com/eqnedit.php?latex=\begin{gathered}&space;\frac{d&space;\textbf{v}}{dt}&space;=&space;q(\textbf{E}&space;&plus;&space;\textbf{v}&space;\times&space;\textbf{B})\\&space;\frac{d&space;\textbf{r}}{dt}&space;=&space;\textbf{v}&space;\end{gathered}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\begin{gathered}&space;\frac{d&space;\textbf{v}}{dt}&space;=&space;q(\textbf{E}&space;&plus;&space;\textbf{v}&space;\times&space;\textbf{B})\\&space;\frac{d&space;\textbf{r}}{dt}&space;=&space;\textbf{v}&space;\end{gathered}" title="\begin{gathered} \frac{d \textbf{v}}{dt} = q(\textbf{E} + \textbf{v} \times \textbf{B})\\ \frac{d \textbf{r}}{dt} = \textbf{v} \end{gathered}" /></a> 

conserving the phase space volume of the distriution function(without an electric field). The aim of this project is to provide the user with images or GIFs of the particle moving in static 3-D fields. The outline of the process is as follows:

* Create code for particle along straight electric and magnetic fields. Status: Done!
* Create code for simple analytical topology of the electric and magnetic fields. For example, ring, cylinder, torus. Status: Done
* Add, debug and test the image and GIF rendering component. Status : Pending
* Transform all the position and velocity vectors to field-aligned coordinates. Status: Not started
* Add provision for the user to add an arbitrary 3D magnetic and electric field topology using a data file(.nc, .hd5) Status: Not started
* Transform the structure of the code to an object-oriented one. Status: Not started

Collaboration with this endaevour is higly-encouraged. Don't hesitate to contact me regarding any further information on this code.



