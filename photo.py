class Photo:

    def __init__(self, name, exif):
        # name='', expo='', fNum=0, iso=0
        self.name = name
        self.expo_length = exif['EXIF ExposureTime']
        self.fNum = exif['EXIF FNumber']
        self.iso = exif['EXIF ISOSpeedRatings']
        self.expo_val = 'calc here?'

    def update(self, update):
        self.expo_val = update