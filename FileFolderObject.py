import os
import shutil
from typing import Final

TARGET = "Hello"

INVALID_CHARACTER   = '\\/:*?"<>|'    #.
INVALID_REPLACEMENT = '\∕ː٭？＂＜＞｜․' #․

class ManagerTool:
    pass


class File:
    def __init__(self, name, location) -> None:
        """
            name
                file name
            location
                file location in directory
        """
        if location[-1] == "/":
            location = location[:-1]
        if os.path.isfile(location+"/"+name):
            self.name = name
            self.location = location
            self.stat = os.stat(self.path)
        else:
            raise Exception("Invalid location or file Name")



    def cekTextValid(txt):
        """
        Cek is string is valid as file name, not containing \\/:*?"<>|

            txt
                text that will be checked
        """
        for char in INVALID_CHARACTER:
            if char in txt:
                return False
        return True

    def validateText(txt, blankStr=False):
        """
        Validate file name by replacing invalid character \\/:*?"<>|

        txt 
            string that will validate
        blankStr
            replacement of invalid character
                <True> : using "_" as default
                <False>: replace character with INVALID_REPLACEMENT
                <str>  : using <str>
        """
        if isinstance(blankStr, str):
            for char in INVALID_CHARACTER:
                txt = txt.replace(char, blankStr)
        if isinstance is True:
            blankStr = "_"
            for char in INVALID_CHARACTER:
                txt = txt.replace(char, blankStr)
        else:
            for old, new in zip(INVALID_CHARACTER, INVALID_REPLACEMENT):
                txt = txt.replace(old, new)
        return txt


    @property
    def path(self):
        return self.location+"/"+self.name

    @property
    def format(self):
        idx = self.name.rfind(".")
        if idx == -1:
            return ""
        else:
            return self.name[idx:]

    @property
    def nameOnly(self):
        idx = self.name.rfind(".")
        if idx == -1:
            return self.name
        else:
            return self.name[:idx]


    def rename(self, name, format=True, replace=False, validateText=False, validateTextOption=False):
        """
        renaming the file
        
        name
            file new name
        format
            added file format to file name
        replace
            replace file when similar name exist
        validateText
            validate <name> if name is not valid
        validateTextOption
            option use for validateText function
                <True> : using "_" as default
                <False>: replace character with INVALID_REPLACEMENT
                <str>  : using <str>
        """
        old = self.path
        name = name.strip()
        name = name+self.format if format else name

        if name == "":
            raise Exception("name is Invalid")
        elif name == self.name:
            pass
        else:
            #except invalid name with modification
            isValid = False
            if File.cekTextValid(name) == False:
                if validateText:
                    name = File.validateText(name, validateTextOption)
                else:
                    raise Exception("invalid file name")

            #only except valid name
            new = self.location+"/"+name

            #replace the file or not
            if os.path.isfile(new):
                if replace:
                    os.remove(new)
                else:
                    raise Exception(f"file <{name}> is already exist")
            #renaming
            
            self.name = name
            os.rename(old, new)


    def move(self, destination, replace=False):
        """
        Moving File to new Location


            destination
                file destination in directory
            replace
                replace file on destination if there already exist
        """
        if os.path.exists(destination):
            old = self.path
            new = destination+"/"+self.name
            if os.path.exists(new):
                if replace:
                    os.remove(new)
                else:
                    raise Exception(f"file {new} allready exist")
            shutil.move(old, new)
            self.location = destination
        else:
            raise Exception("path is not found")



class Folder:
    def __init__(self, location, level=1) -> None:
        """
        
        location
            folder path
        """
        location = location.replace("\\","/")
        if location[-1] == "/":
            location = location[:-1]

        if os.path.isdir(location):

            self.location = location
            self.level = level

            #folder name
            idx = self.location.rfind("/")
            if idx == -1:
                self.name = self.location
            else:
                self.name = self.location[idx+1:]

            content = os.listdir(self.location)
            self.folder = {}
            self.file   = []
            for item in content:
                path = self.location+"/"+item
                if os.path.isfile(path):
                    self.file.append( File(item, self.location) )
                elif os.path.isdir(path):
                    self.folder[item] = Folder(path, self.level+1)
        else:
            raise Exception("Invalid location")

    def __getitem__(self, name):
        return self.folder[name]



    @property
    def numFile(self):
        n = len(self.file)
        for x in self.folder:
            n+=x.numFile
        return n

    @property
    def numFolder(self):
        n = len(self.folder)
        for x in self.folder:
            n+=x.numFolder
        return n



    def getAllFilePath(self):
        file = self.file
        final = []
        for x in file:
            final.append(x.path)
        for folder in self.folder:
            final.extend( self.folder[folder].getAllFilePath() )
        return final

    def getAllFile(self):
        file = self.file
        final = []
        for x in file:
            final.append(x.name)
        for folder in self.folder:
            final.extend( self.folder[folder].getAllFile() )
        return final

    def getAllFileObject(self):
        file = self.file
        final = []
        for x in file:
            final.append(x)
        for folder in self.folder:
            final.extend( self.folder[folder].getAllFileObject() )
        return final


    def show(self):
        """
        print out directory
        """
        print("   "*(self.level-1)+"> "+self.name)
        space = "   "*self.level

        for file in self.file:
            print(space+file.name)
        print()
        for name in self.folder:
            self.folder[name].show()

    def numberingFile(self, initial=1, numFormat=False, replace=False, separator=" ", atFront = False):
        number = initial
        numLength = len( str(len(self.file) ))
        for file in self.file:
            #number format
            strNum = str(number)
            if numFormat == "zero":
                strNum = strNum.rjust(numLength,"0")
            elif numFormat == "bracket":
                strNum = f"({strNum})"
            
            #replace file name or not
            if replace:
                fileName = replace
            else:
                fileName = file.nameOnly

            #Number Position
            if atFront:
                fileName = strNum + separator + fileName
            else:
                fileName =   fileName + separator + strNum

            file.rename(fileName)
            number+=1

    def cekTextValid(txt):
        """
        Cek is string is valid as file name, not containing \\/:*?"<>|

            txt
                text that will be checked
        """
        for char in INVALID_CHARACTER:
            if char in txt:
                return False
        return True
    
    def folderExtract(self, name, destination=False, filter=False, replace=False, fileName="number"):
        if self.destination == False:
            destination = self.location
        
        if not Folder.cekTextValid(name):
            raise Exception("Invalid folder name")
        if os.path.isdir(destination):
            raise Exception("invalid destination")
        path = destination+"/"+name
        if os.path.isdir(path):
            if replace:
                os.remove(path)
            else:
                raise Exception(f"Folder {path} is already exist")
        os.makedirs("")


"""with open("D:/EAT Project/FileObject/Hello/MyFile？？？.txt", "+w") as file:
    file.write("tong")

#file = File( "MyFile？？？.txt", "D:\EAT Project\FileObject\Hello")
dir = Folder( "D:\\EAT Project\\")
for x in dir.getAllFile():
    print(x)"""


