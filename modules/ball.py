from math import radians, sin, cos

STEP = 0.01
GRAVITY = 5

class Ball:
    def __init__(self, **kwargs):
        # x: int, y: int,  angle: int, color: vec3
        self.x = 0 if 'x' not in kwargs else kwargs['x']
        self.y = 0 if 'y' not in kwargs else kwargs['y']
        self.angle = radians(45) if 'angle' not in kwargs else kwargs['angle']
        self.color = (144, 41, 43) if 'color' not in kwargs else kwargs['color']
        self.diameter = 20 if 'diameter' not in kwargs else kwargs['diameter']
        self.mass_radius_ratio = 3
        self.mass = self.diameter*self.mass_radius_ratio if 'mass' not in kwargs else kwargs['mass']
        self.relative_mass = 'mass' not in kwargs
        self.hover = False
        self.moving = False
        self.time_moving = 0
        self.motion_path = []
        self.y = 32 + self.diameter//2

    def launch(self, speed, parameter_range=(50,80), resistance_q = 0.2, air_density=1.20):
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
            self.y = self.__floor(floor_level)


    def __load_launch_params(self, speed, k):
        self.drag_coefficient = k
        self.time_moving = 0
        self.speed = speed

        self.velocity_x = self.speed * cos(self.angle)
        self.velocity_y = self.speed * sin(self.angle)


        self.motion_path = []

    def __floor(self, floor_level):
        return floor_level + self.diameter//2
    
    def on_update(self, width = 600, floor_level = 30):
        # print(f"x = {self.x} y = {self.y}")
        if not self.moving: return
        self.time_moving += STEP

        k = self.drag_coefficient * 0.6

        aX = -k * self.speed * self.velocity_x
        self.velocity_x += aX * self.time_moving
        dx = self.velocity_x * self.time_moving - 0.5 * aX * pow( self.time_moving , 2 )
        dx *= 100

        aY = -GRAVITY - k * self.speed * self.velocity_y
        self.velocity_y += aY * self.time_moving
        dy = self.velocity_y * self.time_moving - 0.5 * aY * pow( self.time_moving , 2 )
        dy *= 100

        # print(f"vx = {vx}\nvy = {vy}\n")
        if 0 <= self.x + dx and self.x + dx <= width:
            self.x += dx
        self.y += dy

        print(f"{str(self.x)[:5]}\t{str(self.y)[:5]}")

        if self.y < self.__floor(floor_level):
            self.y = self.__floor(floor_level)
            self.moving = False

        if int(self.time_moving * 100) % 2 == 0:
            self.motion_path += [(self.x, self.y)]


