import pygame
import math
from typing import List
from ball import Ball

# def button(screen, position, text):

class Button:
    def __init__(self, position, text):
        self.text = text
        self.font = pygame.font.SysFont("Arial", 50)
        self.text_render = self.font.render(self.text, 1, (255, 0, 0))
        self.x, self.y, self.w , self.h = self.text_render.get_rect()
        self.x, self.y = position

    def on_update(self, window):
        self.text_render = self.font.render(self.text, 1, (255, 0, 0))
        x,y,w,h = self.x, self.y, self.w , self.h
        pygame.draw.line(window, (150, 150, 150), (x, y), (x + w , y), 5)
        pygame.draw.line(window, (150, 150, 150), (x, y - 2), (x, y + h), 5)
        pygame.draw.line(window, (50, 50, 50), (x, y + h), (x + w , y + h), 5)
        pygame.draw.line(window, (50, 50, 50), (x + w , y+h), [x + w , y], 5)
        pygame.draw.rect(window, (100, 100, 100), (x, y, w , h))
        return window.blit(self.text_render, (x, y))

    def blit(self, window):
        return window.blit(self.text_render, (self.x, self.y))


class Window:
    def __init__(self, w, h):
        pygame.init()
        self.width, self.height = w, h
        self.window = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.balls = []
        self.hover_ball = 0
        self.b1 = Button((400, 300), "Quit")
        self.b2 = Button((500, 300), "Start")


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
        # nice neat top bar 

        # buttons for top bar
        self.b1.on_update(self.window)
        self.b2.on_update(self.window)
        
        # labels for top bar

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
                        b.angle += ang
                    # print(f'+{ang} angle = {self.balls[0].angle}')
                elif event.key == pygame.K_DOWN:
                    for b in self.balls:
                        b.angle -= ang
                    # print(f'-{ang} angle = {self.balls[0].angle}')
                elif event.key == pygame.K_SPACE:
                    if len(self.balls):
                        self.balls[self.hover_ball].launch(10)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.b1.blit(self.window).collidepoint(pygame.mouse.get_pos()):
                    print('quit pressed')
                elif self.b2.blit(self.window).collidepoint(pygame.mouse.get_pos()):
                    print('start pressed')

        _delta = self.clock.tick(framerate)
        self.window.fill((164, 188, 255))
        self.draw_call() 

        pygame.time.wait(step)
        pygame.display.update()
        return True
    
    def close(self):
        pygame.quit()
        pass
