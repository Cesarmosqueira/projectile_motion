from window import Window
from ball import Ball


window = Window(600, 600)
step, fps = 15, 60

# Keep diameter from 20 above
objects = [Ball(x = 30, y = 30, diameter=90), Ball(x = 100, y = 30, diameter=20)]

window.update_balls(objects)
while window.on_update(15, 60):
        

    pass

window.close()
            

