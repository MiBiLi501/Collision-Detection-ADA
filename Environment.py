import math
import numpy as np
from Particle import Particle
import random
import sys

def getX(particle):
    return particle.x


def getY(particle):
    return particle.y

def getSize(particle):
    return particle.size

def collide(p1, p2, debug = 0):
    dx = p1.x - p2.x
    dy = p1.y - p2.y

    dist = math.hypot(dx, dy)
    if dist - p1.size - p2.size - sys.float_info.epsilon < 0:

        n = np.array([p2.x-p1.x, p2.y-p1.y])
        n /= dist

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

        if debug:
            print("hit")

        return True
    return False



def bruteForce(particles):
    length = len(particles)
    for i in range(length-1):
        for j in range(i+1, length):
            collide(particles[i], particles[j])


def buildkDTree(particles, depth=0):
    if len(particles) <= 1:
        return []

    get_attribute_func = (getY) if depth & 1 else (
        getX)
    sorted_particles = sorted(particles, key=get_attribute_func)
    length = len(sorted_particles)
    mid = length//2
    if length & 1:
        median = get_attribute_func(sorted_particles[mid])
    else:
        median = (get_attribute_func(
            sorted_particles[mid]) + get_attribute_func(sorted_particles[mid - 1])) / 2

    leftSide = []
    rightSide = []

    for particle in sorted_particles:
        if (get_attribute_func(particle) - particle.size <= median):
            leftSide.append(particle)
        if (get_attribute_func(particle) + particle.size >= median):
            rightSide.append(particle)

    if len(leftSide) == length or len(rightSide) == length:
        return [sorted_particles]

    potential_collisions = [
        potential_collision for potential_collision in buildkDTree(leftSide, depth+1)]
    potential_collisions.extend(
        [potential_collision for potential_collision in buildkDTree(rightSide, depth+1)])
    return potential_collisions


def kDTree(particles):
    potential_collisions = buildkDTree(particles)
    collisions = set()
    for potential_collision in potential_collisions:
        length = len(potential_collision)
        for i in range(length - 1):
            for j in range(i+1, length):
                collisions.add(
                    frozenset((potential_collision[i], potential_collision[j])))
    
    for obj1, obj2 in collisions:
        collide(obj1, obj2)


def sweepAndPrune(particles):
        sorted_particles = sorted(particles, key=getX)
        length = len(sorted_particles)

        potential_collisions = []
        for i in range(length-1):
            for j in range(i + 1, length):
                if sorted_particles[j].x - sorted_particles[i].x >= sorted_particles[i].size + sorted_particles[j].size + sys.float_info.epsilon:
                    continue 
                potential_collisions.append((sorted_particles[i], sorted_particles[j]))

        for p1, p2 in potential_collisions:
            collide(p1, p2)

class Environment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.particles = []
        self.current_algorithm = 'bruteForce'  
        self.speed_multiplier = 1.0  



        self.color = (255, 255, 255)
        self.elasticity = 1

        self.lineX = []
        self.lineY = []

        self.pause = False

    def set_collision_algorithm(self, algorithm_name):
        if algorithm_name in ['bruteForce', 'kDTree', 'sweepAndPrune']:
            self.current_algorithm = algorithm_name
        else:
            raise ValueError("Invalid collision detection algorithm name")
    
    def set_particle_count(self, count):
        current_count = len(self.particles)
        if count > current_count:
            for _ in range(count - current_count):
                self.addRandParticle(1) 
        elif count < current_count:
            self.particles = self.particles[:count]

    def addRandParticle(self, n):
        for _ in range(n):
            size = random.randint(4, 5)
            x = random.randint(size, self.width - size)
            y = random.randint(size, self.height - size)
            angle = random.uniform(0, math.pi * 2)
            # Set the base speed to be the original speed times the current speed multiplier
            speed = random.random() * 0.1 * self.speed_multiplier  
            particle = Particle(x, y, size, angle, speed)
            self.particles.append(particle)

        for _ in range(10000):
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
                        length = particle.size + particle2.size - dist + sys.float_info.epsilon
                        particle.x += math.cos(tangent) * length
                        particle.y += math.sin(tangent) * length
                        particle2.x -= math.cos(tangent) * length
                        particle2.y -= math.sin(tangent) * length

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
        
    def set_particle_speed(self, speed_multiplier):
        self.speed_multiplier = speed_multiplier  # Update the current speed multiplier
        for particle in self.particles:
            particle.update_speed(speed_multiplier)


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
    
    def set_particle_speed(self, speed_multiplier):
        for particle in self.particles:
            particle.update_speed(speed_multiplier)



    def update(self):
        if self.pause:
            return
        
        for p in self.particles:
            p.move()
            self.bounce(p)

        if self.current_algorithm == 'bruteForce':
            bruteForce(self.particles)
        elif self.current_algorithm == 'kDTree':
            kDTree(self.particles)
        elif self.current_algorithm == 'sweepAndPrune':
            sweepAndPrune(self.particles)


    
