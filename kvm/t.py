import os
import sys
import time

kmvNameList = ['kvm-1', 'kvm-2', 'kvm-3', 'kvm-4']
tmpkvmdir = '/tmp/kvm'

def diff(listA,listB):
    notused = list(set(listB).difference(set(listA)))
    return notused

def getdifflist():
    listB = kmvNameList
    listA = getlistofkvmDir()
    notusedkvmname = diff(listA,listB)
    return notusedkvmname

def getNumberofkvm():
    count = 0
    for fn in os.listdir(tmpkvmdir):
        count = count + 1
    return count
def getlistofkvmDir():
    for root, dirs, files in os.walk(tmpkvmdir): 
        usingKvmList = files
    return usingKvmList 
def startKVM_1():
    kvmNumber = getNumberofkvm()
    while kvmNumber >= 4:
        time.sleep(3)
        print ('KVM exist, while it is not exist will create KVM: %s ' %status)
        kvmNumber = getNumberofkvm()
    
    notusedlist = getdifflist()
    usekvmname = notusedlist[0]
    print(usekvmname)
    os.system('touch %s/%s' %(tmpkvmdir,usekvmname))

    

if __name__ == "__main__":
    #number = getNumberofkvm()
    #print (number)
    startKVM_1()
    #getlistofkvmDir()
    #notused = getdifflist()
    #print (notused[0])
