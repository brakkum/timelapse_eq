
class Photo:

    def __init__(self, name, exif):
        # name='', expo='', fNum=0, iso=0
        self.name = name
        self.str_shut = str(exif['EXIF ExposureTime'])
        self.shut = eval(self.str_shut)
        self.iso = int(str(exif['EXIF ISOSpeedRatings']))
        self.fNum = float(str(exif['EXIF FNumber']))
        self.stops = 0
        self.shift = 1

    def exp_shift(self, stops):
        self.shift = pow(2, stops) 

    def update_ev(self, stops):
        self.stops = stops
        self.exp_shift(self.stops)
