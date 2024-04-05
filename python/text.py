# Programmer: Connor Fricke (cd.fricke23@gmail.com)
# File: text.py
# Last Revision: 29-MARCH-2024 --> created
#
# *************************************************

import pygame

# CLASS FOR WRITING TEXT IN PYGAME
class Text:

    def __init__(self):
        """
        Text.__init__():
        parameters:
            none
        
        Constructor function for Text class. Assigns default values to necessary font details,
        including font name, bold/italics, size, and color. Also sets the string to "UNINITIALIZED".
        Details: Consolas, 12 pt, White, Non-bold, Non-italic
        """
        self.fontName = "consolas"
        self.bold = False
        self.italic = False
        self.size = 12
        self.color = "white"
        self.txt = "UNINITIALIZED"

    def set_font(self, fontName, size, bold, italics, color):
        """
        Text.set_font(fontName, size, bold, italics, color):
        parameters:
            fontName: name of the font style to be used, Consolas by default. Should be a string type.
            size: Character size, in pixels.
            bold: boolean value specifying whether text is rendered as bold.
            italics: boolean value specifying whether text is renderd as italic.
            color: text color, should be a PyGame.Color type, or color string.

        Sets the font details of the text to be rendered.
        """
        self.fontName = fontName
        self.size = size
        self.bold = bold
        self.italic = italics
        self.color = color

    def text(self, textString):
        """
        Text.text(textString):
        parameters:
            textString: string object representing the text to be output
        
        Defines the string of text to be rendered.
        """
        self.txt = textString

    def render(self, surface, location):
        """
        Text.render(surface, location):
        parameters:
            surface: pygame surface for the text to be rendered to, usually the screen.
            location: location of the top left corner of the text bounding box

        Helper function for easily displaying a string in the form of a Text class in PyGame.
        The function creates a font object from PyGame's SysFont() function, renders the text (anti-aliased)
        and then blit()'s the rendered font to the surface specified, at the location specified.
        """
        font = pygame.font.SysFont(name=self.fontName, size=self.size, bold=self.bold, italic=self.italic)
        text = font.render(self.txt, True, self.color)
        surface.blit(text, location)


    

    
