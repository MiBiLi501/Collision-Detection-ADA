from Particle import Particle

import math
import pygame as pyg
import random
import sys

ELASTICITY = 1

def collide(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    
    dist = math.hypot(dx, dy)
    if dist - p1.size - p2.size  + sys.float_info.epsilon * 100 < 0:
        tangent = -math.atan2(dy, dx)
        angle = tangent

        angle1 = 2 * (math.pi/2 - tangent) - p1.angle
        angle2 = 2 * (math.pi/2 - tangent) - p2.angle
        speed1 = p1.speed*ELASTICITY
        speed2 = p2.speed*ELASTICITY

        p1.angle, p1.speed = angle1, speed1
        p2.angle, p2.speed = angle2, speed2

        p1.x += math.cos(angle) * 2
        p1.y -= math.sin(angle) * 2
        p2.x -= math.cos(angle) * 2
        p2.y += math.sin(angle) * 2


WINDOW_SIZE = (1000, 400)
WHITE = (255, 255, 255)

screen = pyg.display.set_mode(WINDOW_SIZE)
screen.fill(WHITE)

pyg.display.set_caption("Test")
pyg.display.flip()

number_of_particles = 20
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

    for i, particle in enumerate(my_particles):
        particle.move()
        particle.bounce()
        for particle2 in my_particles[i+1:]:
            collide(particle, particle2)
        particle.display()

    pyg.display.flip()