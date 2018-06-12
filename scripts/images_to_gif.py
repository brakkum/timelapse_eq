import imageio
import os

path = input('Input directory of files: ')
files = os.listdir(path)
images = []
for pic in files:
    if os.path.splitext(pic)[1] == '.jpeg':
        images.append(imageio.imread('{}/{}'.format(path, pic)))
imageio.mimsave('{}/gif.gif'.format(path), images, fps=3)