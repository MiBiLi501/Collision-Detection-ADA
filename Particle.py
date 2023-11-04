import math
import pygame as pyg

GRAVITY = None
DRAG = 1
ELASTICITY = 1

def addVectors(angle1, length1, angle2, length2):
    x = length1 * math.cos(angle1) + length2 * math.cos(angle2)
    y = length1 * math.sin(angle1) + length2 * math.sin(angle2)
    
    length = math.hypot(x, y)
    angle = math.atan2(y, x)
    return (angle, length)

class Particle():
    def __init__(self, screen, x, y, size):
        self.screen = screen
        self.x = x
        self.y = y
        self.size = size
        self.color = (0, 0, 255)
        self.thickness = 1

        self.speed = 0.01
        self.angle = 0

    def bounce(self):
        width = self.screen.get_width()
        height = self.screen.get_height()
        if self.x > width - self.size:
            self.x = 2 * (width - self.size) - self.x
            self.angle = math.pi - self.angle
            self.speed *= ELASTICITY

        elif self.x < self.size:
            self.x = 2 * self.size - self.x
            self.angle = math.pi - self.angle
            self.speed *= ELASTICITY

        if self.y > height - self.size:
            self.y = 2 * (height - self.size) - self.y
            self.angle *= -1
            self.speed *= ELASTICITY
        
        elif self.y < self.size:
            self.y = 2 * self.size - self.y
            self.angle *= -1
            self.speed *= ELASTICITY


    def display(self):
        pyg.draw.circle(self.screen, self.color, (self.x, self.y), self.size, self.thickness)
    
    def move(self):
        if GRAVITY is not None:
            (self.angle, self.speed) = addVectors(self.angle, self.speed, *GRAVITY)
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.speed *= DRAG
        