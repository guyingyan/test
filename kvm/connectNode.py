import os,sys,re
import jenkins
import json
import urllib
import urllib2
import time

jenkinsMaster = "http://10.110.18.40:8080"
server = jenkins.Jenkins(jenkinsMaster, username="guyingyan", password="ying123456a?")
server.enable_node('10.110.25.54')
