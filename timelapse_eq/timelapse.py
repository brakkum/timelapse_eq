from timelapse_eq.utilities import colorize, PrintColors
from timelapse_eq.photo import Photo
from functools import partial
import concurrent.futures
import math


class TimeLapse:
    def __init__(self, photos):
        self.file_paths = photos
        self.photos = []
        self.change_points = []
        self.necessary_exposure_changes = []

    def make_photos(self):
        print(colorize("Reading Photos..", PrintColors.YELLOW))
        self.photos = [Photo(path) for path in self.file_paths]
        print(colorize("Photos Read", PrintColors.GREEN))

    def determine_exposure_change_points(self, change_start):
        change_points = [{"index": 0}]
        photos = iter(self.photos)
        current_photo = next(photos)
        next_photo = next(photos)

        while next_photo is not None:
            if current_photo.shut != next_photo.shut:
                change_points.append({
                    "index": self.photos.index(next_photo),
                    "change": "shut"
                })
            elif current_photo.iso != next_photo.iso:
                change_points.append({
                    "index": self.photos.index(next_photo),
                    "change": "iso"
                })
            elif current_photo.fNum != next_photo.fNum:
                change_points.append({
                    "index": self.photos.index(next_photo),
                    "change": "fNum"
                })
            current_photo = next_photo
            try:
                next_photo = next(photos)
            except StopIteration:
                next_photo = None
                continue

        if change_start:
            change_points = self.change_start(change_points)
        self.change_points = change_points

    def change_start(self, change_points):
        for i in range(change_points[1]["index"]):
            print("{0}: {1}".format(i + 1, self.photos[i].name))
        selection = -1
        while selection < 1 or selection > change_points[1]["index"]:
            try:
                selection = int(input("Enter number of new start point: "))
            except ValueError:
                print("Integers only, please.")
        change_points[0]["index"] = selection - 1
        return change_points

    def determine_necessary_exposure_changes(self):
        necessary_exposure_changes = [0] * len(self.photos)

        change_points = iter(self.change_points)
        current_change_point = next(change_points)
        next_change_point = next(change_points)

        while next_change_point is not None:
            current_change_index = current_change_point["index"]
            next_change_index = next_change_point["index"]
            method_of_change = next_change_point["change"]
            start_val = self.get_method_changed_value(current_change_index, method_of_change)
            end_val = self.get_method_changed_value(next_change_index, method_of_change)
            ev_change = self.get_exposure_change(start_val, end_val)
            num_of_photos_in_change = next_change_index - current_change_index
            increments = self.get_increments_for_change(ev_change, num_of_photos_in_change)

            k = 0
            for j in range(current_change_index, next_change_index):
                necessary_exposure_changes[j] = round((increments * k), 3)
                k += 1

            current_change_point = next_change_point
            try:
                next_change_point = next(change_points)
            except StopIteration:
                next_change_point = None
        self.necessary_exposure_changes = necessary_exposure_changes

    def get_method_changed_value(self, i, val):
        if val == "shut":
            return self.photos[i].shut
        elif val == "iso":
            return self.photos[i].iso
        elif val == "fNum":
            return self.photos[i].fNum
        else:
            return

    def update_photos(self):
        for i, change in enumerate(self.necessary_exposure_changes):
            self.photos[i].update_exposure_change_needed(change)

    @staticmethod
    def get_increments_for_change(ev_change, steps):
        return ev_change / steps

    @staticmethod
    def get_exposure_change(start, stop):
        return -(math.log2(start) - math.log2(stop))

    def save_timelapse_photos(self, args):
        print(colorize("Saving TIFF Photos..", PrintColors.YELLOW))
        with concurrent.futures.ProcessPoolExecutor() as executor:
            save_photo_func_with_args = partial(self.save_timelapse_photo, args=args)
            zip(self.photos, executor.map(save_photo_func_with_args, self.photos))
        print(colorize("TIFF Photos Saved", PrintColors.GREEN))

    @staticmethod
    def save_timelapse_photo(photo, args):
        photo.save(args)
