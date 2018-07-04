import os
import sys
import libvirtapi

name = "kvm-jenkins"

conn = libvirtapi.createConnection()
flag = libvirtapi.getDomInfoByName(conn, name)
libvirtapi.closeConnection(conn)

print (flag)
