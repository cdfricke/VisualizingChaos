Final Project for Physics 5810 - Computational Physics

Visualizing Chaos with C++, Gnuplot, and PyGame
C. Fricke (fricke.59@osu.edu)

Latest Revision: 5-April-2024

NOTE: This program cannot be run on OSC, because OSC uses Python 3.9 at the newest, and we cannot use the
PyGame module which is necessary for the simulation.

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

~~~ Getting Started ~~~
Before doing anything, if you are running this on your own Windows machine, you will need to have a few 
programs installed and added to your PATH.
    1) g++ compiler (https://www.mingw-w64.org/)
    2) Python (https://www.python.org/downloads/) - v3.12 preferred
    3) Gnuplot (https://sourceforge.net/projects/gnuplot/files/gnuplot/) - I used v5.4

The project is divided into a few directories:

VisualizingChaos  >>  script file, executables, README
    \datafiles  >>  output files from C++ programs
    \Cpp  >>  Makefile, .cpp and .h files
    \misc  >>  object files (.o) and some other unimportant things
    \python  >>  Python scripts (.py) for PyGame portion of the project

~~~ Running the project ~~~
The entire program runs off of a single script. I'm developing it primarily for Windows, so right now
it runs with a Powershell (.ps1) script. See build.ps1 for details. To run, open up a Powershell terminal,
navigate to the project directory (VisualizingChaos). Here you should see the build.ps1 script. At the command
line, enter:
> .\build.ps1
then let the program do the work! The script will compile and link the C++ dependencies, then run the generated
executable (diffeq_pendulum.exe), which in turn calls Gnuplot to plot in "real-time". You have the option to 
plot multiple times before exiting the C++ program, but note that each time you plot, the program overwrites 
the data file (.dat), so when Python takes over, it will only simulate your last run. Also note that the Gnuplot
window may be rather small on high resolution displays, so it's best to turn down your resolution to something like
1080p (if possible on your machine), and then run the program.

OPTIONAL TODO:
 - implement args to main() for automatically setting certain parameters, so we can call:
    diffeq_pendulum.exe w_ext 0.5 f_ext 0.9 theta0 -0.8
 - Add textbox class to python script so that large amounts of text can be rendered more easily.
 - Add text to simulation that displays the pendulum parameters
 - Add descriptive name of pendulum behavior somewhere in the simulation, e.g. ("Chaotic Pendulum")



