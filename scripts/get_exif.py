import exifread
import os
from file_types import FILETYPES

path = input("Input folder name: ") # folder name
if "exif_data" not in os.listdir(path):
    os.mkdir("{}/exif_data".format(path))
files = os.listdir(path)
num_files = len(files)
for file in files:
    if os.path.splitext(file)[1].lower() in FILETYPES:
        textfile = open("exif_data/{}.txt".format(file),"w")
        textfile.write("{}\n".format(file))
        opened = open(path + "/" + file, "rb")
        tags = exifread.process_file(opened)
        for key, val in tags.items():
            textfile.write("{key:{filler}<45}:{val}\n".format(key=key,filler="_",val=str(val)))
        textfile.close()