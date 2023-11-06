import math
import pygame as pyg


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
        self.x += self.vx
        self.y += self.vy
