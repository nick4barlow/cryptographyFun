from cipherBase import *
from utils import *

def constructVigenereSquare():
    rowDict={}
    for i in range(26):
        thisRow=""
        for j in range(26):
            thisRow+=numbersToAlphabetDict[(i+j)% 26 + 1]
            pass
        rowDict[numbersToAlphabetDict[i+1].lower()] = thisRow
    return rowDict

class vigenereCipher(cipherBase):
    def __init__(self):
        self.square = constructVigenereSquare()

    def encryptLetter(self,letter,keyLetter):
        rowToUse = self.square[keyLetter.lower()]
        columnToUse = self.square["a"].find(letter)
        return rowToUse[columnToUse]

    
    def decryptLetter(self,letter, keyLetter):
        rowToUse = self.square[keyLetter.lower()]
        columnToUse = rowToUse.find(letter)
        return self.square["a"][columnToUse]


    def encrypt(self):
        self.cipherText=""
        self.plainText = self.removeAllSpaces(self.plainText)
        for charCount in range(self.plainText.__len__()):
            keyCount = charCount % (self.key.__len__())
            keyLetter = self.key[keyCount]
            self.cipherText+=self.encryptLetter(self.plainText[charCount],keyLetter)
            pass
        self.cipherText = self.divideMessageIntoBlocks(self.cipherText,5)


    def decrypt(self):
        self.plainText=""
        self.cipherText=self.removeAllSpaces(self.cipherText)
        for charCount in range(self.cipherText.__len__()):
            keyCount = charCount % (self.key.__len__())
            keyLetter = self.key[keyCount]
            self.plainText+=self.decryptLetter(self.cipherText[charCount],keyLetter)
            pass
        
