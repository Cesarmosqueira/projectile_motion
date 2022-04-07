from math import radians, sin, cos

STEP = 0.01
GRAVITY = 11

class Ball:
    def __init__(self, **kwargs):
        # x: int, y: int,  angle: int, color: vec3
        self.x = 0 if 'x' not in kwargs else kwargs['x']
        self.y = 0 if 'y' not in kwargs else kwargs['y']
        self.angle = radians(45) if 'angle' not in kwargs else kwargs['angle']
        self.color = (144, 41, 43) if 'color' not in kwargs else kwargs['color']
        self.diameter = 20 if 'diameter' not in kwargs else kwargs['diameter']
        self.mass_radius_ratio = 5.0
        self.mass = self.diameter*self.mass_radius_ratio if 'mass' not in kwargs else kwargs['mass']
        self.relative_mass = 'mass' not in kwargs
        self.hover = False
        self.moving = False
        self.time_moving = 0
        self.motion_path = []
        self.y = 32 + self.diameter//2

    def launch(self, speed, parameter_range=(50,80), resistance_q = 250, air_density=1.20):
        self.moving = True
        # launch speedd range 2 - 10
        bot, top = parameter_range
        min_speed, max_speed = 5, 13

        m = (max_speed - min_speed)/(top - bot)
        cvt_speed = m*(speed-bot) + min_speed

        drag_coefficient =  (( resistance_q * air_density * (self.diameter/2)**2 ) / 2)/ self.mass

        self.__load_launch_params(cvt_speed, drag_coefficient)

        

    def update_diameter(self, mod, floor_level):
        self.diameter += mod
        if not self.relative_mass:
            self.mass += mod*self.mass_radius_ratio
        if not self.moving:
            self.y = self.__floor(30)


    def __load_launch_params(self, speed, k):
        self.drag_coefficient = k
        self.time_moving = 0
        self.speed = speed
        self.motion_path = []

    def __floor(self, floor_level):
        return floor_level + self.diameter//2
    
    def on_update(self, width = 600, floor_level = 30):
        # print(f"x = {self.x} y = {self.y}")
        if not self.moving: return
        self.time_moving += STEP

        k = self.drag_coefficient


        vx = 0.6 * cos(self.angle) * self.speed * 0.4
        vy = sin(self.angle) * self.speed * 0.6


        # print(f"vx = {vx}\nvy = {vy}\n")
        if 0 <= self.x + vx and self.x + vx <= width:
            self.x += vx

        self.y += vy * self.time_moving + (GRAVITY * -self.time_moving**2) / 2

        if self.y < self.__floor(floor_level):
            self.y = self.__floor(floor_level)
            self.moving = False

        if int(self.time_moving * 100) % 5 == 0:
            self.motion_path += [(self.x, self.y)]


