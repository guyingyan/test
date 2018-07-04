import os
import sys
import commands
import jenkins
import time
import shutil

def getNodeIp():
    macline = commands.getoutput('virsh dumpxml kvm-jenkins|grep mac|grep address')
    mac = macline.split("'")[1]
    ipaddr = commands.getoutput('''arp -a|grep %s|cut -d '(' -f2|cut -d ')' -f1''' %mac)
    return ipaddr
def checkNode(jenkinsServer):
    try:
        jenkinsServer.assert_node_exists('kvmNode', exception_message='node %s does not exist.......')
    except jenkins.JenkinsException, e:
        print (e)
    nodeflag = jenkinsServer.node_exists('kvmNode') 
    return nodeflag

def addJenkinsNode():
    ipaddr = getNodeIp()
    while len(ipaddr)<7:
       # time.sleep(3)
        #ipaddr = getNodeIp()
        status,ipaddr=commands.getstatusoutput("/home/test/kvm/search.sh")
    print (ipaddr)
    nodename = 'kvmNode'
    jenkinsMaster = sys.argv[1]
    cid = '2a90319b-4f75-40da-989a-e0c9633169bf'
    server = jenkins.Jenkins(jenkinsMaster)
    flag = checkNode(server)
    
    while flag == True:
        time.sleep(2)
        flag = checkNode(server)
    
    params = {
        'port': 22,
        'username': 'juser',
        'credentialsId': cid,
        'host': ipaddr
    }
    print ("params: %s" %params)
    try:
        server.create_node(
            nodename,nodeDescription='add slave',
            remoteFS='/data',
            labels='slave',
            exclusive=False,
            launcher=jenkins.LAUNCHER_SSH,
            launcher_params=params)
    except Exception, e:
       print 'str(e):\t\t', str(e)
       print ("failed add jenkins node")
def checkKVM(flagFile):
    if os.path.isfile(flagFile):
        with open(flagFile, 'r') as f:
            lines = f.readlines()
            flag = lines[0].replace("\n", "")
            f.close
    print ("==%s==" %flag)
    return flag

def cleanImage():
    baseimage='/var/lib/libvirt/images/kvm.img'
    #image = '/var/lib/libvirt/images/kvm-jenkins.img'
    #if os.path.exists(image):
    #    os.remove(image)
    #else:
    #    print ('no image can be cleaned!!!')
    #if os.path.exists(baseimage):
    #    shutil.copyfile(baseimage,image)
    #else:
    #    print ('no base image can be copied!!!')
        
def startKVM():
#    flagFile = os.path.join('/tmp','kvm-jenkins.flag')
 #   status =  False
    #while status != 'True':
      #  time.sleep(3)
     #   print ('KVM exist, while it is not exist will create KVM: %s ' %status)
       # status = checkKVM(flagFile)
    #os.system('virsh destroy kvm-jenkins')
    #os.system('virsh undefine kvm-jenkins')
    os.system('virsh shutdown kvm-jenkins')
    os.system('virsh snapshot-revert kvm-jenkins 1529914802')
    os.system('virsh start kvm-jenkins')
    #cleanImage()

    #with open(flagFile, 'w') as f:
     #   f.write('False')
      #  f.close()

    #os.popen("virt-install --name kvm-jenkins --ram 2048 --disk path=/var/lib/libvirt/images/kvm-jenkins.img --import &\n\n\n")
def main():
    sta = startKVM()
    print (sta)
    lines = os.popen('virsh dumpxml kvm-jenkins|grep mac')
    for line in lines:
       print (line)
    print ("add jenkins node ..................")
    addJenkinsNode()
   

if __name__ == "__main__":
    main()
