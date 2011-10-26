""" The FosWindow Event Handler """

from fos.lib.pyglet.window import key,mouse
from fos.core.utils import screen_to_model

class FosWinEventHandler(object):
    
    def __init__(self, window):        
        self.window = window           

    def on_key_press(self, symbol, modifiers):
        
        if symbol not in [key.R, key.H]:            
            self.window._world.propagate_keys(symbol, modifiers)
                  
        
        # how to propagate the events to the actors and camera?            
        if symbol == key.R:
            self.window.current_camera.reset()        
        if symbol == key.H:
            self.window.set_size(1000, 600)            
        if modifiers & key.MOD_CTRL:
            # make window bigger
            if symbol == key.PLUS:
                neww = self.window.width + self.window.width / 10
                newh = self.window.height + self.window.height / 10
                self.window.set_size(neww, newh)
            # make window smaller
            elif symbol == key.MINUS:
                neww = self.window.width - self.window.width / 10
                newh = self.window.height - self.window.height / 10
                self.window.set_size(neww, newh)
                 
        if symbol == key.P:
            x,y=self.window.mouse_x,self.window.mouse_y
            nx,ny,nz=screen_to_model(x,y,0)
            fx,fy,fz=screen_to_model(x,y,1)        
            near=(nx,ny,nz)
            far=(fx,fy,fz)           
            self.window._world.propagate_pickray(near, far)
            
        # with s, select and actor and focus the camera, make the aabb glowing,
        # d to deselect, push new set of events for this actor
        """ 
        if symbol == key.S:          
            # select aabb
            x,y=self.window.mouse_x,self.window.mouse_y
            nx,ny,nz=screen_to_model(x,y,0)
            fx,fy,fz=screen_to_model(x,y,1)        
            near=(nx,ny,nz)
            far=(fx,fy,fz)
            found_actor = self.window._world.find_selected_actor(near, far)
            if not found_actor is None:
                print("found an actor that was selected")
                found_actor.show_aabb = not found_actor.show_aabb                
            else:
                print("no actor found")
        """

    def on_mouse_motion(self, x, y, dx, dy):
        self.window.mouse_x, self.window.mouse_y = x, y
        self.window._world.propagate_mouse_motion(x, y, dx, dy)
        
        
    def on_mouse_drag(self, x,y,dx,dy,buttons,modifiers):
        if buttons & mouse.LEFT:
            if modifiers & key.MOD_CTRL:
                print('ctrl dragging')
            else:
                self.window.current_camera.cam_rot.rotate( dx*self.window.current_camera.mouse_speed,0,1,0)
                self.window.current_camera.cam_rot.rotate(-dy*self.window.current_camera.mouse_speed,1,0,0)                
        if buttons & mouse.RIGHT:
            tx=dx*self.window.current_camera.mouse_speed
            ty=dy*self.window.current_camera.mouse_speed        
            self.window.current_camera.cam_trans.translate(tx,ty,0)    
        if buttons & mouse.MIDDLE:
            tz=dy*self.window.current_camera.mouse_speed
            self.window.current_camera.cam_trans.translate(0,0,tz)
    
    def on_mouse_scroll(self, x,y,scroll_x,scroll_y):
        self.window.current_camera.cam_trans.translate(0,0,scroll_y*self.window.current_camera.scroll_speed)


