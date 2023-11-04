import math
import pygame as pyg

GRAVITY = None
DRAG = 1
ELASTICITY = 1

# def addVectors(angle1, length1, angle2, length2):
#     x = length1 * math.cos(angle1) + length2 * math.cos(angle2)
#     y = length1 * math.sin(angle1) + length2 * math.sin(angle2)
    
#     length = math.hypot(x, y)
#     angle = math.atan2(y, x)
#     return (angle, length)

class Particle():
    def __init__(self, x, y, size, angle, speed):
        self.x = x
        self.y = y
        self.size = size
        self.color = (0, 0, 255)
        self.thickness = 1

        self.speed = speed
        self.vx = math.cos(angle) * self.speed
        self.vy = math.sin(angle) * self.speed
    
    def move(self):
        # if GRAVITY is not None:
            # (self.angle, self.speed) = addVectors(self.angle, self.speed, *GRAVITY)
        # self.vx = math.cos(self.angle) * self.speed
        # self.vy = math.sin(self.angle) * self.speed
        self.x += self.vx
        self.y += self.vy
        self.speed *= DRAG
        