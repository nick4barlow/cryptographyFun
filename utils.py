#!/usr/bin/env python

import numpy
import pylab
import math
from matplotlib import pyplot
from matplotlib.ticker import FormatStrFormatter
import binascii

numbersToAlphabetDict={ 0: "A",
                        1: "B",
                        2: "C",
                        3: "D",
                        4: "E",
                        5: "F",
                        6: "G",
                        7: "H",
                        8: "I",
                        9: "J",
                        10: "K",
                        11: "L",
                        12: "M",
                        13: "N",
                        14: "O",
                        15: "P",
                        16: "Q",
                        17: "R",
                        18: "S",
                        19: "T",
                        20: "U",
                        21: "V",
                        22: "W",
                        23: "X",
                        24: "Y",
                        25: "Z"
                    }

alphabetToNumbersDict={"A": 0,
                       "B": 1,
                       "C": 2,
                       "D": 3,
                       "E": 4,
                       "F": 5,
                       "G": 6,
                       "H": 7,
                       "I": 8,
                       "J": 9,
                       "K": 10,
                       "L": 11,
                       "M": 12,
                       "N": 13,
                       "O": 14,
                       "P": 15,
                       "Q": 16,
                       "R": 17,
                       "S": 18,
                       "T": 19,
                       "U": 20,
                       "V": 21,
                       "W": 22,
                       "X": 23,
                       "Y": 24,
                       "Z": 25
                   }




def plotLetterFrequency(inputString):
    mylist=[]

    for char in inputString:
        if char in alphabetToNumbersDict.keys():
            mylist+=[alphabetToNumbersDict[char]]
            pass
    fig, ax = pyplot.subplots()
    counts, bins, patches = ax.hist(mylist,bins=26,facecolor='yellow', edgecolor='gray')

# Set the ticks to be at the edges of the bins.
    ax.set_xticks(bins)
# Label the raw counts and the percentages below the x-axis...
    bin_centers = 0.5 * numpy.diff(bins) + bins[:-1]
    letters=[]
    for i in range(1,27):
        letters+=numbersToAlphabetDict[i]
        pass
    ax.set_xticklabels(letters)

# Give ourselves some more room at the bottom of the plot
    pyplot.subplots_adjust(bottom=0.15)
    pyplot.show()
    return ax

def plotNumberFrequency(inputString,numberOfBins=30):
    mylist=[]
    previousWasSpace=True
    previousWasLetter=False
    numberString="s"
    for char in inputString:
        if char==" ":
            previousWasLetter=False
            previousWasSpace=True
            numberString="s"
            pass
        if previousWasLetter:
            numberString+=char
            mylist+=[numberString]
            pass
        if char !=" " and previousWasSpace:
            numberString+=char
            previousWasSpace=False
            previousWasLetter=True

    fig, ax = pyplot.subplots()
    counts, bins, patches = ax.hist(mylist,bins=30,facecolor='yellow', edgecolor='gray')

# Set the ticks to be at the edges of the bins.
    ax.set_xticks(bins)
# Label the raw counts and the percentages below the x-axis...

# Give ourselves some more room at the bottom of the plot
    pyplot.subplots_adjust(bottom=0.15)
    pyplot.show()
    return ax    


alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"

englishLetterFrequency={"A": 0.082,
                        "B": 0.015,
                        "C": 0.028,
                        "D": 0.042,
                        "E": 0.127,
                        "F": 0.022,
                        "G": 0.020,
                        "H": 0.061,
                        "I": 0.07,
                        "J": 0.001,
                        "K": 0.008,
                        "L": 0.04,
                        "M": 0.024,
                        "N": 0.067,
                        "O": 0.075,
                        "P": 0.019,
                        "Q": 0.001,
                        "R": 0.06,
                        "S": 0.063,
                        "T": 0.09,
                        "U": 0.028,
                        "V": 0.01,
                        "W": 0.024,
                        "X": 0.001,
                        "Y": 0.021,
                        "Z": 0.0007
                    }

from scipy.stats import chi2

def poisson_interval(n,alpha=0.05):
    a=alpha
    low,high = (chi2.ppf(a/2,2*n)/2, chi2.ppf(1-a/2,2*n+2)/2)
    if n==0:
        low=0.0
        pass
    return low,high


def isWithin95(count, letter,messageLength):
    interval = poisson_interval(messageLength*englishLetterFrequency[letter],0.2)
    if count > interval[0] and count < interval[1]:
        return True
    else:
        return False

# for RSA


def findPrimes(maxVal=1000):
    listOfPrimes=[]
    for i in range(maxVal):  
        if is_prime(i):
            listOfPrimes+=[i]
            pass
        pass
    return listOfPrimes

def is_prime(n):
    if n == 2:
        return True
    if n % 2 == 0 or n <= 1:
        return False
    sqr = int(math.sqrt(n)) + 1
    for divisor in range(3, sqr, 2):
        if n % divisor == 0:
            return False
    return True


def checkIsDivisor(a,b):
    return (b/a)*a == b

def findModMultInverse(e,phi_n):
    for i in range(phi_n):
        if e*i % phi_n ==1:
            return i


def getIntegerFromBinaryString(inputBinaryString):
    outputInt=0
    bitCount=0
    for bit in reversed(inputBinaryString):
        if bit=='1':
            outputInt+=pow(2,bitCount)
            pass
        bitCount+=1
    return outputInt

def getBinaryStringFromString(text, encoding='utf-8'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def getStringFromBinaryString(bits, encoding='utf-8'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding)

def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

def getBinaryStringFromInteger(i):
    return bin(i)[2:]

def getNumberOfBitsInInteger(i):
    binString = bin(i)[2:]
    return binString.__len__()
