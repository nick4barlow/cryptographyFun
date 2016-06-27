import random
from cipherBase import cipherBase

class homCipher(cipherBase):
    def __init__(self):
        super(homCipher,self).__init__()
        self.elementLength=2 # one character encoded at a time
        

    def checkKeyType(self):
        if self.key == None:
            print "No key set!"
            return False
        if not isinstance(self.key,dict):
            print "Wrong type of key for this cipher - expect a dict"
            return False
        self.constructReverseKey()
        print "Key type is OK"
        return True

    def constructReverseKey(self):
        self.reverseKey={}
        for k,v in self.key.items():
            self.reverseKey[v] = k
            pass
        pass

    def divideMessageIntoBlocks(self,message,blockSize=2):
        newMessage = ""
        count = 0
        message=self.removeAllSpaces(message)
        for char in message:
            if count % blockSize == 0 and count > 0:
                newMessage+=" "
                pass
            newMessage+=char
            count+=1
            pass
        return newMessage

    def divideMessageIntoBigBlocks(self,message,blockSize=14):
        newMessage = ""
        count = 0
        for char in message:
            if count % blockSize == 0 and count > 0:
                newMessage+="   "
                pass
            newMessage+=char
            count+=1
            pass
        return newMessage
            

    def encrypt(self):
        cipherText = ""
        self.plainText=self.removeAllSpaces(self.plainText)
        encryptedChar=""
        for char in self.plainText:
            if char in self.key.keys():
                encryptedChar = self.key[char]
                pass
            elif char=="A" or char=="E" or char=="I" or char=="O" or char=="N" or char=="T":
                rnd = random.random()
                if rnd<0.5:
                    char+="0"
                    pass
                else:
                    char+="1"
                    pass
                encryptedChar = self.key[char]
                pass
 #           print "encrypting ",char," as ",encryptedChar," and adding to ciphertext"
            cipherText+=encryptedChar
        cipherText=self.divideMessageIntoBlocks(cipherText)
        cipherText=self.divideMessageIntoBigBlocks(cipherText)
        self.cipherText =  cipherText

    def decrypt(self):
        plainText = ""
        self.cipherText=self.removeAllSpaces(self.cipherText)
        thisChar=""
        for char in self.cipherText:
            thisChar+=char
            if thisChar.__len__() == self.elementLength:
                if thisChar in self.reverseKey.keys():
                    decryptedChar = self.reverseKey[thisChar]
                    plainText+=decryptedChar[0]
                    pass
                thisChar=""
                pass
            pass
        self.plainText = plainText



