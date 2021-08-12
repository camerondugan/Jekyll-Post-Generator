from genericpath import isfile
import os
import random
from collections import defaultdict
from datetime import datetime

numPrevChars = 4
prevChars = [''] * numPrevChars
prevChars[0] = '\n'

def updatePreviousChars(c):
    prev = prevChars[0]
    prevChars[0] = c
    for i in range(1,numPrevChars):
        prev, prevChars[i] = prevChars[i], prev

def test_charUpdate():
    var = ['']*(numPrevChars)
    assert(prevChars == var)
    updatePreviousChars("a")
    var[0] = "a"
    assert(prevChars == var)
    updatePreviousChars("b")
    var[0] = "b"
    var[1] = "a"
    assert(prevChars == var)

def genString(arr):
    string = ""
    for c in arr:
        string += str(c)
    return string

def test_genString():
    arr = [100,2,5,"belly"]
    assert('10025belly' == genString(arr))

def addCharToGrabBag(c,grabBag):
    string = genString(prevChars)
    while len(string)>0:
        grabBag[string].append(c)
        string = string[:-1]
    updatePreviousChars(c)
    return grabBag

def genGrabBag(path,header,filter):
    grabBag = defaultdict(lambda: [])
    files = os.listdir(path)
    for file in files:
        if os.path.isfile(os.path.join(path, file)):
            f = open(os.path.join(path, file),'r')
            curline = 0
            for line in f:
                curline += 1
                if- (filter != ''):
                    shouldRead = line.__contains__(filter)
                    if (not shouldRead): continue
                if (header): 
                    grab = curline < 7
                else: 
                    grab = curline > 7
                if (grab):
                    for char in line:
                        grabBag = addCharToGrabBag(char,grabBag)
            f.close()
    return grabBag

#a kind of test
def printGrabBag(grabBag):
    for k,v in grabBag.items():
        if (len(v)>0):
            print(str(k) + ": " + str(v))

#from grabBag
def get(grabBag):
    string = genString(prevChars)
    potential = grabBag[string]
    count = 0
    while(len(potential)<1):
        string = string[:-1]
        potential = grabBag[string]
        if (count-5>numPrevChars):
            return random.choice(list(grabBag.keys()))
        count += 1
    result = random.choice(potential)
    updatePreviousChars(result)
    return str(result)
    

def generate(file,iter,grabBag,stopOnLine):
    while iter>0:
        iter -= 1
        c = get(grabBag)
        file.write(c)  
        if (stopOnLine):
            if (c == '\n'):
                break

def createString(iter,grabBag,stopOnLine):
    out = ""
    while iter>0:
        iter -= 1
        c = get(grabBag)
        if (stopOnLine and c == '\n'):
            break
        out += c
    return out

#num being how many characters the computer can look back
def setAccuracy(num):
    global numPrevChars,prevChars
    dif = num - numPrevChars
    numPrevChars = num
    if (dif > 0):
        while dif > 0:
            prevChars.append('')
            dif -= 1
    else:
        while dif < 0:
            prevChars.remove(prevChars[len(prevChars)-1])
            dif += 1

def genFileName(path):
    grabBag = defaultdict(lambda: [])
    files = os.listdir(path)
    for file in files:
        if os.path.isfile(os.path.join(path, file)):
            file = file[11:len(file)-3] + '\n'
            for c in file:
                grabBag = addCharToGrabBag(c,grabBag)
    name = createString(20,grabBag,True)
    name = datetime.today().strftime('%Y-%m-%d-') + name
    name += '.md'
    return name

def main():
    path = '_meme'
    setAccuracy(1)
    name = genFileName(path)
    print(name)
    output = open(f'output/{name}','w')
    output.write("---\n")
    headerTags = ['title: ','header: ','description: ','layout: ','permalink: ']
    setAccuracy(3)
    for tag in headerTags:
        grabBag = genGrabBag(path,True,tag)
        generate(output,2000,grabBag,True)
    output.write("---\n\n")
    setAccuracy(10)
    grabBag = genGrabBag(path,False,'')
    generate(output,350,grabBag,False)
    output.close()

if __name__ == "__main__":
    for i in range(10):
        main()