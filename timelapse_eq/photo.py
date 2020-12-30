from timelapse_eq.constants import OUTPUT_DIR
from PIL import Image
import exifread
import rawpy
import os


class Photo:
    def __init__(self, photo_path):
        self.photo_path = photo_path
        self.directory = os.path.split(photo_path)[0]
        self.name = os.path.basename(photo_path)
        self.shut = None
        self.iso = None
        self.fNum = None
        self.get_exif_data()
        self.shift = 1.0

    def get_exif_data(self):
        file = open(self.photo_path, "rb")
        exif = exifread.process_file(file)
        file.close()
        self.shut = eval(str(exif["EXIF ExposureTime"]))
        self.iso = int(str(exif["EXIF ISOSpeedRatings"]))
        self.fNum = float(str(exif["EXIF FNumber"]))

    def save(self, args):
        file = open(self.photo_path, "rb")
        raw = rawpy.imread(file)
        file.close()

        rgb = raw.postprocess(
            exp_shift=self.shift,
            use_auto_wb=args.auto_wb,
            no_auto_bright=True
        )
        raw.close()
        img = Image.fromarray(rgb)
        if args.width is not None:
            img_size = img.size
            image_ratio = img_size[1] / img_size[0]
            height = float(args.width) * float(image_ratio)
            size_tup = (int(args.width), int(height))
            img = img.resize(size_tup)
        img.save(f"{self.directory}/{OUTPUT_DIR}/{self.name}.tiff")

    def update_exposure_change_needed(self, stops):
        self.shift = pow(2, stops)
