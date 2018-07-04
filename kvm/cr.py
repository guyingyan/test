import os
import sys
import jenkins
import json

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
if __name__ == "__main__":
    jenkinsMaster = sys.argv[1]
    nodeUsername = 'root'
    nodePasswd = '123456a?'
    credentialId = 'k-v-m-i-d'
    createCredential(jenkinsMaster, nodeUsername, nodePasswd,credentialId)
