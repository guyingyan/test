import os
import sys
import commands
import jenkins
import time
import paramiko


def deleteJenkinsNode():
    jenkinsMaster = sys.argv[1]
    nodename = 'kvmNode'
    jenkinsMaster = sys.argv[1]
    cid = '3ea2a0cd-b611-433b-9998-d2d8882f97b2'
    server = jenkins.Jenkins(jenkinsMaster)
    try:
        server.delete_node(nodename)
    except:
        print ('can not delete node')


def copyfile():
    transport = paramiko.Transport(('10.110.25.227', 22))
    transport.connect(username='root', password='123456a?')
 
    sftp = paramiko.SFTPClient.from_transport(transport)
 
    sftp.put('/tmp/kvm.flag', '/tmp/kvm.flag')
 
    transport.close()

def alter(file,old_str,new_str):
    file_data = ""
    with open(file, "r") as f:
        for line in f:
            if old_str in line:
                line = line.replace(old_str,new_str)
            file_data += line
    with open(file,"w") as f:
        f.write(file_data)



def main():
    alter("/tmp/kvm-jenkins.flag", "False", "True")
    deleteJenkinsNode()
   

if __name__ == "__main__":
    main()
