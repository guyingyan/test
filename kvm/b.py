import os
import sys
import commands
import jenkins
import time
import shutil

def getNodeIp():
    macline = commands.getoutput('virsh dumpxml demo|grep mac|grep address')
    mac = macline.split("'")[1]
    ipaddr = commands.getoutput('''arp -a|grep %s|cut -d '(' -f2|cut -d ')' -f1''' %mac)
    return ipaddr

def addJenkinsNode():
    ipaddr = getNodeIp()
    while len(ipaddr)<7:
        time.sleep(3)
        os.system('./search.sh')
        ipaddr = getNodeIp()
    print (ipaddr)
def main():
    addJenkinsNode()
   

if __name__ == "__main__":
    main()
