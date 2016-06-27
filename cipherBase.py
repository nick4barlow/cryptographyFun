from utils import *
import re
import enchant 

class cipherBase(object):
    def __init__(self):
        self.plainText=""
        self.cipherText=""

    def setKey(self,key):
        self.key= key
        self.checkKeyType()

    def setPlainText(self,text):
        self.plainText = text

    def setCipherText(self,text):
        self.cipherText = text

    def resetPlainText(self):
        self.plainText=""

    def resetCipherText(self):
        self.cipherText=""

    def returnPlainText(self):
        return self.plainText

    def returnCipherText(self):
        return self.cipherText

    def encrypt(self):
        return

    def decrypt(self):
        return

    def normalizeSpaces(self,message):
        newMessage=""
        for count in range(message.__len__()):
            if not message[count]==" ":
                newMessage+= message[count]
                pass
            if message[count]==" " and count>0 and message[count-1]!=" ":
                newMessage+=" "
                pass
            pass
        return newMessage


    def removeAllSpaces(self,message):
        newMessage=""
        whiteSpaceRegex=re.compile("[\s]+")
        for count in range(message.__len__()):
            if whiteSpaceRegex.match(message[count]) == None:
                newMessage+=message[count]
                pass
            pass
        return newMessage

    def divideMessageIntoBlocks(self,message,blockSize=2):
        newMessage = ""
        count = 0
        for char in message:
            if count % blockSize == 0 and count > 0:
                newMessage+=" "
                pass
            if char in alphabetToNumbersDict.keys():
                newMessage+=char
                count+=1
            pass
        return newMessage


    def countWords(self,message):
        d=enchant.Dict("en_UK")
        message = self.removeAllSpaces(message)
        count = 0
        for wordLength in range(3,6):
            for offset in range(0,wordLength):
                thisWord=""
                for charCount in range(message.__len__()-offset):
                    if (charCount) > 0 and (charCount) % wordLength == 0:
                        if d.check(thisWord):
                            count+= wordLength
                            pass
                        thisWord=""
                        pass
                    thisWord+=message[charCount+offset]
                    pass
                pass
            pass
        return count
                

    def getMessageLengthWithoutSpaces(self,message):
        message= self.removeAllSpaces(message)
        count=0
        return message.__len__() / self.elementLength
        
    def countElements(self,message):
        message = self.removeAllSpaces(message)
        countDict={}
        thisElement=""
        for charCount in range(message.__len__()):
            thisElement+=message[charCount]
            if thisElement.__len__() == self.elementLength:
                if not thisElement in countDict:
                    countDict[thisElement]=0
                    pass
                countDict[thisElement] += 1
                thisElement=""
                pass
            pass
        return countDict

    def putElementsInOrder(self,elementCountDict):
        outputList=[]
        counts=elementCountDict.values()
        counts.sort(reverse=True)
        for count in counts:
            for k,v in elementCountDict.items():
                if v==count and not k in outputList:
                    outputList+=[k]
                    pass
                pass
            pass
        return outputList
