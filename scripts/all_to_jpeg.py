import rawpy
import os
import sys
from PIL import Image
FILETYPES = ['.nef', '.tiff']

path = input('Input directory to convert: ')
files = os.listdir(path)
if 'jpegs' not in files:
    os.mkdir('{}/jpegs'.format(path))
for file in files:
    if os.path.splitext(file)[1].lower() in FILETYPES:
        if os.path.splitext(file)[1].lower() == '.nef':
            raw = rawpy.imread('{}/{}'.format(path, file))
            rgb = raw.postprocess(use_auto_wb=True, no_auto_bright=True)
            raw.close()
            img = Image.fromarray(rgb)  # Pillow image
        else:
            img = Image.open('{}/{}'.format(path, file))
        if 'small' in sys.argv:
            size = img.size
            size = tuple(int(s / 5) for s in size)
        else:
            size = img.size
        img = img.resize(size)
        img.save('{}/jpegs/{}.jpeg'.format(path, file))
