#!/usr/bin/python

import os
import sys
import shutil
import commands
import time

def search():
    for i in range(1,254):
        os.system('ping -c1 10.110.25.%s' %i)
def main():
    test()
    addJenkinsNode()
def cleanImage():
    baseimage='/var/lib/libvirt/images/base_1.img'
    image = '/var/lib/libvirt/images/demo.img'
    if os.path.exists(image):
        os.remove(image)
    else:
        print ('no image can be cleaned!!!')
    if os.path.exists(baseimage):
        shutil.copyfile(baseimage,image)
    else:
        print ('no base image can be copied!!!')
def test():
    os.system('virsh destroy demo')
    os.system('virsh undefine demo')
  #  cleanImage()

    #os.system("virt-install --name demo --ram 2048 --disk path=/var/lib/libvirt/images/demo.img --import &\n\n\n")
    os.popen("virt-install --name demo --ram 2048 --disk path=/var/lib/libvirt/images/demo.img --import &\n\n\n")
    #os.system("./a.sh")
    print ("xxxxx")
    os.system("\n")
    os.system("/home/test/search.sh")

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


if __name__=="__main__":
    main()
