import exifread, os, rawpy
from photo import Photo
from PIL import Image   


def get_photos():
    path = 'pictures' #input('Enter folder path: ')
    files = os.listdir(path)
    photos = []
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
    return photos

def compare_photos(originals):
    print(originals)

def main():
    originals = get_photos()
    compare_photos(originals)

# if __name__ == '__main__':
#     main()

raw = rawpy.imread('pictures/nef.nef')
rgb = raw.postprocess()
raw.close()
img = Image.fromarray(rgb) # Pillow image
# img.show()
img.save('rawpytests/nef_test.tiff')