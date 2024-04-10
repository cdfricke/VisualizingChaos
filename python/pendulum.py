# Programmer: Connor Fricke (fricke.59@osu.edu)
# File: pendulum.py
# Latest Revision: 5-APRIL-2024 --> Created for Physics 5810 with Prof. Ralf Bundschuh
# PyGame simulation of damped, driven pendulum behavior, with positions updated from
# C++ differential equation solver, diffeq_pendulum.cpp, written by Prof. Furnstahl and
# adapted for use within this project by myself 

# *** NECESSARY MODULES ***
import pygame
from grid import *  # for drawing grid
from text import *  # for writing text
from trail import * # visual trail behind swinging mass
from arrow import * # draw arrow from center to mass
from math import pi, sin, cos
from pandas import read_csv
import os
# *************************

# *** GET PATHS, CHOOSE FILE ***
PROJ_DIR = os.getcwd()
DATA_PATH = PROJ_DIR + "/datafiles/"
selectFile = input("Select simulation to run:\n[1] Most Recent\n[2] Chaotic Example\n[3] Limit Cycles Example\n[4] Other\n>> ")
selectFile = int(selectFile) # convert to int

if (selectFile == 1):
    DATA_FILE = "diffeq_pendulum.dat"
elif (selectFile == 2):
    DATA_FILE = "chaotic.dat"
elif (selectFile == 3):
    DATA_FILE = "limit_cycles.dat"
elif (selectFile == 4):
    DATA_FILE = input("Enter file name (in /datafiles directory) >> ")
else:
    print("Using most recent C++ output.")
    DATA_FILE = "diffeq_pendulum.dat"
# *****************

# *** INITIALIZE ***
running = True
pygame.init()
WIDTH = 720
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH+1, HEIGHT+1))
clock = pygame.time.Clock()
dt = 0
frame = 0
simulationTime = 0
RATE = 5
fps = 0
SIM_RUNNING = True
# ******************

# *** COMMON VECTORS AND LOCATIONS ***
center = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
zero = pygame.Vector2(0, 0)
origin = zero
xhat = pygame.Vector2(1, 0)
yhat = pygame.Vector2(0, 1)
# ************************************

# **** HELPER FUNCTIONS ****
def screenPosition(r, theta) -> pygame.Vector2:
    return center + r*cos(theta)*yhat - r*sin(theta)*xhat
# **************************

# *** CLASSES ***
class Pendulum:
    def __init__(self, radius, arm_length):
        # constants
        self.RADIUS = radius
        self.ARM_LENGTH = arm_length
        # variables
        self.theta = 0          # ANGULAR POSITION OF PENDULUM
        self.thetadot = 0       # ANGULAR VELOCITY OF PENDULUM
        self.position = screenPosition(self.ARM_LENGTH, self.theta)

    def draw(self, surface, color):
        pygame.draw.circle(surface=surface, color=color, center=self.position, radius=self.RADIUS)

    def rotate(self, step):
        self.theta += step
        self.position = screenPosition(self.ARM_LENGTH, self.theta)

    def update(self, theta):
        self.theta = theta
        self.position = screenPosition(self.ARM_LENGTH, self.theta)
# *************************

# *** GRIDS, TRAILS, ASSETS ***
grid = Grid(5, 5, WIDTH, HEIGHT)
pendulum = Pendulum(radius=20, arm_length=250)
motor = Pendulum(radius=12, arm_length=0)
arrow = Arrow(center, pendulum.position)
trail = Trail(15)

# initialize text
fps_text = Text()
completion_text = Text()
theta_text = Text()
thetadot_text = Text()
time_text = Text()
motor_text = Text()

# *** PARSE DATA FROM C++ ***
colnames = ["t", "theta", "thetadot"]
dataframe = read_csv(DATA_PATH + DATA_FILE, comment="#", sep=" ", names=colnames)
print(dataframe)
# ***************************

# *** INITIAL CONDITIONS ***
initialAngle = dataframe["theta"][0]
initialPos = screenPosition(pendulum.ARM_LENGTH, initialAngle)
pendulum.position = initialPos
# **************************

# ***** GAME LOOP *****
while running:
    SIM_RUNNING = (frame < len(dataframe["theta"]))
    # pygame.QUIT means the user closed the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # wipe away anything from the previous frame
    screen.fill("black")

    # ***** UPDATE OBJECTS / TEXT *****
    # some things cannot be updated without error unless the frame number corresponds to a row within the dataframe
    if (SIM_RUNNING):
        # update all text to display values on screen
        completion_text.text("Simulation Running...")
        fps_text.text( "FPS :" + str( int(fps) ) )
        time_text.text( "Time (s) :" + str( round(dataframe["t"][frame], 1) ) )
        theta_text.text( "Theta (radians) :" + str(round(dataframe["theta"][frame],3) ) )
        thetadot_text.text( "ThetaDot (radians/s) :" + str( round(dataframe["thetadot"][frame],3) ) )  
        motor_text.text("motor") 
        pendulum.update(dataframe["theta"][frame]) 
    else: 
        completion_text.text("Simulation complete!")
    # trail requires copies of the current position each frame
    currentPos = pendulum.position.copy()   
    trail.addPoint(currentPos)
    # arrow update
    arrow.update(center, currentPos)

    # ***** RENDER THE SIM HERE *****
    grid.drawLines(screen, "grey", 1)
    trail.aadraw(screen, "green", 3)
    arrow.draw(screen, "grey", 5)
    pendulum.draw(screen, "red")
    motor.draw(screen, "light grey")
    fps_text.render(screen, 20*xhat + 20*yhat)
    time_text.render(screen, 20*xhat + 35*yhat)
    theta_text.render(screen, 20*xhat + 50*yhat)
    thetadot_text.render(screen, 20*xhat + 65*yhat)
    completion_text.render(screen, 5*xhat + 5*yhat)
    motor_text.render(screen, motor.position + 10*xhat - 20*yhat)

    pygame.display.flip() # flip() display to send work to the screen

    # limit to 50 fps (dt ~ 0.02)
    dt = clock.tick(30) / 1000
    # track a couple things for use
    simulationTime += dt * RATE
    frame += 1
    fps = 1.0 / dt

pygame.quit()