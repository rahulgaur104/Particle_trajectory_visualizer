# visPT

**Author:** Rahul Gaur\
**email:** rgaur@terpmail.umd.edu\
Copyright Rahul Gaur 2020

This is a code used to visualize trajectories of charged particles under static electric and magnetic fields.

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

The code uses the famous Boris algorithm to solve the following equations of motion:
[!Equation] <a href="https://www.codecogs.com/eqnedit.php?latex=\begin{gathered}&space;\frac{d&space;\textbf{v}}{dt}&space;=&space;q(\textbf{E}&space;&plus;&space;\textbf{v}&space;\times&space;\textbf{B})\\&space;\frac{d&space;\textbf{r}}{dt}&space;=&space;\textbf{v}&space;\end{gathered}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\begin{gathered}&space;\frac{d&space;\textbf{v}}{dt}&space;=&space;q(\textbf{E}&space;&plus;&space;\textbf{v}&space;\times&space;\textbf{B})\\&space;\frac{d&space;\textbf{r}}{dt}&space;=&space;\textbf{v}&space;\end{gathered}" title="\begin{gathered} \frac{d \textbf{v}}{dt} = q(\textbf{E} + \textbf{v} \times \textbf{B})\\ \frac{d \textbf{r}}{dt} = \textbf{v} \end{gathered}" /></a> 

The template and explanatory text are in [README-template.md](README-template.md)
## Links
Blog post: https://iaizzi.me/04/25/write-a-good-readme

