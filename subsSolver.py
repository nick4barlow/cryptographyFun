from simpleSubstitutionCipher import subsCipher
from exampleCipherTexts import simpleSubs_cipherText1
import random
import utils


quadDict={}
infile=open("english_quadgrams.txt")
for line in infile.readlines():
    quadDict[line.split()[0]] = int(line.split()[1])
    pass


def calculateQuadramScore(message):
    score = 0
    for index in range(message.__len__()-3):
        quad = message[index]+message[index+1]+message[index+2]+message[index+3]
        try:
            score+=quadDict[quad]
        except:
            pass
        pass
    return score


def generateRandomKey():
    list1=[]
    list2=[]
    for l in utils.alphabet:
        list1+=[l]
        list2+=[l]
        pass
    random.shuffle(list2)
    outputDict={}
    for i in range(list1.__len__()):
        outputDict[list1[i]] = list2[i]
        pass
    return outputDict


def swapRandomPair(inputDict):
    outputDict={}
    keys=inputDict.keys()
    for k in keys:
        outputDict[k] = inputDict[k]
        pass
    rnd1=int(random.random()*outputDict.__len__())
    rnd2=int(random.random()*outputDict.__len__())
    while rnd2 == rnd1:
        rnd2=int(random.random()*outputDict.__len__())
        pass
    tmpVal=outputDict[keys[rnd1]]
    outputDict[keys[rnd1]] = outputDict[keys[rnd2]]
    outputDict[keys[rnd2]] = tmpVal
    return outputDict
    

sc = subsCipher()
sc.setCipherText(simpleSubs_cipherText1)

countDict = sc.countElements(simpleSubs_cipherText1)
messageLength = sc.getMessageLengthWithoutSpaces(simpleSubs_cipherText1)

orderedList=sc.putElementsInOrder(countDict)
englishOrder=sc.putElementsInOrder(utils.englishLetterFrequency)


startingReverseKey={}
for i in range(orderedList.__len__()):
    startingReverseKey[orderedList[i]] = englishOrder[i]
    pass


sc.reverseKey=startingReverseKey
sc.decrypt()
wordCount = sc.countWords(sc.plainText)

quadCount = calculateQuadramScore(sc.plainText)

iterationsWithNoImprovement=0
rk = startingReverseKey
bestWordCount = 0
bestQuadCount = 0

bestKey={}
numResets=0
while numResets < 50:
    if iterationsWithNoImprovement%100 ==0:
        print "Iterations with no improvement", iterationsWithNoImprovement, numResets, quadCount, bestQuadCount
    newRK = swapRandomPair(rk)
    sc.reverseKey=newRK
    sc.decrypt()
    sc.plainText = sc.removeAllSpaces(sc.plainText)
    newQC = calculateQuadramScore(sc.plainText)
    if newQC > bestQuadCount:
        bestQuadCount = newQC
        bestKey = newRK
        pass
    if newQC > quadCount:
        rk = newRK
        quadCount = newQC
        iterationsWithNoImprovement=0
        pass
    else:
        iterationsWithNoImprovement+=1
    if iterationsWithNoImprovement == 2000:
        rk = generateRandomKey()
        sc.reverseKey=rk
        sc.decrypt()
        sc.plainText = sc.removeAllSpaces(sc.plainText)
        quadCount=calculateQuadramScore(sc.plainText)
        print "Starting with a new random key", quadCount
        iterationsWithNoImprovement=0
        numResets+=1


sc.reverseKey=bestKey
sc.decrypt()

print "Best effort at decrypting the message: \n \n"
print sc.plainText







