import numpy as np
import numpy as np

from pyglet.gl import *
from fos import Actor, World, Window
from pyglet.text import Label
from pyglet.graphics import Batch

class Labels(Actor):    
    #def __init__(self, *args, **kwargs):
    def __init__(self,positions,texts,fonts,fonts_size,colors=None,dpi=50,follow=True):
            
        self.textures=[]    
        for (i,p) in enumerate(positions):
        
            label=pyglet.text.Label(texts[i], font_name=fonts[i], 
                                  font_size=fonts_size[i],
                                  dpi=dpi,
                                  anchor_x='center', anchor_y='center')
            self.textures.append(label2texture(label))
            
    def update(self, dt):
        pass
        
    def draw(self):        
        glPushMatrix()                
        #self.batch.draw()
        for i in range(len(self.textures)):
            self.textures[i].blit(0,0)
        glPopMatrix()

def label2texture(label):
    ''' from pyglet.texture to  
    Thank you http://paste.pocoo.org/show/89317/
    '''
    
    vertex_list = label._vertex_lists[0].vertices[:]
    xpos = map(int, vertex_list[::8])
    ypos = map(int, vertex_list[1::8])
    glyphs = label._get_glyphs()

    xstart = xpos[0]
    xend = xpos[-1] + glyphs[-1].width
    width = xend - xstart

    ystart = min(ypos)
    yend = max(ystart+glyph.height for glyph in glyphs)
    height = yend - ystart

    texture = pyglet.image.Texture.create(width, height, pyglet.gl.GL_RGBA)

    for glyph, x, y in zip(glyphs, xpos, ypos):
        data = glyph.get_image_data()
        x = x - xstart
        y =  height - glyph.height - y + ystart
        texture.blit_into(data, x, y, 0)

    return texture.get_transform(flip_y=True)


                
if __name__ == '__main__':
    wi = Window()
    w = wi.get_world()
        
    positions=np.array([[-1,0,0],[0,0,0],[1,0,0]])
    texts=['Stefan','Eleftherios','Ian']
    fonts=['Times New Roman']*3
    fonts_size=[10]*3
    
    l=Labels(positions,texts,fonts,fonts_size)
    w.add(l)  
    
    

