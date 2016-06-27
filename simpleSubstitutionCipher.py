from cipherBase import cipherBase

class subsCipher(cipherBase):
    def __init__(self):
        super(subsCipher,self).__init__()
        self.elementLength=1 # one character encoded at a time
        

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

    def encrypt(self):
        cipherText = ""
        for char in self.plainText:
            if char in self.key.keys():
                char = self.key[char]
                pass
            cipherText+=char
        self.cipherText =  cipherText

    def decrypt(self):
        plainText = ""
        for char in self.cipherText:
            if char in self.reverseKey.keys():
                char = self.reverseKey[char]
                pass
            plainText+=char
        self.plainText = plainText



