import os
from file_types import FILETYPES
from timelapse import Timelapse


class Dir:
    def __init__(self, dir_path, args):
        try:
            self.dir_path = dir_path
            self.args = args
            self.dir_contents = self.get_dir(self.dir_path)
            self.files = self.only_valid_files(self.dir_contents)
            self.move_on()
        except FileNotFoundError:
            print('No such directory')

    def move_on(self):
        if self.files:
            self.make_dir()
            self.timelapse = Timelapse(self)
        else:
            print('No valid files.')

    def sort_files(self, photos):
        return sorted(photos)

    def is_image(self, pic):
        return os.path.splitext(pic)[1].lower() in FILETYPES

    def only_valid_files(self, files):
        def is_image(pic): return self.is_image(pic)
        return self.sort_files(list(filter(is_image, files)))

    def get_dir(self, dir_path):
        return os.listdir(dir_path)

    def make_dir(self):
        if 'new_photos' not in self.dir_contents:
            os.mkdir('{}/new_photos'.format(self.dir_path))
