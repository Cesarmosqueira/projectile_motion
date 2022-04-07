import pygame
import math
from typing import List
from ball import Ball

# def button(screen, position, text):

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

        self.text_render = self.font.render(self.text, 1, (255, 0, 0))
        draw_nice_rectangle(window, self.x, self.y, self.w , self.h, \
                bg, border, shadow)
        return window.blit(self.text_render, (self.x, self.y))

    def blit(self, window):
        return window.blit(self.text_render, (self.x, self.y))

class Modifier:
    def __init__(self, pos, text, fontsize):
        self.label = Button(pos, text, fontsize)
        x, y, w, h = self.label.x, self.label.y, self.label.w, self.label.h

        self.modifier_up = Button((x+w+3, int(y-h*0.4)), "+", int(fontsize*1.02))
        self.modifier_down = Button((x+w+5, int(y+h*0.3)), "-", int(fontsize*1.09))

        self.x, self.y = pos
        self.w = int(w + 0.5*(self.modifier_up.w + self.modifier_down.w))
        self.h = int(h + 0.5*(self.modifier_up.h + self.modifier_down.h))

    def on_update(self, window, bg_color=(100,100,100)):
        self.modifier_down.on_update(window, bg=bg_color, shadow=bg_color, border=bg_color )
        self.modifier_up.on_update(window, bg=bg_color, shadow=bg_color, border=bg_color )
        self.label.on_update(window, bg=bg_color, border=bg_color)

    def on_click(self, window, mousepos):
        if self.modifier_down.blit(window).collidepoint(mousepos):
            print('minus pressed')
        elif self.modifier_up.blit(window).collidepoint(mousepos):
            print('plus pressed')



class Window:
    def __init__(self, w, h):
        pygame.init()
        self.width, self.height = w, h
        self.window = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.balls = []
        self.hover_ball = 0

        self.x_modifier = Modifier((10,10), "X:", 20)
        self.y_modifier = Modifier((50,10), "Y:", 20)


    def update_balls(self, balls:List[Ball]):
        self.balls = balls
        self.__focus_ball(0)

    def __focus_ball(self, dir):
        if len(self.balls) == 0: return
        self.balls[self.hover_ball].hover = False
        if 0 <= self.hover_ball + dir \
            and self.hover_ball + dir < len(self.balls):
                self.hover_ball += dir

        self.balls[self.hover_ball].hover = True

    def __get_reference_point(self, center, angle, radius):
        x, y = center
        ref_x = math.cos(angle) * radius + x - 1
        ref_y = math.sin(angle) * radius + y - 1
        return int(ref_x), self.height-int(ref_y)
    

    def draw_call(self):
        bg_color = (130,130,130)
# Posición inicial de lanzamiento (m) [0,00; 0,00]
# Rapidez inicial (m/s) [50,0 ; 80,0]
# Radio (cm) [10,0 ; 30,0]
# Coeficiente de resistencia (CD) 0,500
# Masa (kg) [0,140; 0,350]
# Ángulo de lanzamiento [20,0°; 70,0°]
# Densidad del aire (kg/m3
# ) 1,20


        # nice neat top bar 
        draw_nice_rectangle(self.window, 0, 0, self.width, self.height*0.08, \
                bg_color, (150, 150, 150), (50, 50, 50))

        # modifiers inside bar
        self.x_modifier.on_update(self.window, bg_color)
        self.y_modifier.on_update(self.window, bg_color)

        for ball in self.balls:
            reference = self.__get_reference_point((ball.x, ball.y), 
                    ball.angle, ball.diameter/2)
            pygame.draw.circle(self.window,
                                ball.color if not ball.hover else (122,255,33),
                    [ball.x, self.height-ball.y], ball.diameter/2)

            pygame.draw.line(self.window, (0,0,0),
                    (ball.x, self.height-ball.y), 
                    reference, 
                    int(ball.diameter*0.05))
            if ball.moving:
                pygame.draw.circle(self.window, (235, 239, 18), \
                        [ball.x, self.height - ball.y], ball.diameter*0.1)
            if len(ball.motion_path):
                for p in ball.motion_path:
                    pygame.draw.circle(self.window, (235, 239, 18), \
                            [p[0], self.height - p[1]], 1)


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
                            b.angle += ang
                    # print(f'+{ang} angle = {self.balls[0].angle}')
                elif event.key == pygame.K_DOWN:
                    for b in self.balls:
                        if not b.moving:
                            b.angle -= ang
                    # print(f'-{ang} angle = {self.balls[0].angle}')
                elif event.key == pygame.K_SPACE:
                    if len(self.balls):
                        self.balls[self.hover_ball].launch(10)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.x_modifier.on_click(self.window, pygame.mouse.get_pos())

        _delta = self.clock.tick(framerate)
        self.window.fill((164, 188, 255))
        self.draw_call() 

        pygame.time.wait(step)
        pygame.display.update()
        return True
    
    def close(self):
        pygame.quit()
        pass
