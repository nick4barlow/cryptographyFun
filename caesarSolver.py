from caesarCipher import caesarCipher

from exampleCipherTexts import caesar_cipherText1

counts={}

cs = caesarCipher()

bestKey=0
bestCount=0


for possibleKey in range(26):
    cs.resetPlainText()
    cs.resetCipherText()
    cs.setKey(possibleKey)
    cs.setCipherText(caesar_cipherText1)
    cs.decrypt()
    counts[possibleKey] = cs.countWords(cs.plainText)
    if counts[possibleKey] > bestCount:
        bestCount = counts[possibleKey]
        bestKey = possibleKey
        pass
    pass

cs.setKey(bestKey)
cs.decrypt()

print "Best decryption is \n \n",
print cs.plainText
