import exifread
import os
import subprocess
import rawpy
import math
from photo import Photo
from PIL import Image
from file_types import FILETYPES


def sort_files(photos):
    """ Output valid photo files """
    return sorted(photos)


def is_image(pic):
    """ Is it a vlid filetype? """
    return os.path.splitext(pic)[1].lower() in FILETYPES


def validate_photos(file_array):
    """ Send validated files to get sorted """
    def func(pic): return is_image(pic)
    return sort_files(list(filter(func, file_array)))


def get_files(path):
    """ Send filenames from directory to validation """
    return validate_photos(os.listdir(path))


def make_new_folder(path):
    """ Make new folder to hold new photos """
    if 'new_photos' not in os.listdir(path):
        os.mkdir('{}/new_photos'.format(path))


def get_exif(path):
    tags = exifread.process_file(open(path, 'rb'))
    return tags


def make_photo(name, path):
    data = open('{}/{}'.format(path, name), 'rb')
    exif = get_exif('{}/{}'.format(path, name))
    return Photo(data, exif, name, path)


def make_array_from_files(path, valid_files):
    photo_array = []
    for file in valid_files:
        photo_array.append(make_photo(file, path))
    return photo_array


def find_change_points(photos):
    diff_array = [{'index': 0}]
    for i in range(0, len(photos)):
        if i != len(photos) - 1:
            if photos[i].shut != photos[i + 1].shut:
                change = photos[i + 1].shut
                diff_array.append({
                    'index': i + 1,
                    'change': 'shut'})
            elif photos[i].iso != photos[i + 1].iso:
                change = photos[i + 1].iso
                diff_array.append({
                    'index': i + 1,
                    'change': 'iso'})
            elif photos[i].fNum != photos[i + 1].fNum:
                change = photos[i + 1].fNum
                diff_array.append({
                    'index': i + 1,
                    'change': 'fNum'})
    return diff_array


def get_val(photo_array, i, val):
    if val == 'shut':
        return photo_array[i].shut
    elif val == 'iso':
        return photo_array[i].iso
    elif val == 'fNum':
        return photo_array[i].fNum
    else:
        return


def get_ev_change(start, stop):
    return -(math.log2(start) - math.log2(stop))


def get_increments(ev_change, steps):
    return ev_change / steps


def make_ev_change_array(diff_array, photo_array):
    change_array = []
    # TODO Refactor all this junk
    # TODO add ev changes for images after final change?
    for i in range(len(diff_array) - 1):
        start_index = diff_array[i]['index']
        next_start = diff_array[i + 1]['index']
        being_changed = diff_array[i + 1]['change']

        start_val = get_val(photo_array, start_index, being_changed)
        end_val = get_val(photo_array, next_start, being_changed)

        ev_change = get_ev_change(start_val, end_val)
        increments = get_increments(ev_change, next_start - start_index)

        for j in range(0, next_start - start_index):
            change_array.append(round((increments * j), 3))

    return change_array


def update_photo_objects(photos, ev_changes):
    for i in range(len(ev_changes)):
        photos[i].update_ev(ev_changes[i])
    return photos


def save_photos(photos):
    for photo in photos:
        raw = rawpy.imread(photo.data)
        # TODO auto white balance option
        rgb = raw.postprocess(
            exp_shift=photo.shift,
            use_auto_wb=True,
            no_auto_bright=True)
        raw.close()
        img = Image.fromarray(rgb)  # Pillow image
        img.save('{}/new_photos/{}.tiff'.format(photo.path, photo.name))


def main():
    # get folder with images
    path = input('Enter directory: ')
    # get filenames of valid file type
    valid_files = get_files(path)

    if valid_files:
        # get array of photo objects
        array_of_photos = make_array_from_files(path, valid_files)
        # make new directory for new photos
        make_new_folder(path)
        # find the indices where exposure changes
        diff_array = find_change_points(array_of_photos)
        # create array with ev change that will be needed for each photo
        ev_change_array = make_ev_change_array(diff_array, array_of_photos)
        # apply changes to Photo objects
        photos_with_ev = update_photo_objects(array_of_photos, ev_change_array)
        # pass photo array to photo maker
        save_photos(photos_with_ev)

    else:
        print('no valid files')


if __name__ == '__main__':
    main()
