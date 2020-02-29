#!/usr/bin/python

import xmlrpclib

#xmlrpc connection
SERVER = data.SERVER
proxy = xmlrpclib.ServerProxy(SERVER)
multicall = xmlrpclib.MultiCall(proxy)

#multicall
multicall.d.multicall2("", "main")
multicall.d.multicall2("", "stopped")
multicall.d.multicall2("", "complete")
multicall.d.multicall2("", "seeding", "d.up.rate=", "d.hash=", "d.name=")
multicall.d.multicall2("", "leeching", "d.down.rate=", "d.hash=", "d.name=")

#data
uploading_torrents = 0
downloading_torrents = 0

print("uploading torrents:")
for i in multicall()[3]:
  if i[0] > 0:
    uploading_torrents += 1
    print(str(round(i[0]/float(1024),2)) + " kByte - " + i[2])

print("downloading torrents:")
for i in multicall()[4]:
  if i[0] > 0:
    print(str(round(i[0]/float(1024),2)) + " kByte - " + i[2])

active_torrents = uploading_torrents + downloading_torrents
inactive_torrents = len(multicall()[0]) - active_torrents

#all torrents
print "all: ", len(multicall()[0])

#downloading torrents
print("downloading torrents ( number ): " + str(downloading_torrents))

#complete torrents
print "complete torrents: ", len(multicall()[2])

#stopped torrents
print "stopped torrents: ", len(multicall()[1])

#active torrents
print "active torrents: " + str(active_torrents)

#inactive torrents
print "inactive torrents: " + str(inactive_torrents)

#uploading torrents
print("uploading torrents ( number ): " + str(uploading_torrents))

