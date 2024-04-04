# File: trail.py
# Programmer: Connor Fricke (cd.fricke23@gmail.com)
# Last Revision:
#   27-MARCH-2024 --> created, used for drawing paths of orbitor objects in orbit simulation

import pygame

class Trail:

    # Trail.__init__(maxlength):
    # parameters:
    #   maxlength: the maximum number of points to be used to draw the trail at one given time
    # *************
    # This constructor defines the maxlength data member of the trail class, which defines the max size of the points array
    # for optimization and indefinite simulation times. Without a max length, the array which stores the points that are used
    # to draw the trail would grow arbitrarily large, which is unnecessary. The length needed is to be determined by the user.
    def __init__(self, maxlength):
        self.pointArray = []
        self.maxlength = maxlength
        
    # Trail.aadraw(surface, color, blend):
    # parameters:
    #   surface: the pygame surface for the lines to be drawn on, usually the screen.
    #   color: the color of the trail. Should be a pygame.Color type.
    #   blend: the blend of the line to be drawn, which is needed for the anti-aliasing.
    # *************
    # This function draws an anti-aliased line between each of the points in the pointArray stored by the class.
    def aadraw(self, surface, color, blend):
        pygame.draw.aalines(surface=surface, color=color, closed=False, points=self.pointArray, blend=blend)
    
    # Trail.draw(surface, color, width):
    # parameters:
    #   surface: the pygame surface for the lines to be drawn on, usually the screen.
    #   color: the color of the trail. Should be a pygame.Color type.
    #   width: the width of the line to be drawn, measured in pixels.
    # *************
    # This function draws a line between each of the points in the pointArray stored by the class.
    def draw(self, surface, color, width):
        pygame.draw.lines(surface=surface, color=color, closed=False, points=self.pointArray, width=width)

    # Trail.addPoint(point):
    # parameters:
    #   point: a pygame.Vector2 type object representing a location in 2D space which is to be added to the internal 
    #          array of the class.
    # *************
    # This function appends a 2D vector to the end of the pointArray list of the Trail class. If the array length exceeds 
    # the max length defined during the initialization stage of creating a trail, then the value at the beginning of the 
    # list is removed, ensuring the array never exceeds the maximum length.
    def addPoint(self, point):
        self.pointArray.append(point)
        # limit trail length to N points (N should be determined based on the orbit length)
        if (len(self.pointArray) > self.maxlength):
            self.pointArray.pop(0)