#!/usr/bin/python

import commands
import os


status,ip=commands.getstatusoutput("/home/test/kvm/search.sh")
print (ip)

#try:

#    os.system('cd /ls')
#except Exception, e:
  #  print 'str(e):\t\t', str(e)
 #   print 'e.message:\t', e.message
