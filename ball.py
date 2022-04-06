from math import radians
class Ball:
    def __init__(self, **kwargs):
        # x: int, y: int,  angle: int, color: vec3
        self.x = 0 if 'x' not in kwargs else kwargs['x']
        self.y = 0 if 'y' not in kwargs else kwargs['y']
        self.angle = radians(45) if 'angle' not in kwargs else kwargs['angle']
        self.color = (144, 41, 43) if 'color' not in kwargs else kwargs['color']
        self.diameter = 20 if 'diameter' not in kwargs else kwargs['diameter']
        self.hover = False



