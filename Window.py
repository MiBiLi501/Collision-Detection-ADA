from Environment import Environment
import pygame as pyg

pyg.font.init()

WINDOW_SIZE = (1000, 600)
WHITE = (255, 255, 255)

screen = pyg.display.set_mode(WINDOW_SIZE)
screen.fill(WHITE)

clock = pyg.time.Clock()
fps_font = pyg.font.SysFont("Arial", 20)
current_algorithm = "Brute Force"

def show_fps_and_particles():
    fps_text = f"FPS: {int(clock.get_fps())}"
    particles_text = f"Particles: {len(env.particles)}"
    fps_surface = fps_font.render(fps_text, True, pyg.Color('black'))
    particles_surface = fps_font.render(particles_text, True, pyg.Color('black'))
    screen.blit(fps_surface, (800, 0))
    screen.blit(particles_surface, (800, 30))

def toggle_pause(env):
    env.pause = not env.pause

def show_speed():
    speed_text = f"Speed: {speed_slider.val:.2f}x"
    speed_surface = fps_font.render(speed_text, True, pyg.Color('black'))
    screen.blit(speed_surface, (800, 60))  


class Button:
    def __init__(self, x, y, width, height, text):
        self.color = (0, 128, 0)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, screen):
        pyg.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        font = pyg.font.SysFont('Arial', 20)    
        text_surf = font.render(self.text, True, (255, 255, 255))
        screen.blit(text_surf, (self.x + (self.width / 2 - text_surf.get_width() / 2),
                                self.y + (self.height / 2 - text_surf.get_height() / 2)))

    def is_over(self, pos):
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            return True
        return False

class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, start_val):
        self.rect = pyg.Rect(x, y, w, h)
        self.min_val = min_val
        self.max_val = max_val
        self.val = start_val
        self.grabbed = False
        self.circle_rect = pyg.Rect(x + w // 2, y - h // 2, h, h)


    def draw(self, screen):
        # Draw the line
        pyg.draw.line(screen, (0, 0, 0), (self.rect.x, self.rect.y + self.rect.height // 2),
                      (self.rect.x + self.rect.width, self.rect.y + self.rect.height // 2), 3)
        # Draw the circle
        pyg.draw.circle(screen, (0, 0, 255), self.circle_rect.center, self.circle_rect.width // 2)

    def handle_event(self, event):
        if event.type == pyg.MOUSEBUTTONDOWN:
            if self.circle_rect.collidepoint(event.pos):
                self.grabbed = True
        elif event.type == pyg.MOUSEBUTTONUP:
            self.grabbed = False
        elif event.type == pyg.MOUSEMOTION and self.grabbed:
            self.circle_rect.x = max(self.rect.x, min(event.pos[0], self.rect.x + self.rect.width))
            self.val = self.min_val + (self.max_val - self.min_val) * ((self.circle_rect.x - self.rect.x) / self.rect.width)
            return True  # Indicates that the value has changed
        return False


# Create buttons and slider
sweep_prune_button = Button(800, 100, 150, 50, 'Sweep & Prune')
kd_tree_button = Button(800, 150, 150, 50, 'KD Tree')
pause_button = Button(800, 250, 150, 50, 'Pause/Resume')
particle_slider = Slider(830, 330, 100, 10, 10, 100, 30) 
speed_slider = Slider(830, 380, 100, 10, 0.5, 5, 1)  
brute_force_button = Button(800, 200, 150, 50, 'Brute Force')



env = Environment(*WINDOW_SIZE)
env.addRandParticle(50)

running = True
while running:
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            running = False
        if event.type == pyg.MOUSEBUTTONDOWN:
            mouse_pos = pyg.mouse.get_pos()
            if sweep_prune_button.is_over(mouse_pos):
                env.set_collision_algorithm('sweepAndPrune')
                current_algorithm = "Sweep and Prune"
                print("Algorithm: Sweep and Prune")
            elif kd_tree_button.is_over(mouse_pos):
                env.set_collision_algorithm('kDTree')
                current_algorithm = "KD Tree"
                print("Algorithm: KD Tree")
            elif brute_force_button.is_over(mouse_pos):
                env.set_collision_algorithm('bruteForce')
                current_algorithm = "Brute Force"
                print("Algorithm: Brute Force")
            elif pause_button.is_over(mouse_pos):
                toggle_pause(env)
                print("Simulation Paused" if env.pause else "Simulation Resumed")
        
        
        # Handle slider event
        if particle_slider.handle_event(event):
            env.set_particle_count(int(particle_slider.val))  # Implement this in Environment
        if speed_slider.handle_event(event):
            env.set_particle_speed(speed_slider.val)

    screen.fill(env.color)
    env.update()

    for p in env.particles:
        pyg.draw.circle(screen, p.color, (p.x, p.y), p.size, p.thickness)

    algo_text = f"Algorithm: {current_algorithm}"
    algo_surface = fps_font.render(algo_text, True, pyg.Color('black'))
    screen.blit(algo_surface, (10, 10))  

    # Draw UI elements
    sweep_prune_button.draw(screen)
    kd_tree_button.draw(screen)
    pause_button.draw(screen)
    particle_slider.draw(screen)
    speed_slider.draw(screen) 
    brute_force_button.draw(screen)


    # Show FPS and Particle Count
    show_fps_and_particles()
    particle_count_text = f"Particles: {len(env.particles)}"
    particle_count_surface = fps_font.render(particle_count_text, True, pyg.Color('black'))
    screen.blit(particle_count_surface, (800, 30))
    show_speed()

    

    pyg.display.flip()
    clock.tick(3000)






