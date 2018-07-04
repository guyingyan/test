import os
import sys
import jenkins
import socket
import time
import urllib2

def send_request(url):  
    try:  
        res = urllib2.urlopen(urllib2.Request(url))  
        code = res.getcode()  
        res.close()  
        return code  
    except Exception,e:  
        return False  

def getIP():
    myname = socket.getfqdn(socket.gethostname(  ))
    myaddr = socket.gethostbyname(myname)
    return myaddr

if __name__ == "__main__":
    ip = getIP()
    jenkinsurl = ('http://%s:8080' %ip)
    print (jenkinsurl)
    status = send_request(jenkinsurl)
    while status is not True:
        status = send_request(jenkinsurl)
        time.sleep(3)
    server = jenkins.Jenkins(jenkinsurl)

    server.build_job('travis')


