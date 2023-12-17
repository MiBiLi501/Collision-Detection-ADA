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
    def __init__(self, x, y, width, height, min_val, max_val, start_val):
        self.rect = pyg.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.val = start_val
        self.grabbed = False
        self.circle_radius = 10
        self.circle_rect = pyg.Rect(0, 0, self.circle_radius * 2, self.circle_radius * 2)
        self.circle_rect.center = self.get_pos_from_val(self.val)

    def get_pos_from_val(self, val):
        return (self.rect.x + (val - self.min_val) / (self.max_val - self.min_val) * self.rect.width, self.rect.centery)

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
            self.val = round(self.min_val + (self.max_val - self.min_val) * ((self.circle_rect.x - self.rect.x) / self.rect.width))
            return True  # Indicates that the value has changed
        return False
    
    def set_val(self, val):
        self.val = val
        self.circle_rect.center = self.get_pos_from_val(val)

 
# Create buttons and slider
sweep_prune_button = Button(800, 350, 150, 50, 'Sweep & Prune')
kd_tree_button = Button(800, 400, 150, 50, 'KD Tree')
pause_button = Button(800, 500, 150, 50, 'Pause/Resume')
particle_slider = Slider(10, 580, 980, 10, 10, 400, 50) 
# speed_slider = Slider(830, 380, 100, 10, 0.5, 5, 1)  
brute_force_button = Button(800, 450, 150, 50, 'Brute Force')

env = Environment(*WINDOW_SIZE)
env.addRandParticle(50)

text_box = pyg.Rect(50, 50, 140, 32)
input_string = ""
is_text_box_clicked = False

speed_text_box = pyg.Rect(50, 100, 140, 32)  # Position it below the particle count text box
speed_input_string = ""
is_speed_text_box_clicked = False
default_speed_multiplier = 1.0

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
            
            if text_box.collidepoint(event.pos):
                is_text_box_clicked = True
            else:
                is_text_box_clicked = False

        if event.type == pyg.MOUSEMOTION:
            if text_box.collidepoint(event.pos):
                cursor = pyg.cursors.compile(pyg.cursors.textmarker_strings)
                pyg.mouse.set_cursor((8, 16), (0, 0), *cursor)
            else:
                pyg.mouse.set_cursor(*pyg.cursors.arrow)
        
        if event.type == pyg.KEYDOWN and is_text_box_clicked:
            if event.key == pyg.K_BACKSPACE:
                input_string = input_string[:-1]
            elif event.unicode.isdigit():
                input_string += event.unicode
            elif event.key == pyg.K_RETURN:
                particle_count = int(input_string)
                env.set_particle_count(particle_count)
                particle_slider.set_val(particle_count)
                input_string = ""

        if env.pause:
            if particle_slider.handle_event(event):
                env.set_particle_count(int(particle_slider.val))  
        

        if event.type == pyg.MOUSEBUTTONDOWN:
            if speed_text_box.collidepoint(event.pos):
                is_speed_text_box_clicked = True
            else:
                is_speed_text_box_clicked = False

        if event.type == pyg.KEYDOWN and is_speed_text_box_clicked:
            if event.key == pyg.K_BACKSPACE:
                speed_input_string = speed_input_string[:-1]
            elif event.unicode.isdigit() or event.unicode == '.':
                speed_input_string += event.unicode
            elif event.key == pyg.K_RETURN:
                try:
                    new_speed = float(speed_input_string)
                    env.set_particle_speed(new_speed * default_speed_multiplier)
                except ValueError:
                    print("Invalid speed input")
                speed_input_string = ""

    # ... [Your existing drawing code here] ...

    # Draw speed text box
    speed_txt_surface = fps_font.render(speed_input_string, True, pyg.Color('black'))
    screen.blit(speed_txt_surface, (speed_text_box.x + 5, speed_text_box.y + 5))
    pyg.draw.rect(screen, pyg.Color('black'), speed_text_box, 2)
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
    # speed_slider.draw(screen) 
    brute_force_button.draw(screen)


    # Show FPS and Particle Count
    show_fps_and_particles()
    particle_count_text = f"Particles: {len(env.particles)}"
    particle_count_surface = fps_font.render(particle_count_text, True, pyg.Color('black'))
    screen.blit(particle_count_surface, (800, 30))
    # show_speed()

    txt_surface = fps_font.render(input_string, True, pyg.Color('black'))
    screen.blit(txt_surface, (text_box.x+5, text_box.y+5))

    speed_txt_surface = fps_font.render(speed_input_string, True, pyg.Color('black'))
    screen.blit(speed_txt_surface, (speed_text_box.x + 5, speed_text_box.y + 5))
    pyg.draw.rect(screen, pyg.Color('black'), speed_text_box, 2)

    pyg.draw.rect(screen, pyg.Color('black'), text_box, 2)
  
    pyg.display.flip()
    clock.tick(3000)





