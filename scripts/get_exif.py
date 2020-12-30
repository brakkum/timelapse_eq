from timelapse_eq.constants import RAW_FILETYPES
import exifread
import sys
import os

path = sys.argv[1]
if "exif_data" not in os.listdir(path):
    os.mkdir(f"{path}/exif_data")
files = os.listdir(path)
num_files = len(files)
for file in files:
    if os.path.splitext(file)[1].lower() in RAW_FILETYPES:
        text_file = open(f"{path}/exif_data/{file}.txt", "w")
        text_file.write(f"{file}\n")
        opened = open(f"{path}/{file}", "rb")
        tags = exifread.process_file(opened)
        for key, val in tags.items():
            text_file.write(f"{key:_<45}:{val}\n")
        text_file.close()
