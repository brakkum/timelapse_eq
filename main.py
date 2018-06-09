import exifread
import os
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
    print(sorted(photos))


def validate_photos(file_array):
    """ Send validated files to get sorted """
    def func(pic): return os.path.splitext(pic)[1].lower() in FILETYPES
    sort_files(list(filter(func, file_array)))


def get_files(path):
    """ Send files from directory to validation """
    validate_photos(os.listdir(path))


def get_path():
    """ Send directory with files to get_files """
    get_files('pictures')  # switch for input('Enter folder path: ')


def main():
    get_path()
    # path = get_path()
    # file_array = get_files(path)
    # photos = validate_photos(file_array)
    # sorted_photos = sort_files(photos)
    # print(sorted_photos)

if __name__ == '__main__':
    main()

# raw = rawpy.imread('pictures/nef.nef')
# rgb = raw.postprocess()
# raw.close()
# img = Image.fromarray(rgb) # Pillow image
# # img.show()
# img.save('rawpytests/nef_test.tiff')
