from timelapse_eq.constants import RAW_FILETYPES
from PIL import Image
import rawpy
import os
import sys


path = sys.argv[1]
files = os.listdir(path)
if "jpegs" not in files:
    os.mkdir(f"{path}/jpegs")
for file in files:
    if os.path.splitext(file)[1].lower() in RAW_FILETYPES:
        if os.path.splitext(file)[1].lower() == ".nef":
            raw = rawpy.imread(f"{path}/{file}")
            rgb = raw.postprocess(use_auto_wb=True, no_auto_bright=True)
            raw.close()
            img = Image.fromarray(rgb)
        else:
            img = Image.open(f"{path}/{file}")
        if "small" in sys.argv:
            size = img.size
            size = tuple(int(s / 5) for s in size)
        else:
            size = img.size
        img = img.resize(size)
        img.save(f"{path}/jpegs/{file}.jpeg")
