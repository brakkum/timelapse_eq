import os
from file_types import FILETYPES
from timelapse import Timelapse


class Dir:
    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.dir_contents = self.get_dir(self.dir_path)
        self.files = self.only_valid_files(self.dir_contents)
        self.move_on()

    def move_on(self):
        if self.files:
            self.timelapse = Timelapse(self)
            self.make_dir()
        else:
            print('No valid files.')

    def sort_files(self, photos):
        return sorted(photos)

    def is_image(self, pic):
        return os.path.splitext(pic)[1].lower() in FILETYPES

    def only_valid_files(self, files):
        def func(pic): return self.is_image(pic)
        return self.sort_files(list(filter(func, files)))

    def get_dir(self, dir_path):
        return os.listdir(dir_path)

    def make_dir(self):
        if 'new_photos' not in self.dir_contents:
            os.mkdir('{}/new_photos'.format(self.dir_path))
