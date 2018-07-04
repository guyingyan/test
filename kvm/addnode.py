import os
import sys
import commands
import jenkins
import json
import time
import shutil
import libvirtapi


basedir = os.path.dirname(os.path.realpath(__file__))

kvmName = 'kvm-jenkins'

credentialId = 'k-v-m-i-d'

kvmnodeUserName = 'root'
kvmnodePasswd = '123456a?'

def createCredential(jenkinsMaster, nodeUsername, nodePasswd, credentialId):
    para = "--data-urlencode"
    post_url = '%s/credentials/store/system/domain/_/createCredentials ' %jenkinsMaster
    credent = {
    "scope": "GLOBAL",
    "id": credentialId,
    "username": nodeUsername,
    "password": nodePasswd,
    "description": "auto added",
    "$class": "com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl"}

    data = json.dumps(credent)
    cmd = '''curl -X POST %s %s 'json={"":"0","credentials":%s}'
          ''' %(post_url, para, data)
    print (cmd)
    os.system(cmd)


def getNodeIp():
    macline = commands.getoutput('virsh dumpxml %s|grep mac|grep address' %kvmName)
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

def addJenkinsNode(jenkinsMaster):
    ipaddr = getNodeIp()
    while len(ipaddr)<7:
       # time.sleep(3)
        #ipaddr = getNodeIp()
        status,ipaddr=commands.getstatusoutput("%s/search.sh" %basedir)
    print (ipaddr)
    nodename = 'kvmNode'
    cid = credentialId
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
    image = '/var/lib/libvirt/images/%s.img' %kvmName
    if os.path.exists(image):
        os.remove(image)
    else:
        print ('no image can be cleaned!!!')
    if os.path.exists(baseimage):
        shutil.copyfile(baseimage,image)
    else:
        print ('no base image can be copied!!!')

        
def startKVM():
    flagFile = os.path.join('/tmp','%s.flag' %kvmName)
    status =  False
    while status != 'True':
        time.sleep(3)
        print ('KVM exist, while it is not exist will create KVM: %s ' %status)
        status = checkKVM(flagFile)
    conn = libvirtapi.createConnection()
    flag = libvirtapi.getDomInfoByName(conn, kvmName)
    libvirtapi.closeConnection(conn)
    
    if flag is not 1:
        os.system('virsh destroy %s' %kvmName)
        os.system('virsh undefine %s' %kvmName)
    
    cleanImage()

    with open(flagFile, 'w') as f:
        f.write('False')
        f.close()
    try:
        os.popen("virt-install --name %s --ram 2048 --disk path=/var/lib/libvirt/images/%s.img --import &\n\n\n" %(kvmName,kvmName))
    except:
        print('create kvm failed')

def startService():
    os.system('systemctl start docker')
def main():
    jenkinsMaster = sys.argv[1]
    createCredential(jenkinsMaster, kvmnodeUserName, kvmnodePasswd, credentialId)
    sta = startKVM()
    print (sta)
    lines = os.popen('virsh dumpxml kvm-jenkins|grep mac')
    for line in lines:
       print (line)
    print ("add jenkins node ..................")
    addJenkinsNode(jenkinsMaster)
   

if __name__ == "__main__":
    main()
