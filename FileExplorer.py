import time

from File import File
from Folder import Folder




def exeTime(func):
    def newFunc(*args, **argv):
        start = time.time()
        print(func.__name__,"start")
        back = func(*args, **argv)
        stop = time.time()
        print(func.__name__,"stop")
        print((stop-start)*1000,'ms')
        return back
    return newFunc()












class GuiFileExplorer:
    def __init__(self):
        self.mainfolder = None

        self.folderLeavesNumberDict = dict() #save number of leaves under a folder, in order to be displayed on gui

        #Gui
        self.k = 50 # coefficient
        self.folderX, self.folderY = 10, 500
        self.linesSet = set()
        return


    def setFolder(self, path):  #set main folder
        self.mainfolder = Folder(path)
        self.mainfolder.x, self.mainfolder.y = self.folderX, self.folderY
        self.mainfolder.bfs()
        self.mainfolder.setCoordinate(self.folderX, self.folderY)
        return


    def setFolderContentsCoordinate(self, folder):

        contentslist = folder.getFolderContents()
        length = len(contentslist)
        topfx = folder.x + 2*self.k #the position of the top folder or file
        #leave space for all nodes under one folder
        topfy = folder.y - self.k*(self.getLeavesNumber(folder))/2

        fx, fy = topfx, topfy
        #print(folder, self.getLeavesNumber(folder))
        #print(topfx,topfy)
        for f in contentslist: #to keep files and folders' space equal, move the file or folder before and after it sets coordinate
            if type(f) == Folder:
                fy = fy + self.k*(self.getLeavesNumber(f))/2
            elif type(f) == File:
                fy = fy + self.k/2
            f.setCoordinate(fx, fy)
            self.linesSet.add((folder.x, folder.y, fx, fy))
            if type(f) == File:
                fy = fy + self.k/2
            elif type(f) == Folder:
                if self.getLeavesNumber(f) == 0:
                    fy = fy + self.k
                    #fy = fy + self.k * (self.getLeavesNumber(f)) / 2
                else:
                    fy = fy + self.k*(self.getLeavesNumber(f))/2
        return

    def setAllFoldersContentsCoordinate(self):
        self.setFolderContentsCoordinate(self.mainfolder)
        l = list()
        l.append(self.mainfolder)
        for c in l:
            if type(c) == Folder:
                l.extend(c.getFolderContents())
                self.setFolderContentsCoordinate(c)
        return


    def getLeavesNumber(self, folder):
        if folder in self.folderLeavesNumberDict:
            return self.folderLeavesNumberDict[folder]
        cList = folder.getFolderContents()
        number = 0
        if cList:
            for c in cList:
                if type(c) == File:
                    number = number + 1
                elif type(c) == Folder:
                    number = number + self.getLeavesNumber(c)
        else:
            return 1
        self.folderLeavesNumberDict[folder] = number
        return number



#file0 = fileinfo('/Users/huweilun/Pictures/IMG_1065黑客技能书.JPG')
#print(file0.getDetailInfo())

#file1 = fileinfo('/Users/huweilun/Pictures/QQ20170904-0 第六章剧情.jpg')
#print(file1.getDetailInfo(),file1.getFileSize())

#filem = file('/Users/huweilun/files/oped/小幸运.flac')

#print(filem.getDetailInfo())
#print(filem.getBigMD5())

'''
f1 = folder("/Users/huweilun/files/dictionary")
print(f1.bfs())
f2 = folder("/Users/huweilun/files/dictionary/牛津8")
print(f2.bfs())
print(f1.compare(f2))

print([str(x) for x in f1.compare(f2)])
'''