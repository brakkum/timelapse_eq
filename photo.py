class Photo:

    def __init__(self, name, exif):
        # name='', expo='', fNum=0, iso=0
        self.name = name
        self.expo_length = exif['EXIF ExposureTime']
        self.fNum = exif['EXIF FNumber']
        self.iso = exif['EXIF ISOSpeedRatings']

    # self.expo_diff = exif['MakerNote ExposureDifference']
    # self.new_expo = self.expo_diff

    # def set_new_expo(self, new_expo):
    #     self.new_expo = new_expo

    # def update_expo(self):
    #     if self.expo_diff != self.new_expo:
    #         self.expo_diff = self.new_expo

    # def set_filename(self, fileName):
    #     self.fileName = fileName

    # def set_expo(self, expo):
    #     self.expo = expo

    # def set_fnum(self, fNum):
    #     self.fNum = fNum

    # def set_iso(self, iso):
    #     self.iso = iso

    # def set_diff(self, diff):
    #     self.diff = diff
