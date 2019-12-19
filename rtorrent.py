#!/usr/bin/python3
# -*- coding: utf-8 -*-

#import required data
import data

import xmlrpc.client
import json

# variables
downloading_torrents = 0
uploading_torrents = 0
status = ''
stopped_torrents = 0
paused_torrents = 0
active_torrents = 0

#xmlrpc connection
SERVER = data.SERVER
connection = xmlrpc.client.ServerProxy(SERVER)

def get_Torrents(connection):
  downloadlist = connection.download_list("", "main")
  return downloadlist

def active_Torrents(downloadlist):
  return len(downloadlist)

def pretty_number(num):
  kbyte = int(num) / 1024
  if str(kbyte).endswith(".0"):
    kbyte = int(kbyte)
  else:
    kbyte = "{0:.3f}".format(kbyte)
  return kbyte


#total torrents
all_torrents = active_Torrents(get_Torrents(connection))

#upload speed
upload_speed = connection.throttle.global_up.rate()

#download speed
download_speed = connection.throttle.global_down.rate()

#status ( up, down, updown )
if upload_speed > 0:
  status = 'uploading'
if download_speed > 0:
  status = 'downloading'
if upload_speed > 0 and download_speed > 0:
  status = 'uploading and downloading'

#max upload speed
max_upload_speed = connection.throttle.global_up.max_rate()

#max download speed
max_download_speed = connection.throttle.global_down.max_rate()

## actions ##
#set max upload speed
#connection.throttle.global_up.max_rate.set_kb("", 300)
#set max download speed
#connection.throttle.global_down.max_rate.set_kb("", 3000)

#stop all torrents
#start all torrents

torrents = {}

for torrent in get_Torrents(connection):
  #name of torrent
  print(f"torrent hash: {torrent}, torrent_name: {connection.d.name(torrent)}")

  if connection.d.incomplete(torrent) > 0:
    downloading_torrents += 1
  if connection.d.up.rate(torrent) > 0:
    uploading_torrents += 1

#stopped torrents
  if connection.d.is_open(torrent) == 0:
    stopped_torrents += 1

#paused torrents
  if connection.d.is_open(torrent) == 1 and connection.d.is_active(torrent) == 0:
    paused_torrents += 1

#active torrents
  if connection.d.is_open(torrent) == 1 and connection.d.is_active(torrent) == 1:
    active_torrents += 1

#get array of torrents -> json
  torrents[torrent] = connection.d.name(torrent)


#print rtorrent data
print(json.dumps(torrents))

print(f"all torrents: {all_torrents}")
print(f"downloading (leeching): {downloading_torrents}")
print(f"uploading (seeding): {uploading_torrents}")
print(f"max upload speed: {pretty_number(max_upload_speed)} kbyte")
print(f"max download speed: {pretty_number(max_download_speed)} kbyte")

print(f"upload speed: {pretty_number(upload_speed)} kbyte")
print(f"download speed: {pretty_number(download_speed)} kbyte")
print(f"status: {status}")

print(f"stopped torrents: {stopped_torrents}")
print(f"paused torrents: {paused_torrents}")
print(f"active torrents: {active_torrents}")
