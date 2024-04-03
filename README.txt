Final Project for Physics 5810 - Computational Physics

Visualizing Chaos with C++, Gnuplot, and PyGame
C. Fricke (fricke.59@osu.edu)

Latest Revision: 3-April-2024

The final project will use some previously learned methods of solving dfferential equations in C++ to 
solve the damped, driven pendulum oscillator differential equation. Then, the project will use PyGame 
to create a 2D visual representation of the pendulum system and display the chaotic behavior as well as
a few plots for data analysis such as phase-space plots, power spectrums, etc. 

The program relies on both Gnuplot and Matplotlib to do some data analysis. In particular, the current 
project handles Phase-Space plots with Gnuplot. Power spectrums will be handled with Matplotlib.

PyGame is a simple 2D graphics "engine" that runs on a fairly basic API written in Python. For more 
information, docs, and how to download the module for use, visit https://www.pygame.org/docs/ref/draw.html.
This project will use PyGame to create a 2-dimensional representation of the pendulum system as a sort 
of "visual simulation" of a chaotic or non-chaotic pendulum system.

Getting Started...
Before doing anything, if you are running this on your own Windows machine, you will need to have a few 
programs installed and added to your PATH.
    1) g++ compiler (I used the one from mingw64)
    2) Python - v3.12 preferred
    3) Gnuplot - I used v5.4
Here's a couple links in case you don't have these installed:
https://www.mingw-w64.org/
https://www.python.org/downloads/
https://sourceforge.net/projects/gnuplot/files/gnuplot/

The C++ part of the program compiles and links using a Powershell script, since Make is primarily a 
Linux-based application. The dependencies for the C++ segment reside within the aptly named "dependencies" 
directory of the project workspace. It does a couple more things than JUST compile and link the needed .cpp 
files, such as testing the Gnuplot functionality and retrieving the current working directory of the 
project (for compiling and creating object files with absolute paths). The script also installs the required
Python modules on your machine using a couple calls to pip. I understand that running this on Windows means 
you need these various softwares, so hopefully you are comfortable with that.


