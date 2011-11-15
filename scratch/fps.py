import pyglet as pyglet

window = pyglet.window.Window()

#fps_display = pyglet.window.FPSDisplay(window)

clock_display = pyglet.clock.ClockDisplay()

@window.event
def on_draw():
    # ... perform ordinary window drawing operations ...
    window.clear()
    clock_display.draw()
 #   fps_display.draw()

pyglet.app.run()