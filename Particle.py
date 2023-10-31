import math
import pygame as pyg

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

        elif self.x < self.size:
            self.x = 2 * self.size - self.x
            self.angle = math.pi - self.angle

        if self.y > height - self.size:
            self.y = 2 * (height - self.size) - self.y
            self.angle *= -1
        
        elif self.y < self.size:
            self.y = 2 * self.size - self.y
            self.angle *= -1


    def display(self):
        pyg.draw.circle(self.screen, self.color, (self.x, self.y), self.size, self.thickness)
    
    def move(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
