import fos.lib.pyglet as pyglet

def load_animation(image_name,columns,rows):
 
    frame_seq = pyglet.image.ImageGrid(pyglet.image.load(image_name), rows, columns)
    
    frame_list = []
    for row in range(rows, 0, -1):
        end = row * columns
        start = end - (columns -1) -1
        for frame in frame_seq[start:end:1]:
            frame_list.append(AnimationFrame(frame, .1))
    
    #frame_list[(rows * columns) -1].duration = None        
    return Animation(frame_list)

'''
anim=load_animation('effects/_LPE__Healing_Circle_by_LexusX2.png', 5, 10)
sprite=pyglet.sprite.Sprite(anim)
sprite.position = (-sprite.width/2, - sprite.height/2)
actors.append(sprite)
'''
