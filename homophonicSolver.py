from homophonicCipher import homCipher
from exampleCipherTexts import homophonic_cipherText1
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
    list2=["A0","A1","B","C","D","E0","E1","F","G","H","I0","I1","J","K","L",
           "M","N0","N1","O0","O1","P","Q","R","S","T0","T1","U","V","W","X",
           "Y","Z"]
    list1=["00","01","02","03","04","05","06","07","08","09","10","11","12",
           "13","14","15","16","17","18","19","20","21","22","23","24","25",
           "26","27","28","29","30","31"]
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
    

sc = homCipher()
sc.setCipherText(homophonic_cipherText1)

countDict = sc.countElements(homophonic_cipherText1)
messageLength = sc.getMessageLengthWithoutSpaces(homophonic_cipherText1)

orderedList=sc.putElementsInOrder(countDict)

modifiedLetterFrequency={}
for k,v in utils.englishLetterFrequency.items():
    if k=="A" or k=="E" or k=="I" or k=="O" or k=="N" or k=="T":
        modifiedLetterFrequency[k+"0"] = v/2.0
        modifiedLetterFrequency[k+"1"] = v/2.0
        pass
    else:
        modifiedLetterFrequency[k] = v
        pass
    pass

englishOrder=sc.putElementsInOrder(modifiedLetterFrequency)


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
while numResets < 30:
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







