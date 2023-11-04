import math
import numpy as np
from Particle import Particle
import random

def collide(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    
    dist = math.hypot(dx, dy)
    if dist - p1.size - p2.size < 0:

        #get unit normal vector
        n = np.array([p2.x-p1.x, p2.y-p1.y])
        n /= dist

        #get unit tangent vector
        t = np.array([-n[1], n[0]])

        v1 = np.array([p1.vx, p1.vy])
        v2 = np.array([p2.vx, p2.vy])

        v1n = n.dot(v1)
        v1t = t.dot(v1)

        v2n = n.dot(v2)
        v2t = t.dot(v2)
        
        v1, v2 = n*v2n + v1t*t, n*v1n + v2t * t
        p1.vx, p1.vy = v1[0], v1[1]
        p2.vx, p2.vy = v2[0], v2[1]

class Environment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.particles = []

        self.color = (255, 255, 255)
        self.elasticity = 1

    def addRandParticle(self, n):
        for _ in range(n):
            size = random.randint(10, 20)
            x = random.randint(size, self.width-size)
            y = random.randint(size, self.height-size)
            angle = random.uniform(0, math.pi*2)
            speed = random.random() * 0.05
            particle = Particle(x, y, size, angle, speed)
            self.particles.append(particle)

        for _ in range(1000):
            overlap = False

            for i, particle in enumerate(self.particles):
                if particle.x > self.width - particle.size:
                    particle.x -= particle.x - self.width + particle.size
                elif particle.x < particle.size:
                    particle.x += particle.size - particle.x 
                if particle.y > self.height - particle.size:
                    particle.y -= particle.y - self.height + particle.size
                elif particle.y < particle.size:
                    particle.y += particle.size - particle.y

                for particle2 in self.particles[i+1:]:
                        dx = particle.x - particle2.x
                        dy = particle.y - particle2.y
                        
                        dist = math.hypot(dx, dy)
                        if dist - particle.size - particle2.size < 0:
                            overlap = True
                            tangent = math.atan2(dy, dx)
                            length = particle.size + particle2.size - dist
                            particle.x += math.cos(tangent) * length
                            particle.y += math.sin(tangent) * length
                            particle2.x -= math.cos(tangent) * length
                            particle.x -= math.sin(tangent) * length
            if not overlap:
                break

    def bounce(self, particle):
        if particle.x > self.width - particle.size:
            particle.x = 2 * (self.width - particle.size) - particle.x
            # self.angle = math.pi - self.angle
            particle.vx *= -1
            particle.speed *= self.elasticity

        elif particle.x < particle.size:
            particle.x = 2 * particle.size - particle.x
            # self.angle = math.pi - self.angle
            particle.vx *= -1
            particle.speed *= self.elasticity

        if particle.y > self.height - particle.size:
            particle.y = 2 * (self.height - particle.size) - particle.y
            # self.angle *= -1
            particle.vy *= -1
            particle.speed *= self.elasticity
        
        elif particle.y < particle.size:
            particle.y = 2 * particle.size - particle.y
            # self.angle *= -1
            particle.vy *= -1
            particle.speed *= self.elasticity

    def update(self):
        for p in self.particles:
            p.move()
            self.bounce(p)

        self.collisionDetection()
        
    def collisionDetection(self):
        for i, particle in enumerate(self.particles):
            particle.move()
            for particle2 in self.particles[i+1:]:
                collide(particle, particle2)

        