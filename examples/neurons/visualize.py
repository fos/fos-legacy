import h5py
from fos import Actor, World, Window
from fos.actor.neuronregion import NeuronRegion

def visualize(pos, parents, offset, colors):
    
    wi = Window()
    w = wi.get_world()
    act = NeuronRegion(vertices = pos,
                       connectivity = parents,
                       offset = offset,
                       colors = colors,
                       force_centering = True)
    
    w.add(act)
    return act

f = h5py.File('neurons.hdf5', 'r')
pos = f['neurons/positions'].value
offset = f['neurons/offset'].value
parents = f['neurons/parents'].value
colors = f['neurons/colors'].value
f.close()

ac = visualize(pos, parents, offset, colors)