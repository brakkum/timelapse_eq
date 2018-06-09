class Photo:

    def __init__(self, fileName, expo='', fNum=0, iso=0, diff=0):
        self.fileName = fileName
        self.expo = expo
        self.fNum = fNum
        self.iso = iso
        self.diff = diff

    def set_filename(self, fileName):
        self.fileName = fileName

    def set_expo(self, expo):
        self.expo = expo

    def set_fnum(self, fNum):
        self.fNum = fNum

    def set_iso(self, iso):
        self.iso = iso

    def set_diff(self, diff):
        self.diff = diff
