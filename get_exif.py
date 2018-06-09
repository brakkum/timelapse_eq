import exifread, os

FILETYPES = ['.jpg','.jpeg','.nef','.tiff']
i = 1

path = input('Input folder name: ') # folder name
files = os.listdir(path)
for file in files:
    if os.path.splitext(file)[1].lower() in FILETYPES:
        textfile = open('pic{}.txt'.format(i),'w')
        textfile.write('{}\n'.format(file))
        opened = open(path + '/' + file, 'rb')
        tags = exifread.process_file(opened)
        for key, val in tags.items():
            textfile.write('{key:{filler}<45}:{val}\n'.format(key=key,filler='_',val=str(val)))
        textfile.close()
        i += 1