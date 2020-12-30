from timelapse_eq.file_types import FILETYPES
import os


class Directory:
    def __init__(self, directory):
        self.path = directory
        self.valid_photos = []
        self.output_path = directory + "/new_photos/"
        self.exists = os.path.isdir(self.path)

    def find_photos(self):
        def is_image(pic): return self.is_image(pic)
        valid_photos = [pic for pic in os.listdir(self.path) if is_image(pic)]
        self.valid_photos = [(self.path + "/" + pic) for pic in valid_photos]

    def sort_photos(self):
        self.valid_photos = sorted(self.valid_photos)

    def has_valid_photos(self):
        return len(self.valid_photos) > 0

    def make_output_dir(self):
        if not os.path.exists(self.output_path):
            os.mkdir("{0}/new_photos".format(self.path))

    @staticmethod
    def is_image(pic):
        return os.path.splitext(pic)[1].lower() in FILETYPES
