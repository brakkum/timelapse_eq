from timelapse_eq.constants import RAW_FILETYPES, OUTPUT_DIR
import os


class Directory:
    def __init__(self, directory):
        self.path = directory
        self.valid_photos = []
        self.output_path = f"{directory}/{OUTPUT_DIR}/"
        self.exists = os.path.isdir(self.path)

    def find_photos(self):
        def is_image(pic): return os.path.splitext(pic)[1].lower() in RAW_FILETYPES
        valid_photos = [pic for pic in os.listdir(self.path) if is_image(pic)]
        self.valid_photos = [f"{self.path}/{pic}" for pic in valid_photos]

    def sort_photos(self):
        self.valid_photos = sorted(self.valid_photos)

    def has_valid_photos(self):
        return len(self.valid_photos) > 0

    def make_output_dir(self):
        if not os.path.exists(self.output_path):
            os.mkdir(f"{self.path}/{OUTPUT_DIR}")
