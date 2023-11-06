import math
import numpy as np
from Particle import Particle
import random
import sys


def bruteForce(particles):
    for i, particle in enumerate(particles):
        particle.move()
        for particle2 in particles[i+1:]:
            collide(particle, particle2)


def kDTree(particles, depth=0):
    if len(particles) <= 1:
        return

    if len(particles) == 2:
        bruteForce(particles)
        return

    get_attribute_func = (lambda particle: particle.y) if depth & 1 else (
        lambda particle: particle.x)
    sorted_particles = sorted(particles, key=get_attribute_func)
    length = len(sorted_particles)
    if length & 1:
        median = get_attribute_func(sorted_particles[length//2])
    else:
        median = (get_attribute_func(
            sorted_particles[length//2]) + get_attribute_func(sorted_particles[length//2 - 1])) / 2

    leftSide = list()
    rightSide = list()

    for particle in sorted_particles:
        if (get_attribute_func(particle) - particle.size <= median):
            leftSide.append(particle)
        if (get_attribute_func(particle) + particle.size >= median):
            rightSide.append(particle)

    stop = True
    if length == len(leftSide):
        for i in range(length):
            if sorted_particles[i] is not leftSide[-i]:
                stop = False
                break

    if length == len(rightSide) and not stop:
        for i in range(length):
            if sorted_particles[i] is not rightSide[-i]:
                stop = False
                break

    if stop:
        bruteForce(particles)
        return

    kDTree(leftSide, depth+1)
    kDTree(rightSide, depth+1)


def collide(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y

    dist = math.hypot(dx, dy)
    if dist - p1.size - p2.size - sys.float_info.epsilon < 0:

        # get unit normal vector
        n = np.array([p2.x-p1.x, p2.y-p1.y])
        n /= dist

        # get unit tangent vector
        t = np.array([-n[1], n[0]])

        v1 = np.array([p1.vx, p1.vy])
        v2 = np.array([p2.vx, p2.vy])

        v1n = n.dot(v1)
        v1t = t.dot(v1)

        v2n = n.dot(v2)
        v2t = t.dot(v2)

        v1, v2 = n*v2n + v1t*t, n*v1n + v2t * t
        p1.vx, p1.vy = v1
        p2.vx, p2.vy = v2


class Environment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.particles = []

        self.color = (255, 255, 255)
        self.elasticity = 1

    def addRandParticle(self, n):
        for _ in range(n):
            size = random.randint(4, 5)
            x = random.randint(size, self.width-size)
            y = random.randint(size, self.height-size)
            angle = random.uniform(0, math.pi*2)
            speed = random.random() * 0.1
            particle = Particle(x, y, size, angle, speed)
            self.particles.append(particle)

        for _ in range(10000):
            overlap = False

            for i, particle in enumerate(self.particles):

                for particle2 in self.particles[i+1:]:
                    dx = particle.x - particle2.x
                    dy = particle.y - particle2.y

                    dist = math.hypot(dx, dy)
                    if dist - particle.size - particle2.size < 0:
                        overlap = True
                        tangent = math.atan2(dy, dx)
                        length = particle.size + particle2.size - dist + sys.float_info.epsilon
                        particle.x += math.cos(tangent) * length
                        particle.y += math.sin(tangent) * length
                        particle2.x -= math.cos(tangent) * length
                        particle.x -= math.sin(tangent) * length

                if particle.x > self.width - particle.size:
                    particle.x -= particle.x - self.width + particle.size
                elif particle.x < particle.size:
                    particle.x += particle.size - particle.x
                if particle.y > self.height - particle.size:
                    particle.y -= particle.y - self.height + particle.size
                elif particle.y < particle.size:
                    particle.y += particle.size - particle.y
            if not overlap:
                break

    def bounce(self, particle):
        if particle.x > self.width - particle.size:
            particle.x = 2 * (self.width - particle.size) - particle.x
            particle.vx *= -1
            particle.speed *= self.elasticity

        elif particle.x < particle.size:
            particle.x = 2 * particle.size - particle.x
            particle.vx *= -1
            particle.speed *= self.elasticity

        if particle.y > self.height - particle.size:
            particle.y = 2 * (self.height - particle.size) - particle.y
            particle.vy *= -1
            particle.speed *= self.elasticity

        elif particle.y < particle.size:
            particle.y = 2 * particle.size - particle.y
            particle.vy *= -1
            particle.speed *= self.elasticity

    def update(self):
        for p in self.particles:
            p.move()
            self.bounce(p)

        self.collisionDetection(kDTree)

    def collisionDetection(self, func):
        func(self.particles)
