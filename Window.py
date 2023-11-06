from Environment import Environment
import pygame as pyg

WINDOW_SIZE = (1000, 600)
WHITE = (255, 255, 255)

screen = pyg.display.set_mode(WINDOW_SIZE)
screen.fill(WHITE)

pyg.display.set_caption("Test")
pyg.display.flip()

env = Environment(*WINDOW_SIZE)
env.addRandParticle(30)

running = True
while running:
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            running = False

    screen.fill(env.color)
    env.update()

    for p in env.particles:
        pyg.draw.circle(screen, p.color, (p.x, p.y), p.size, p.thickness)

    pyg.display.flip()
