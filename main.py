import sys
sys.path.append('modules/')
from window import Window # pylint: disable=(import-error)
from ball import Ball # pylint: disable=(import-error)


window = Window(600, 600)
step, fps = 15, 60

# Keep diameter from 20 above
objects = [Ball(x = 30, y = 30, diameter=50), Ball(x = 100, y = 30, diameter=20)]

window.update_balls(objects)
while window.on_update(15, 60):
    window.move_balls()
    pass

window.close()
