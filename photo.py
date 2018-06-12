
class Photo:

    def __init__(self, name, exif):
        # name='', expo='', fNum=0, iso=0
        self.name = name
        self.str_shut = str(exif['EXIF ExposureTime'])
        self.shut = eval(self.str_shut)
        self.iso = int(str(exif['EXIF ISOSpeedRatings']))
        self.fNum = float(str(exif['EXIF FNumber']))
        self.stops = 1.0

    def update_ev(self, stops):
        self.stops = stops
