import struct
import numpy

def read_mnist_images(file):
  f = open(file)
  magic, num_imgs, num_rows, num_cols = struct.unpack('>iiii', f.read(4*4))
  assert magic == 2051, 'MNIST checksum failed'

  shape = (num_imgs, num_cols, num_rows)

  imgs = numpy.fromfile(file=f, dtype=numpy.uint8).reshape(shape)
  f.close()

  return imgs

def read_mnist_labels(file):
  f = open(file)
  magic = struct.unpack('>i', f.read(4))[0]
  assert magic == 2049, 'MNIST checksum failed'

  num_imgs = struct.unpack('>i', f.read(4))

  labels = numpy.fromfile(file=f, dtype=numpy.uint8)
  f.close()

  return labels

def read_mnist_dir(dirname):
  import os
  imgs_file = os.path.join(dirname, 'train-images.idx3-ubyte')
  labels_file = os.path.join(dirname, 'train-labels.idx1-ubyte')

  return (read_mnist_images(imgs_file), read_mnist_labels(labels_file))


def mnist_img_reader(fd, size, fname):
  # Disco function must be pure (ie no globals, ie no imports)
  if fd.tell() is 0:
    magic, num_imgs, num_rows, num_cols = struct.unpack('>iiii', fd.read(4*4))
    assert magic == 2051, 'MNIST checksum failed'

    shape = (num_imgs, num_cols, num_rows)

    pixels_per_img = num_cols*num_rows
    imgs_per_batch = size % pixels_per_img

    read_bytes = imgs_per_batch*pixels_per_img

  imgs = numpy.fromfile(file=fd, dtype=numpy.uint8, count=read_bytes).reshape(shape) 
  if imgs.alen > 0:
    yield imgs
