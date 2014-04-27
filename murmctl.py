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

def _print_name_from_dict(dict):
    for key in dict:
        print dict[key].name

def _getSession(server, name):
    all_users = server.getUsers()
    for u,d in all_users.items():
        if d.name == name:
            return d.session

def _get_user_info(server,name):
    all_users = server.getUsers()
    for key in all_users:
        if all_users[key].name == name:
            return all_users[key]

def list_object_names(args):
    if args.object == 'channels':
        _print_name_from_dict(server.getChannels())
    elif args.object == 'users':
        _print_name_from_dict(server.getUsers())
    elif args.object == 'bans':
        _print_name_from_dict(server.getBans())
    elif args.object == 'registered':
        _print_name_from_dict(server.getRegisteredUsers(''))
    elif args.object == 'tree':
        print server.getTree()


def logdump(args):
    length = server.getLogLen()
    logs = server.getLog(0,length)
    #logs have newest entry as first item in the list
    #we want it to be visible on screen so make it the last entry
    for log in reversed(logs):
        print '%s: %s' %(log.timestamp, log.txt)

def status(args):
    if server.isRunning():
        print 'Running. Uptime: %d seconds' %server.getUptime()
    else:
        print 'Stopped'

def kick_user(args):
    sessionid = _getSession(server, args.user)
    server.kickUser(sessionid, args.message)

def send_message(args):
    sessionid = _getSession(server, args.user)
    server.sendMessage(sessionid, args.message)

#still broken....
def register_user(args):
    print _get_user_info(server, args.user)
    user_info = Murmur.UserInfo(args.user,1)
    print user_info
    server.registerUser(user_info)

def channel_actions(args):
    if args.action == 'add':
        if args.parent:
            channels = server.getChannels()
            for key in channels:
                channels[key].name == args.parent
                args.parent = channels[key].id

        server.addChannel(args.channel_name,args.parent)
    elif args.action =='remove':
        channels = server.getChannels()
        for key in channels:
            if channels[key].name == args.channel_name:
                server.removeChannel(channels[key].id)




props = Ice.createProperties()
props.setProperty('Ice.Default.EncodingVersion','1.0')

id = Ice.InitializationData()
id.properties = props

comm = Ice.initialize(id)

proxy = comm.stringToProxy("Meta: tcp -p 6502")

meta = Murmur.MetaPrx.checkedCast(proxy)

server = meta.getServer(1)

parser = argparse.ArgumentParser()
subparser = parser.add_subparsers()
#subparser for list functionality
list_parser = subparser.add_parser('list', help='lists info from the server')
list_parser.add_argument('object', help='object to list')
list_parser.set_defaults(func=list_object_names)
#subparser for dumping logs to the screen
dump_parser = subparser.add_parser('logdump', help='dump logs to the screen')
dump_parser.set_defaults(func=logdump)
#status parser
status_parser = subparser.add_parser('status', help='get the status of the server')
status_parser.set_defaults(func=status)
#kick user parser
kick_parser = subparser.add_parser('kick', help='kick a user')
kick_parser.add_argument('user', help='user to kick')
kick_parser.add_argument('-m','--message',default=' ',
        help='message to send to the user')
kick_parser.set_defaults(func=kick_user)
#send a message
message_parser = subparser.add_parser('message', help='send a message to a user')
message_parser.add_argument('user', help='user to send a message to')
message_parser.add_argument('message',help='body of the messeage')
message_parser.set_defaults(func=send_message)
#register a user
reg_parser = subparser.add_parser('register', help='register a user')
reg_parser.add_argument('user', help='user to register')
reg_parser.set_defaults(func=register_user)
#add channel
channel_parser = subparser.add_parser('channel', help='add or remove channels')
channel_parser.add_argument('action', help='add or remove')
channel_parser.add_argument('channel_name', help='name of new channel')
channel_parser.add_argument('-p','--parent',default=0,
        help='parent of channel you are adding')
channel_parser.set_defaults(func=channel_actions)
args = parser.parse_args()
args.func(args)


    
