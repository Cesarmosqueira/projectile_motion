from math import radians, sin, cos

STEP = 0.01

class Ball:
    def __init__(self, **kwargs):
        # x: int, y: int,  angle: int, color: vec3
        self.x = 0 if 'x' not in kwargs else kwargs['x']
        self.y = 0 if 'y' not in kwargs else kwargs['y']
        self.angle = radians(45) if 'angle' not in kwargs else kwargs['angle']
        self.color = (144, 41, 43) if 'color' not in kwargs else kwargs['color']
        self.diameter = 20 if 'diameter' not in kwargs else kwargs['diameter']
        self.hover = False
        self.moving = False
        self.time_moving = 0
        self.motion_path = []

    def launch(self, speed):
        self.moving = True
        self.__load_launch_params(speed)

    def __load_launch_params(self, speed):
        self.time_moving = 0
        self.speed = speed
        self.starting_point = float(self.x), float(self.y)
        self.motion_path = []
    
    def on_update(self):
        # print(f"x = {self.x} y = {self.y}")
        if not self.moving: return
        self.time_moving += STEP


        vx = cos(self.angle) * self.speed * 0.2
        vy = sin(self.angle) * self.speed * 0.8

        # print(f"vx = {vx}\nvy = {vy}\n")
        
        self.x += vx
        self.y += vy * self.time_moving + (9.81 * -self.time_moving**2)/2

        if self.y < self.starting_point[1]:
            print(f'y = {self.y} old_y = {self.starting_point[1]}')
            self.y = self.starting_point[1]
            self.moving = False

        if int(self.time_moving * 100) % 5 == 0:
            self.motion_path += [(self.x, self.y)]


