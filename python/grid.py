# File: grid.py
# Programmer: Connor Fricke (cd.fricke23@gmail.com)
# Last Revision:
#   4-MAR-2024 --> Created, v1
#   7-MAR-2024 --> added grid colors
#   17-MAR-2024 --> added comments for documentation
#
# ************************************************

import pygame
import random

# *** CLASS DEFINITION ***

# GRID: class object for drawing a grid with a certain number of rows and columns on the screen.
class Grid:
    
    def __init__(self, rows, columns, width, height):
        """
        Grid.__init__(rows, columns):
        parameters:
           rows: number of rows in the grid
           columns: number of columns in the grid
           width: the width of the screen, in pixels
           height: the height of the screen, in pixels

        This constructor function initializes several variables based on the passed parameters
        as they are necessary for the member functions of the class to operate.
        numRows: defines the number of rows
        numCols: defines the number of columns
        xticks: an array of pixel locations in the x-dimension marking the left and right edges of grid spaces.
        yticks: analogous to xticks, in the y-dimension.
        Matrix: a two-dimensional list of randomized numbers, used by the colorFunction for each grid space to randomize the color of that space.
        Matrix must be populated with float values from 0 to 1
        """
        self.width = width
        self.height = height
        self.numRows = rows
        self.numCols = columns
        self.xticks = list(range(0, width + 1, int(width / columns)))
        self.yticks = list(range(0, height + 1, int(height / rows)))
        # initially, the matrix is populated with random values
        self.Matrix = [[random.random() for x in range(columns)] for y in range(rows)]
    

    def drawLines(self, surface, color, thickness):
        """
        Grid.drawLines(surface, color, thickness):
        parameters:
           surface: the surface of the PyGame for the grid lines to be drawn on, usually the screen.
           color: the color of the lines to be drawn, must be an object of type pyGame.color
           thickness: the width of the grid lines to be drawn, measured in pixels.
        
        This function will draw equally spaced gridlines in both the x and y dimensions of the screen with color and thickness of
        gridlines defined as paramaters passed to the function. The spacing of the gridlines is determined by the width or height of the screen 
        divided by the number of columns or rows that the grid is made up of. (numRows and numCols are data members of this class)
        """
        for tick in self.xticks:
            start = tick*pygame.Vector2(1,0)
            end = start + self.height*pygame.Vector2(0,1)
            pygame.draw.line(surface=surface, color=color, start_pos=start, end_pos=end, width=thickness)
        for tick in self.yticks:
            start = tick*pygame.Vector2(0,1)
            end = start + self.width*pygame.Vector2(1,0)
            pygame.draw.line(surface=surface, color=color, start_pos=start, end_pos=end, width=thickness)
            
    
    def drawRectangles(self, surface, colorFunc):
        """
        Grid.drawRectangles(self, surface, colorFunc):
        parameters:
            surface: the surface of the PyGame for the grid lines to be drawn on, usually the screen.
            colorFunc: a function object, which returns a color. The function passed should take two parameters. See colorFunctions for details.

        This function colors each of the rectangles defined by the dimensions, numRows, and numCols attributes of the grid.
        Colors are currently randomly generated via a colorFunction which pulls float values from the Matrix attribute of the grid.
        Since the float values of the Matrix are RNG'd between 0 and 1, then the color of each grid space is also random.
        """
        for x in range(0, self.numCols):
            for y in range(0, self.numRows):
                rect = pygame.Rect(self.xticks[x], self.yticks[y], self.width / self.numCols, self.height / self.numRows)
                pygame.draw.rect(surface, colorFunc(self.Matrix[y][x]), rect)


    def fillMatrix(self):
        """
        Grid.fillMatrix()
        parameters: none
    
        This function decides how to populate the matrix of floats that decides the color of each rectangle
        Whatever this function yields, it must be a value between 0 and 1
        """
        for y in range(self.numRows):
            for x in range(self.numCols):
                self.Matrix[y][x] = float(y / self.numRows)