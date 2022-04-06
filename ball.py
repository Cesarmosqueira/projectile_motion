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

    def load_launch_params(self, speed):
        self.speed = speed
        self.starting_point = self.x, self.y
        pass
    


    def on_update(self):
        if not self.moving: return
        self.time_moving += STEP


        vx = cos(self.speed)
        vy = sin(self.speed) + (0.981 * self.time_moving**2)/2
        
        self.x += vx
        self.y += vy


        

        
        pass

      



