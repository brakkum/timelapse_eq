import exifread, os, rawpy
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
            fileName = file, 
            expo = tags['EXIF ExposureTime'],
            fNum = tags['EXIF FNumber'],
            iso = tags['EXIF ISOSpeedRatings'],
            diff = tags['MakerNote ExposureDifference']
            )
        photos.append(pic)

def valid_photos(fileArray):
    return list(filter(lambda pic: os.path.splitext(pic)[1].lower() in FILETYPES, fileArray))

def get_files(path):
    return os.listdir(path)

def get_path():
    return 'pictures' #input('Enter folder path: ')

def sort_files(photos):
    return sorted(photos)

def main():
    path = get_path()
    fileArray = get_files(path)
    photos = valid_photos(fileArray)
    sortedPhotos = sort_files(photos)
    print(sortedPhotos)

if __name__ == '__main__':
    main()

# raw = rawpy.imread('pictures/nef.nef')
# rgb = raw.postprocess()
# raw.close()
# img = Image.fromarray(rgb) # Pillow image
# # img.show()
# img.save('rawpytests/nef_test.tiff')