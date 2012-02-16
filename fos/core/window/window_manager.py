""" Window Manager - manages all of the windows for the application and 
                     contains the main update loop """

from threading import Thread, Lock

class WindowManager:
    
    def __init__(self):
        """Create a WindowManager. """        
        self.window_list = []
        pass
    
    def add(self, window):
        """Add a window to the window manager"""
        self.window_list.append(window)        
    
    def remove(self, window):
        """Remove a window from the window manager and from memory"""
        self.window_list.remove(window)
        try:
            del window
        except Exception as e:
            print e
            
    def run(self):
        """Start the main loop for the program"""
        self.Thread=Thread(target=self.__main_loop__)
        self.Thread.start()
        
    def __main_loop__(self):
        """The main loop, create the windows here so that they are
           stored in the thread, then update all windows continuously until exited """        
        
        for window in self.window_list:
            window.create_window()
                
        while len(self.window_list) > 0:            
            for window in self.window_list:
                if window.has_exit == False:
                    window.process_frame()
                else:                    
                    self.remove(window)                    
                    break                    
