import exifread
import os
import subprocess
import rawpy
from photo import Photo
from PIL import Image
from file_types import FILETYPES


def photo_objects():
    photos = []
    print(files)
    for file in files:
        opened = open(path + '/' + file, 'rb')
        tags = exifread.process_file(opened)
        pic = Photo(
            fileName=file,
            expo=tags['EXIF ExposureTime'],
            fNum=tags['EXIF FNumber'],
            iso=tags['EXIF ISOSpeedRatings'],
            diff=tags['MakerNote ExposureDifference']
            )
        photos.append(pic)


def sort_files(photos):
    """ Output valid photo files """
    return sorted(photos)


def is_image(pic):
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
    if 'new_photos' not in os.listdir('pictures'):  # Replace with path
        os.mkdir('{}/new_photos'.format('pictures'))  # Replace with path


def get_exif(path):
    tags = exifread.process_file(open(path, 'rb'))
    return tags


def make_photo(name, path):
    exif = get_exif(path)
    return Photo(name, exif)


def make_array_from_files(path, valid_files):
    photo_array = []
    for file in valid_files:
        photo = make_photo(file, '{}/{}'.format(path,file))
        photo_array.append(photo)
    return photo_array


def main():
    path = 'pictures'  # input('Enter directory: ')
    valid_files = get_files(path)
    array_of_photos = make_array_from_files(path, valid_files)


if __name__ == '__main__':
    main()

# new_photo = Photo()
# print(new_photo.expo)
# new_photo.set_new_expo(98)
# new_photo.update_expo()
# print(new_photo.expo)

# raw = rawpy.imread('pictures/nef.nef')
# rgb = raw.postprocess()
# raw.close()
# img = Image.fromarray(rgb) # Pillow image
# # img.show()
# img.save('rawpytests/nef_test.tiff')
