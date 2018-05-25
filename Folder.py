import os
import time
import hashlib
import datetime

from File import File


class Folder:
    def __init__(self, path):
        self.foldername = os.path.split(path)[-1]
        self.path = path
        self.size = 0
        self.filenumber = 0
        self.foldernumber = 0
        self.fileSet = set()
        self.folderSet = set()
        self.dir = None
        self.contentsList = None
        self.tags = set()

        #coordinate
        self.x, self.y = (0, 0)


    def __str__(self):
        return self.foldername

    def getFolderContents(self):
        if self.contentsList:
            return self.contentsList

        contents = list()
        path = self.path
        for c in os.listdir(path):
            f = None
            cpath = '/'.join([path,c])
            if os.path.isdir(cpath):
                f = Folder(cpath)
                f.dir = self
                contents.append(f)
            elif os.path.isfile(cpath):
                f = File(cpath)
                f.dir = self
                contents.append(f)

        self.contentsList = contents
        return contents






    def bfs(self):
        self.filenumber = 0
        self.foldernumber = 0
        l = list()
        l.append(self)
        for c in l:
            if type(c) == Folder:
                l.extend(c.getFolderContents())
                self.folderSet.add(c)
            elif type(c) == File:
                self.size = self.size + c.getFileSize()
                self.fileSet.add(c)
        self.filenumber = len(self.fileSet)
        self.foldernumber = len(self.folderSet)
        return l

    def getFolderSize(self):
        return self.size

    def compare(self, f):
        if not self.fileSet:  #if fileSet is empty  then run  bfs
            self.bfs()
        if not f.fileSet:
            f.bfs()

        resultSet = self.fileSet & f.fileSet
        return resultSet


    def searchFiles(self, keyword):
        resultSet = set()
        for f in self.fileSet:
            if keyword in f.filename:
                resultSet.add(f)
        return resultSet

    def searchFolder(self, keyword):
        resultSet = set()
        for f in self.folderSet:
            if keyword in f.foldername:
                resultSet.add(f)
        return resultSet

    def getName(self):
        return self.foldername

    def getDetailInfo(self):
        return str(self)

    def setCoordinate(self, x, y):
        self.x, self.y = x, y

