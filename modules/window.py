import pygame
import math
from typing import List
from ball import Ball

MAX_MASS = 300

def draw_nice_rectangle(window, x,y,w,h, bg, border, shadow):
    pygame.draw.line(window, border, (x, y), (x + w , y), 5)
    pygame.draw.line(window, border, (x, y - 2), (x, y + h), 5)
    pygame.draw.line(window, shadow, (x, y + h), (x + w , y + h), 5)
    pygame.draw.line(window, shadow, (x + w , y+h), [x + w , y], 5)
    pygame.draw.rect(window, bg, (x, y, w , h))


class Button:
    def __init__(self, position, text, fontsize):
        self.text = text
        self.font = pygame.font.SysFont("Arial", fontsize)
        self.text_render = self.font.render(self.text, 1, (255, 0, 0))
        self.x, self.y, self.w , self.h = self.text_render.get_rect()
        self.x, self.y = position

    def on_update(self, window, **kwargs):
        bg = (100, 100, 100) if 'bg' not in kwargs else kwargs['bg']
        border = (150, 150, 150) if 'border' not in kwargs else kwargs['border']
        shadow = (50, 50, 50) if 'shadow' not in kwargs else kwargs['shadow']
        value = "N" if 'value' not in kwargs else kwargs['value']
        r_offset = 3 if 'r_offset' not in kwargs else kwargs['r_offset']

        if value != "N":
            self.text = value + ' '

        self.text_render = self.font.render(self.text, 1, (255, 0, 0))
        draw_nice_rectangle(window, self.x, self.y, self.w + r_offset, self.h, \
                bg, border, shadow)
        if 'x_offset' in kwargs:
            return window.blit(self.text_render, (self.x + kwargs['x_offset'], self.y))
        else:
            return window.blit(self.text_render, (self.x, self.y))

    def blit(self, window, x_offset = 0):
        return window.blit(self.text_render, (self.x + x_offset, self.y))

class Modifier:
    # Contains two buttons to modify a value up and down
    # Contains a label showing variable name and its value
    def __init__(self, pos, text, fontsize, **kwargs):
        self.label = Button(pos, text, fontsize)
        step = 5 if 'step' not in kwargs else kwargs['step']
        x, y, w, h = self.label.x, self.label.y, self.label.w, self.label.h
        self.step = step

        self.modifier_up = Button((x+w+8, int(y-h*0.4)), "+", int(fontsize*1.02))
        self.modifier_down = Button((x+w+8, int(y+h*0.3)), "-", int(fontsize*1.09))

        self.x, self.y = pos
        self.w = int(w + 0.5*(self.modifier_up.w + self.modifier_down.w))
        self.h = int(h + 0.5*(self.modifier_up.h + self.modifier_down.h))
        self.down_label = Button((x+w//4.2, y+20), text, int(fontsize*0.5))

    def on_update(self, window, bg_color=(100,100,100), **kwargs):
        r_offset = 3 if 'r_offset' not in kwargs else kwargs['r_offset']
        value = '- ' if 'value' not in kwargs else kwargs['value']
    
        if 'x_offset' in kwargs:
            self.modifier_down.on_update(window, bg=bg_color, shadow=bg_color, border=bg_color, x_offset=kwargs['x_offset'])
            self.modifier_up.on_update(window, bg=bg_color, shadow=bg_color, border=bg_color, x_offset=kwargs['x_offset'])
        else:
            self.modifier_down.on_update(window, bg=bg_color, shadow=bg_color, border=bg_color)
            self.modifier_up.on_update(window, bg=bg_color, shadow=bg_color, border=bg_color)

        self.label.on_update(window, value=value, bg=bg_color, border=bg_color, r_offset=r_offset)
        self.down_label.on_update(window, bg=bg_color, border=bg_color)


    def on_click(self, window, mousepos, x_offset=0):
        if self.modifier_down.blit(window, x_offset).collidepoint(mousepos):
            return self.step * -1
        elif self.modifier_up.blit(window, x_offset).collidepoint(mousepos):
            return self.step
        else: return 0


V_XOFFSET = 23 
R_XOFFSET = 17
M_XOFFSET = 23

class Window:
    def __init__(self, w, h):
        pygame.init()
        self.width, self.height = w, h
        self.ceiling = w*0.92
        self.window = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.balls = []
        self.hover_ball = 0
        self.velocity = 50
        self.drag_coefficient = 47
        self.air_density = 1.2

        self.x_modifier  = Modifier((10,10), "X: - ", 18, step=10)
        self.y_modifier  = Modifier((67,10), "Y: - ", 18, step=10)
        self.v_modifier  = Modifier((150,10), "V: - ", 20, step=1)
        self.r_modifier  = Modifier((240,10), "R: - ", 20, step=2)
        self.dc_modifier = Modifier((320,10), "C: - ", 20, step = 5)
        self.mass_modifier = Modifier((400,10), "m: - ", 20, step = 5)
        self.p_modifier = Modifier((500,10), "p: - ", 20, step = 0.2)


    def update_balls(self, balls:List[Ball]):
        # Receive ball array from main module
        self.balls = balls
        self.__focus_ball(0)

    def __focus_ball(self, dir):
        # Changes ball being focused
        if len(self.balls) == 0: return
        self.balls[self.hover_ball].hover = False
        if 0 <= self.hover_ball + dir \
            and self.hover_ball + dir < len(self.balls):
                self.hover_ball += dir

        self.balls[self.hover_ball].hover = True

    def __get_reference_point(self, center, angle, radius):
        # Line inside circles
        x, y = center
        ref_x = math.cos(angle) * radius + x - 1
        ref_y = math.sin(angle) * radius + y - 1
        return int(ref_x), self.height-int(ref_y)

    def __update_mods(self, x_mod, y_mod, v_mod, r_mod, dc_mod, mass_mod, density_mod):
        if len(self.balls):
            if 0 <= self.balls[self.hover_ball].x + x_mod and \
                    self.balls[self.hover_ball].x + x_mod <= self.width:
                self.balls[self.hover_ball].x += x_mod
        if len(self.balls):
            if 0 <= self.balls[self.hover_ball].y + y_mod and \
                    self.balls[self.hover_ball].y + y_mod <= self.ceiling:
                self.balls[self.hover_ball].y += y_mod
             
            if 0 <= self.balls[self.hover_ball].mass - mass_mod and \
                    self.balls[self.hover_ball].mass - mass_mod <= MAX_MASS:
                self.balls[self.hover_ball].mass -= mass_mod

            if 10 <= self.balls[self.hover_ball].diameter//2 + r_mod and \
                self.balls[self.hover_ball].diameter//2 + r_mod <= 30:
                self.balls[self.hover_ball].update_diameter(r_mod, 30)
        if 0 <= self.air_density + density_mod and self.air_density + density_mod <= 5:
            self.air_density += density_mod
    
        if 50 <= self.velocity + v_mod and self.velocity + v_mod <= 80:
            self.velocity += v_mod
        if 0 <= self.drag_coefficient + dc_mod and self.drag_coefficient + dc_mod <= 50:
            self.drag_coefficient += dc_mod

    def draw_call(self):
        bg_color = (130,130,130)
        for ball in self.balls:
            reference = self.__get_reference_point((ball.x, ball.y), 
                    ball.angle, ball.diameter/2)
            pygame.draw.circle(self.window,
                                ball.color if not ball.hover else (122,255,33),
                    [ball.x, self.height-ball.y], ball.diameter/2)

            if ball.hover:
                pygame.draw.circle(self.window,
                                    ball.color,
                        [ball.x, self.height-ball.y], ball.diameter/2, width=int(ball.mass*0.05))



            pygame.draw.line(self.window, (0,0,0),
                    (ball.x, self.height-ball.y), 
                    reference, 
                    int(ball.diameter*0.05))
            if ball.moving:
                pygame.draw.circle(self.window, (256-235, 256-239, 256-18), \
                        [ball.x, self.height - ball.y], ball.diameter*0.1)
            if len(ball.motion_path):
                for p in ball.motion_path:
                    pygame.draw.circle(self.window, (235, 239, 18), \
                            [p[0], self.height - p[1]], 2)

        # nice neat top bar 
        draw_nice_rectangle(self.window, 0, 0, self.width, self.height*0.08, \
                bg_color, (150, 150, 150), (50, 50, 50))

        draw_nice_rectangle(self.window, 0, self.height-30, self.width, 30, \
                bg_color, (150, 150, 150), (50, 50, 50))

        # modifiers inside bar
        self.x_modifier.on_update(self.window, bg_color, value = f"{int(self.balls[self.hover_ball].x)}m")
        self.y_modifier.on_update(self.window, bg_color, value = f"{int(self.balls[self.hover_ball].y)}m")
        self.r_modifier.on_update(self.window, bg_color, value = f"{int(self.balls[self.hover_ball].diameter/2)}cm", r_offset=R_XOFFSET, x_offset=R_XOFFSET)
        self.mass_modifier.on_update(self.window, bg_color, value = f"{MAX_MASS - int(self.balls[self.hover_ball].mass)}kg", r_offset=M_XOFFSET, x_offset= M_XOFFSET)

        self.v_modifier.on_update(self.window, bg_color, value = f"{self.velocity}m/s", r_offset=V_XOFFSET, x_offset=V_XOFFSET)
        self.dc_modifier.on_update(self.window, bg_color, value = f"{self.drag_coefficient}c")
        self.p_modifier.on_update(self.window, bg_color, value = f"{round(self.air_density,2)}d", r_offset=R_XOFFSET, x_offset=R_XOFFSET)


    def move_balls(self):
        for ball in self.balls:
            ball.on_update()


    def on_update(self, step, framerate):
        ang=math.radians(5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_LEFT:
                    self.__focus_ball(-1)
                elif event.key == pygame.K_RIGHT:
                    self.__focus_ball(1)
                elif event.key == pygame.K_UP:
                    for b in self.balls:
                        if not b.moving:
                            b.angle -= ang
                elif event.key == pygame.K_DOWN:
                    for b in self.balls:
                        if not b.moving:
                            b.angle += ang
                elif event.key == pygame.K_SPACE:
                    if len(self.balls):
                        self.balls[self.hover_ball].launch(self.velocity, \
                                resistance_q=self.drag_coefficient/100, air_density=self.air_density)

            if event.type == pygame.MOUSEBUTTONDOWN:
                x_mod = self.x_modifier.on_click(self.window, pygame.mouse.get_pos())
                y_mod = self.y_modifier.on_click(self.window, pygame.mouse.get_pos())
                v_mod = self.v_modifier.on_click(self.window, pygame.mouse.get_pos(), V_XOFFSET)
                r_mod = self.r_modifier.on_click(self.window, pygame.mouse.get_pos(), R_XOFFSET)
                mass_mod = self.mass_modifier.on_click(self.window, pygame.mouse.get_pos(), M_XOFFSET)
                dc_mod = self.dc_modifier.on_click(self.window, pygame.mouse.get_pos())
                density_mod = self.p_modifier.on_click(self.window, pygame.mouse.get_pos(), x_offset=R_XOFFSET)
                self.__update_mods(x_mod, y_mod, v_mod, r_mod, dc_mod, mass_mod, density_mod)


        _delta = self.clock.tick(framerate)
        self.window.fill((164, 188, 255))
        self.draw_call() 

        pygame.time.wait(step)
        pygame.display.update()
        return True
    
    def close(self):
        pygame.quit()
        pass
