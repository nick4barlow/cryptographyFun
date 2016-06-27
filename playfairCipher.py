#!/usr/bin/env python

from utils import alphabetToNumbersDict

from cipherBase import cipherBase

class playfairCipher(cipherBase):
    def __init__(self):
        self.plainText=""
        self.cipherText=""
        pass


    def checkEvenNumber(self):
        count = 0
        for char in self.plainText:
            if char in alphabetToNumbersDict.keys():
                count+=1
                pass
            pass
        if count%2==1:
            self.plainText+="Z"
            pass
        pass

    def checkForEqualPairs(self):
        gotToTheEndWithoutChanges=False
        while gotToTheEndWithoutChanges == False:
            self.plainText = self.divideMessageIntoBlocks(self.plainText,2)
            self.plainText = self.normalizeSpaces(self.plainText)
            newPlainText=""
            firstChar=""
            secondChar=""
            modifiedSomething=False
            for count in range(self.plainText.__len__()):
                if count % 3 == 0:
                    firstChar=self.plainText[count]
                    newPlainText+=firstChar
                    pass
                if count % 3 ==1:
                    secondChar = self.plainText[count]
                    if secondChar == firstChar and modifiedSomething==False:
                        newPlainText+= "Z" + secondChar
                        modifiedSomething = True
                    else:
                        newPlainText += secondChar
                if count% 3 == 2: 
                    newPlainText += self.plainText[count]
                    pass
                pass
            self.plainText = newPlainText
            if not modifiedSomething:
                gotToTheEndWithoutChanges=True
                pass
            pass
        pass

    def replaceJwithI(self):
        newPlainText = ""
        for char in self.plainText:
            if char == "J":
                newPlainText+="I"
                pass
            else:
                newPlainText+=char
                pass
            pass
        self.plainText = newPlainText


    def encryptPair(self,pair):
        newPair=""
        rowCount=0
        for keyRow in self.key:
            if pair[0] in keyRow and pair[1] in keyRow:
                newPair += keyRow[(keyRow.find(pair[0])+1) % 5]
                newPair += keyRow[(keyRow.find(pair[1])+1) % 5]
                return newPair
            if pair[0] in keyRow and not pair[1] in keyRow:
                firstColumn = keyRow.find(pair[0])
                firstRow=rowCount
                otherRowCount=0
                for otherKeyRow in self.key:
                    if pair[1] in otherKeyRow:
                        secondColumn = otherKeyRow.find(pair[1])
                        secondRow = otherRowCount
                        pass
                    otherRowCount+=1
            rowCount+=1
        if firstColumn == secondColumn:
            newFirstLetter = self.key[(firstRow+1)%5][firstColumn]
            newSecondLetter = self.key[(secondRow+1)%5][secondColumn]
            return newFirstLetter+newSecondLetter
        else: 
            newFirstLetter = self.key[firstRow][secondColumn]
            newSecondLetter = self.key[secondRow][firstColumn]
            return newFirstLetter+newSecondLetter

    def decryptPair(self,pair):
        newPair=""
        rowCount=0
        for keyRow in self.key:
            if pair[0] in keyRow and pair[1] in keyRow:
                newPair += keyRow[(keyRow.find(pair[0])-1) % 5]
                newPair += keyRow[(keyRow.find(pair[1])-1) % 5]
                return newPair
            if pair[0] in keyRow and not pair[1] in keyRow:
                firstColumn = keyRow.find(pair[0])
                firstRow=rowCount
                otherRowCount=0
                for otherKeyRow in self.key:
                    if pair[1] in otherKeyRow:
                        secondColumn = otherKeyRow.find(pair[1])
                        secondRow = otherRowCount
                        pass
                    otherRowCount+=1
            rowCount+=1
        if firstColumn == secondColumn:
            newFirstLetter = self.key[(firstRow-1)%5][firstColumn]
            newSecondLetter = self.key[(secondRow-1)%5][secondColumn]
            return newFirstLetter+newSecondLetter
        else: 
            newFirstLetter = self.key[firstRow][secondColumn]
            newSecondLetter = self.key[secondRow][firstColumn]
            return newFirstLetter+newSecondLetter

    def removeZs(self):
        newPlainText=""
        previousLetter=""
        nextLetter=""
        modifiedSomething=False
        for charCount in range(self.plainText.__len__()):
            skipThisLetter=False
            if self.plainText[charCount]=="Z":
                if charCount%3 == 0 and charCount>2:
                    previousLetter = self.plainText[charCount-2]
                    if charCount < self.plainText.__len__():
                        nextLetter = self.plainText[charCount+1]
                        if previousLetter == nextLetter:
                            skipThisLetter=True
                            pass
                        pass
                if charCount%3==1 and charCount < self.plainText.__len__()-2:
                    previousLetter = self.plainText[charCount-1]
                    nextLetter = self.plainText[charCount+2]
                    if previousLetter == nextLetter:
                        skipThisLetter=True
                        modifiedSomething=True
                        pass
                if charCount == self.plainText.__len__()-1:
                    skipThisLetter=True
                    modifiedSomething=True
                    pass
                pass
            if not skipThisLetter:
                newPlainText+=self.plainText[charCount]
                pass
            pass
        self.plainText=newPlainText
        self.plainText = self.divideMessageIntoBlocks(self.plainText,2)
        self.plainText = self.normalizeSpaces(self.plainText)


    def encrypt(self):
        self.replaceJwithI()
        self.checkForEqualPairs()
        self.checkEvenNumber()
        pair=""
        for charCount in range(self.plainText.__len__()):
            if charCount%3 ==0:
                pair+=self.plainText[charCount]
            elif charCount%3==1:
                pair+=self.plainText[charCount]
                self.cipherText+=self.encryptPair(pair)
            elif charCount%3 ==2:
                self.cipherText+=" "
                pair=""
                pass
            pass
        pass

    def decrypt(self):
        self.cipherText = self.divideMessageIntoBlocks(self.cipherText,2)
        self.cipherText = self.normalizeSpaces(self.cipherText)
        pair=""
        for charCount in range(self.cipherText.__len__()):
            if charCount%3 ==0:
                pair+=self.cipherText[charCount]
            elif charCount%3==1:
                pair+=self.cipherText[charCount]
                self.plainText+=self.decryptPair(pair)
            elif charCount%3 ==2:
                self.plainText+=" "
                pair=""
                pass
            pass
        self.removeZs()
        pass


