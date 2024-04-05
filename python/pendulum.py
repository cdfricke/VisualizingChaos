# Programmer: Connor Fricke (fricke.59@osu.edu)
# File: pendulum.py
# Latest Revision: 4-April-2024 --> Created
# PyGame simulation of damped, driven pendulum behavior, with positions updated from
# C++ differential equation solver, diffeq_pendulum.cpp, written by Prof. Furnstahl and
# adapted for use within this project

# *** NECESSARY MODULES ***
import pygame
from grid import *  # for drawing grid
from text import *  # for writing text
from trail import * # visual trail behind swinging mass
from math import pi, sin, cos
from pandas import read_csv
import os
# *************************

# *** GET PATHS ***
PROJ_DIR = os.getcwd()
DATA_PATH = PROJ_DIR + "\\datafiles\\"
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
# ******************

# *** COMMON VECTORS AND LOCATIONS ***
center = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
zero = pygame.Vector2(0, 0)
origin = zero
xhat = pygame.Vector2(1, 0)
yhat = pygame.Vector2(0, 1)
# ************************************

def screenPosition(r, theta) -> pygame.Vector2:
    return center + r*cos(theta)*yhat - r*sin(theta)*xhat

# *** CLASSES ***
class Object:
    def __init__(self, radius, mass):
        # constants
        self.RADIUS = radius
        self.MASS = mass
        # variables
        self.position = center          # set position at middle of screen
        self.velocity = origin            # set velocity to zero
        self.acceleration = zero        # set acceleration to zero

    # call draw() to automatically draw the circle with it's current attributes
    def draw(self, surface, color):
        pygame.draw.circle(surface=surface, color=color, center=self.position, radius=self.RADIUS)

    def update(self, deltaTime):
        # update acceleration, velocity, and position
        # v_f = v_0 + at
        self.velocity += self.acceleration * deltaTime
        # x_f = x_0 + vt
        self.position += self.velocity * deltaTime 

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

    def set_theta(self, theta):
        self.theta = theta

    def update(self, step):
        self.theta += step
        self.position = screenPosition(self.ARM_LENGTH, self.theta)

# *************************

# *** GRIDS, TRAILS, ASSETS ***
grid = Grid(5, 5, WIDTH, HEIGHT)
pendulum = Pendulum(radius=10, arm_length=250)

# *** PARSE DATA FROM C++ ***
colnames = ["t", "theta", "thetadot"]
dataframe = read_csv(DATA_PATH + "diffeq_pendulum.dat", comment="#", sep=" ", names=colnames)
print(dataframe)
# ***************************

# ***** GAME LOOP *****
while running:
    # pygame.QUIT means the user closed the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # wipe away anything from the previous frame
    screen.fill("black")

    # ***** RENDER THE SIM HERE *****
    grid.drawLines(screen, "grey", 1)
    pendulum.draw(screen, "red")
    pendulum.update(0.001*RATE)

    # flip() display to send work to the screen
    pygame.display.flip()

    # limit to 50 fps (dt ~ 0.02)
    dt = clock.tick(100) / 1000
    # track a couple things for use
    simulationTime += dt * RATE
    frame += 1

pygame.quit()