import os
import time
import hashlib
import datetime
from collections import deque
from PIL import Image
from PIL.ExifTags import TAGS
from moviepy.editor import VideoFileClip
from tinytag import TinyTag




class File:
    def __init__(self, path):
        self.path = path
        if not os.path.exists(path):
            print("it is not exist")
            return

        self.filename = os.path.split(self.path)[-1]
        self.extension = os.path.splitext(self.filename)[-1]
        self.extension = str(self.extension).lower().strip('.') #delete '.'
        self.filetype = self.getFileType()
        self.dir = None
        self.tags = set()
        #coordinate
        self.x, self.y = (0, 0)


    def __str__(self):
        return self.filename

    '''
    def getMD5(self):
        f = open(self.path,"rb")
        md5_obj = hashlib.md5()
        md5_obj.update(f.read())
        hash_code = md5_obj.hexdigest()
        f.close()
        md5 = str(hash_code).lower()
        return md5
    '''
    def getBigMD5(self):
        f = open(self.path,"rb")
        md5_obj = hashlib.md5()
        while True:
            d = f.read(8096)
            if not d:
                break
            md5_obj.update(d)
        hash_code = md5_obj.hexdigest()
        f.close()
        md5 = str(hash_code).lower()
        return md5

    def __eq__(self, other):

        #compare md5
        f = open(self.path,'rb')
        if self.getFileSize() != other.getFileSize():
            return False
        if self.getBigMD5() != other.getBigMD5():
            return False
        return True

    def __hash__(self):#make file hashable
        return hash(self.path)

    def getFileType(self):
        ext = self.extension
        if ext in ['bmp','jpg','jpeg','png','gif']:
            return 'picture'
        if ext in ['mp3','wma','wav','asf','aac','flac','ape','mid','ogg']:
            return 'music'
        if ext in ['flv','ogv','avi','mp4','mpg','mpeg','3gp','mkv','ts','webm','vob','wmv']:
            return 'video'
        if ext in ['mobi','epub','chm']:
            return 'book'
        if ext in ['txt','pdf','doc','docx','odf','xls','xlsv','xlsx']:
            return 'document'
        return 'other'


    def getDetailInfo(self):
        if self.getFileType() == 'picture':
            img = Image.open(self.path)
            info = img._getexif()
            exifinfo = {}
            if info:
                for tag, val in info.items():
                    decoded = TAGS.get(tag, tag)
                    exifinfo[decoded] = val
            return img.size, img.mode, exifinfo

        if self.getFileType() == 'music':
            tag = TinyTag.get(self.path)
            return tag

        if self.getFileType() == 'video':
            clip = VideoFileClip(self.path)
            return clip.duration

        return str(self)+" "+str(self.getFileSize())+"MB"


    def getFileSize(self):
        fsize = os.path.getsize(self.path)
        fsize = fsize/float(1024*1024) #MB
        return round(fsize,2)

    def timeStampToTime(self,timestamp):
        timeStruct = time.localtime(timestamp)
        return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)

    def getFileAccessTime(self):
        t = os.path.getatime(self.path)
        return self.timeStampToTime(t)

    def getFileCreateTime(self):
        t = os.path.getctime(self.path)
        return self.timeStampToTime(t)

    def getFileModifyTime(self):
        t = os.path.getmtime(self.path)
        return self.timeStampToTime(t)

    def getName(self):
        return self.filename

    def setCoordinate(self, x, y):
        self.x, self.y = x, y