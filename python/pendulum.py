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
RATE = 1
# ******************

# *** COMMON VECTORS AND LOCATIONS ***
center = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
zero = pygame.Vector2(0, 0)
origin = zero
xhat = pygame.Vector2(1, 0)
yhat = pygame.Vector2(0, 1)
# ************************************

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
    

    # flip() display to send work to the screen
    pygame.display.flip()

    # limit to 50 fps (dt ~ 0.02)
    dt = clock.tick(100) / 1000
    # track a couple things for use
    simulationTime += dt * RATE
    frame += 1

pygame.quit()