import imageio
import sys
import os

path = sys.argv[1]
files = os.listdir(path)
images = []
for pic in sorted(files):
    if os.path.splitext(pic)[1] == ".jpeg":
        images.append(imageio.imread(f"{path}/{pic}"))
imageio.mimsave(f"{path}/timelapse.gif", images, fps=12)
