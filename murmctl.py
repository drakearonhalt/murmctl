#!/usr/bin/env python

# murmctl 
# Copyright (C) 2014  Drake Aronhalt
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


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
parser.add_argument('remain',nargs='*')
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
elif args.command == 'status':
    if server.isRunning():
        print 'Running. Uptime: %d seconds' %server.getUptime()
    else:
        print 'Stopped'

