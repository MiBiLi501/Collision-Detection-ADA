from Particle import Particle

import math
import pygame as pyg
import random

WINDOW_SIZE = (600, 400)
WHITE = (255, 255, 255)

screen = pyg.display.set_mode(WINDOW_SIZE)
screen.fill(WHITE)

pyg.display.set_caption("Test")
pyg.display.flip()

number_of_particles = 10
my_particles = []
for n in range(number_of_particles):
    size = random.randint(10, 20)
    x = random.randint(size, WINDOW_SIZE[0]-size)
    y = random.randint(size, WINDOW_SIZE[1]-size)

    particle = Particle(screen, x, y, size)
    particle.speed = random.random() * 0.05
    particle.angle = random.uniform(0, math.pi*2)
    my_particles.append(particle)

running = True
while running:
    screen.fill(WHITE)
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            running = False
    sie = random.randint(10, 20)

    for particle in my_particles:
        particle.move()
        particle.bounce()
        particle.display()

    pyg.display.flip()