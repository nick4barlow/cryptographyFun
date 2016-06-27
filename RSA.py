import random
import math
import utils
from cipherBase import cipherBase

class RSA(cipherBase):
    def __init__(self):
        super(RSA,self).__init__()
        self.listOfPrimes = utils.findPrimes()
        self.plainTextBinary=""
        self.listOfBlocks=[]
        self.publicKey=None
        self.privateKey = None
        self.blockSize=0
        self.mode="ECB"

    def setCBC(self):
        print "Changing to Cipher Block Chaining mode"
        self.mode="CBC"


    def generateKeys(self):
        rnd1=int(random.random()*self.listOfPrimes.__len__())
        rnd2=int(random.random()*self.listOfPrimes.__len__())
        while rnd2 == rnd1:
            rnd2=int(random.random()*self.listOfPrimes.__len__())
            pass
        p = self.listOfPrimes[rnd1]
        q = self.listOfPrimes[rnd2]
        n=p*q
##  n is part of the public key - also determines block length
        self.blockSize = utils.getNumberOfBitsInInteger(n)
## compute totient of n 
        phi_n=(p-1)*(q-1)
## find a number that is co-prime to phi_n
        for prime in self.listOfPrimes[3:]:
            if prime >= n:
                break
            if utils.checkIsDivisor(prime,n):
                break

## find modular multiplicative inverse of e mod(phi_n)
            d = utils.findModMultInverse(prime,phi_n)
            if d != None:
                e=prime
                self.publicKey=(n,e)
                self.privateKey=(n,d)
                print "Public key: ",self.publicKey
                print "Private key: ",self.privateKey
                print "Block size", self.blockSize
                return True
            pass
        print "Couldn't generate keys"
        return False

    def convertPlainTextToBinary(self):
        self.plainTextBinary=utils.getBinaryStringFromString(self.plainText)

    def splitBinaryTextIntoBlocks(self,binaryText):
        listOfBlocks=[]
        thisBlock=""
        blockCount=0
        for i in range(binaryText.__len__()):
            if i % self.blockSize == 0:
                if blockCount>0:
                    listOfBlocks+=[thisBlock]
                    pass
                thisBlock=""
                blockCount+=1
            thisBlock+=binaryText[i]
            pass
        if thisBlock.__len__()>0:
            if thisBlock.__len__() < self.blockSize:
                for i in range(self.blockSize - thisBlock.__len__()):
                    thisBlock+="0"
                    pass
                pass
            listOfBlocks+=[thisBlock]
            pass
        return listOfBlocks
        
    def encryptBlock(self,messageBlock):
        thisInt = utils.getIntegerFromBinaryString(messageBlock)
        encryptedInt=pow(thisInt,self.publicKey[1]) % self.publicKey[0]
        binString = utils.getBinaryStringFromInteger(encryptedInt)
##  Need to deal with preceding 0s, to make correct length blocks.
        newBinString=""
        if binString.__len__() < self.blockSize:
            for i in range(self.blockSize - binString.__len__()):
                newBinString+="0"
        return newBinString+binString


    def decryptBlock(self,messageBlock):
        thisInt = utils.getIntegerFromBinaryString(messageBlock)
        print "Decrypting", messageBlock," which is", thisInt
        plainTextInt=pow(thisInt,self.privateKey[1]) % self.privateKey[0]
        binString = utils.getBinaryStringFromInteger(plainTextInt)
##  Need to deal with preceding 0s, to make correct length blocks.
        newBinString=""
        if binString.__len__() < self.blockSize:
            for i in range(self.blockSize - binString.__len__()):
                newBinString+="0"
        return newBinString+binString

    def xorBlock(self,block1,block2):
        if isinstance(block1,int):
##  convert to a binary string of the correct length
            blockString1=bin(block1)[2:]
            for i in range(self.blockSize - blockString1.__len__()):
                blockString1="0"+blockString1
                pass
            pass
        if isinstance(block2,int):
            blockString2=bin(block2)[2:]
            for i in range(self.blockSize - blockString2.__len__()):
                blockString2="0"+blockString2
                pass
            pass
        print "Will XOR ",blockString1,blockString2
        outputString=""
        for i in range(self.blockSize):
            if int(blockString1[i])+int(blockString2[i])==1:
                outputString+="1"
                pass
            else:
                outputString+="0"
                pass
            pass
        return outputString

    def encrypt(self):
        self.cipherText=""
        self.convertPlainTextToBinary()
        self.listOfBlocks = self.splitBinaryTextIntoBlocks(self.plainTextBinary)
        if self.mode == "CBC":
##  "block chain" - xor each block with the ciphertext of the previous block.
            previousBlock = self.encryptBlock(listOfBlocks[0])
            self.cipherText+=previousBlock
            for block in self.listOfBlocks[1:]:
                thisBlock=self.xorBlocks(previousBlock,block)
                thisEncryptedBlock = self.encryptBlock(thisBlock)
                self.cipherText+=thisEncryptedBlock
                previousBlock=thisEncryptedBlock
                pass
            pass
        else:
            for block in self.listOfBlocks:
                self.cipherText+=self.encryptBlock(block)
                pass
            pass
        


    def decrypt(self):
        plainText=""
        decryptedBinary=""
        listOfBlocks = self.splitBinaryTextIntoBlocks(self.cipherText)
        if self.mode=="CBC":
            previousCipherTextBlock =listOfBlocks[0]
            decryptedBinary+=self.decryptBlock(previousCipherTextBlock)
            for block in listOfBlocks[1:]:
                thisDecryptedBlock=self.decryptBlock(previousCipherTextBlock)
                decryptedBinary+=self.xorBlock(previousCipherTextBlock,thisDecryptedBlock)
                previousCipherTextBlock = block
                pass
            pass
            
        else:
            for block in listOfBlocks:
                decryptedBinary += self.decryptBlock(block)
                pass
            self.decryptedBinary=decryptedBinary
            pass
        decrypted=False
        trailingBitsToRemove=0
        while not decrypted:
            try:
                if trailingBitsToRemove==0:
                    plainText = utils.getStringFromBinaryString(decryptedBinary)
                    pass
                else:
                    plainText = utils.getStringFromBinaryString(decryptedBinary[:(-1*trailingBitsToRemove)])
                    pass
                decrypted=True
            except(LookupError):
                trailingBitsToRemove+=1
                pass
            pass
        self.plainText=plainText


