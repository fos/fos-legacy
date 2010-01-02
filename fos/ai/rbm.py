try:
    import mdp    
except ImportError:
    ImportError('Modular Data Processing Toolkit is not available')

from fos.io import read_mnist

dname='/home/eg309/Data/MNIST/'
imgs,labels=read_mnist.read_mnist_dir(dname)

print imgs.shape, labels.shape

img=imgs[0]

train_set=imgs[:100]
label_set=labels[:100]

#unsupervised learning
rbm=mdp.nodes.RBMNode(hidden_dim=25)

ts=train_set.reshape(100,28*28).astype('float32')

rbm.train(ts)
    
