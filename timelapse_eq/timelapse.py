from timelapse_eq.photo import Photo
from PIL import Image
import math
import exifread
import rawpy
import os


class Timelapse:
    def __init__(self, directory):
        self.args = directory.args
        self.path = directory.dir_path
        self.files = directory.files
        self.photos = self.make_photos()
        self.change_points = self.find_changes()
        self.ev_changes = self.make_ev_array()
        self.update_photo_objects()
        self.save_photos()

    def save_photos(self):
        for photo in self.photos:
            raw = rawpy.imread(photo.data)
            rgb = raw.postprocess(
                exp_shift=photo.shift,
                use_auto_wb=self.args.auto_wb,
                no_auto_bright=True)
            raw.close()
            img = Image.fromarray(rgb)  # Pillow image
            # change width if arg
            if self.args.width:
                img_size = img.size
                image_ratio = img_size[1] / img_size[0]
                height = float(self.args.width) * float(image_ratio)
                new_tup = (int(self.args.width), int(height))
                size = new_tup
                img = img.resize(size)
            print('Saving {}/new_photos/{}.tiff'.format(photo.path, photo.name),
                end="\r",
                flush=True)
            img.save('{}/new_photos/{}.tiff'.format(photo.path, photo.name))
        print('Photos saved.')

    def update_photo_objects(self):
        for i in range(len(self.ev_changes)):
            self.photos[i].update_ev(self.ev_changes[i])

    def get_val(self, i, val):
        if val == 'shut':
            return self.photos[i].shut
        elif val == 'iso':
            return self.photos[i].iso
        elif val == 'fNum':
            return self.photos[i].fNum
        else:
            return

    def get_increments(self, ev_change, steps):
        return ev_change / steps

    def get_ev_change(self, start, stop):
        return -(math.log2(start) - math.log2(stop))

    def make_ev_array(self):
        change_array = [1] * len(self.photos)
        # TODO Refactor all this junk
        for i in range(len(self.change_points) - 1):
            start_index = self.change_points[i]['index']
            next_start = self.change_points[i + 1]['index']
            being_changed = self.change_points[i + 1]['change']
            start_val = self.get_val(start_index, being_changed)
            end_val = self.get_val(next_start, being_changed)
            ev_change = self.get_ev_change(start_val, end_val)
            diff = next_start - start_index
            increments = self.get_increments(ev_change, diff)
            k = 0
            for j in range(start_index, next_start):
                change_array[j] = round((increments * k), 3) + 1
                k += 1
        print('change_array',change_array)
        return change_array

    def change_start(self, diff_array):
        for i in range(diff_array[1]['index']):
            print('{}: {}/{}'.format(i + 1,self.path,self.photos[i].name))
        selection = -1
        while selection < 1 or selection > diff_array[1]['index']:
            try:
                selection = int(input('Enter number to select new start point: '))
            except ValueError:
                print('Integers only, please.')
        diff_array[0]['index'] = selection - 1
        print(diff_array)
        return diff_array

    def find_changes(self):
        diff_array = [{'index': 0}]
        for i in range(0, len(self.photos)):
            if i != len(self.photos) - 1:
                current = self.photos[i]
                _next = self.photos[i + 1]
                if current.shut != _next.shut:
                    change = self.photos[i + 1].shut
                    diff_array.append({
                        'index': i + 1,
                        'change': 'shut'})
                elif current.iso != _next.iso:
                    change = self.photos[i + 1].iso
                    diff_array.append({
                        'index': i + 1,
                        'change': 'iso'})
                elif current.fNum != _next.fNum:
                    change = self.photos[i + 1].fNum
                    diff_array.append({
                        'index': i + 1,
                        'change': 'fNum'})
        if self.args.start:
            diff_array = self.change_start(diff_array)
        return diff_array

    def get_exif(self, photo):
        tags = exifread.process_file(open(photo, 'rb'))
        return tags

    def make_photo(self, photo):
        data = open('{}/{}'.format(self.path, photo), 'rb')
        exif = self.get_exif('{}/{}'.format(self.path, photo))
        return Photo(data, exif, photo, self.path)

    def make_photos(self):
        photos = []
        for photo in self.files:
            photos.append(self.make_photo(photo))
        return photos
