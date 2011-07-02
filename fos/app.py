import fos.lib.pyglet as pyglet
import fos.lib.pyglet.app.base

class MyEventLoop(fos.lib.pyglet.app.base.EventLoop):

    # only overwrite idle
    def idle(self):
        dt = self.clock.update_time()
        redraw_all = self.clock.call_scheduled_functions(dt)

        # Redraw all windows
        for window in pyglet.app.windows:
            if redraw_all or (window._legacy_invalid and window.invalid):
                window.switch_to()
                window.dispatch_event('on_draw')
                window.flip()
                window._legacy_invalid = False

        # Update timout
        return self.clock.get_sleep_time(True)

    def exit(self):
        print "exit my own event loop"
        # call parent
        pyglet.app.base.EventLoop.exit(self)


def run():
    """ Run Fos event loop """
    pyglet.app.event_loop = MyEventLoop()
    pyglet.app.run()
