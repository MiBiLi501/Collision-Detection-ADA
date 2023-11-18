from Environment import Environment
import pygame as pyg

pyg.font.init()

WINDOW_SIZE = (1000, 600)
WHITE = (255, 255, 255)

screen = pyg.display.set_mode(WINDOW_SIZE)
screen.fill(WHITE)

clock = pyg.time.Clock()
fps_bg = pyg.Surface((25,25))
fps_bg.fill((255,0,0))
fps_font = pyg.font.SysFont("Arial", 20)

def show_fps():
    fps_text = str(int(clock.get_fps()))
    fps_surface = fps_font.render(fps_text, 1, pyg.Color('black'))
    screen.blit(fps_bg, (0,0))
    screen.blit(fps_surface, (0,0))

pyg.display.set_caption("Test")
pyg.display.flip()

env = Environment(*WINDOW_SIZE)
env.addRandParticle(30)

running = True
min_fps = float('inf')
max_fps = 0
total_fps = 0
frame_count = 0

start_time = pyg.time.get_ticks()

while running:
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            running = False

    screen.fill(env.color)
    env.update()

    for p in env.particles:
        pyg.draw.circle(screen, p.color, (p.x, p.y), p.size, p.thickness)

    if pyg.time.get_ticks() - start_time >= 1000:
        current_fps = clock.get_fps()
        min_fps = min(min_fps, current_fps)
        max_fps = max(max_fps, current_fps)
        total_fps += current_fps
        frame_count += 1

    show_fps()
    pyg.display.flip()
    clock.tick(3000)

if frame_count > 0:
    average_fps = total_fps / frame_count
    print(f"Min FPS: {min_fps}, Max FPS: {max_fps}, Average FPS: {average_fps}")
else:
    print("FPS data not captured.")