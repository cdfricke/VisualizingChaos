# File: text.py
# Programmer: Connor Fricke (cd.fricke23@gmail.com)
# Last Revision: 
#   29-March-2024 --> created
#
# Class file designed as a wrapper aroung the PyGame font objects for writing text to the screen.

import pygame

class Text:
    def __init__(self):
        self.fontName = "consolas"
        self.bold = False
        self.italic = False
        self.size = 12
        self.color = "white"
        self.txt = "UNINITIALIZED"

    def set_font(self, fontName, size, bold, italics, color):
        self.fontName = fontName
        self.size = size
        self.bold = bold
        self.italic = italics
        self.color = color

    def text(self, textString):
        self.txt = textString

    def render(self, surface, location):
        font = pygame.font.SysFont(name=self.fontName, size=self.size, bold=self.bold, italic=self.italic)
        text = font.render(self.txt, True, self.color)
        surface.blit(text, location)


    

    
