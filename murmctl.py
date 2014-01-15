#!/usr/bin/env python

import Ice
Ice.loadSlice('-I/usr/share/Ice-3.5.1/slice /opt/murmur/Murmur.ice')
import Murmur
import argparse



props = Ice.createProperties()
props.setProperty('Ice.Default.EncodingVersion','1.0')

id = Ice.InitializationData()
id.properties = props

comm = Ice.initialize(id)

proxy = comm.stringToProxy("Meta: tcp -p 6502")

meta = Murmur.MetaPrx.checkedCast(proxy)

server = meta.getServer(1)

parser = argparse.ArgumentParser()
parser.add_argument('command', help='command to perform on murmur server')
parser.add_argument('object', help='object the command should be performed on',
        default='None')
args = parser.parse_args()


if args.command == 'list':
    if args.object == 'channels':
        print server.getChannels()
    elif args.object == 'users':
        print server.getUsers()
    elif args.object == 'bans':
        print server.getBans()
    elif args.object == 'registered':
        print server.getRegisteredUsers('')
    elif args.object == 'tree':
        print server.getTree()
elif args.command == 'dump':
    if args.object =='logs':
        length = server.getLogLen()
        print server.getLog(0,length)






