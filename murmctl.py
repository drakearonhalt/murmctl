#!/usr/bin/env python

import Ice
Ice.loadSlice('-I/usr/share/Ice-3.5.1/slice /opt/murmur/Murmur.ice')
import Murmur

props = Ice.createProperties()
props.setProperty('Ice.Default.EncodingVersion','1.0')

id = Ice.InitializationData()
id.properties = props

comm = Ice.initialize(id)

proxy = comm.stringToProxy("Meta: tcp -p 6502")

meta = Murmur.MetaPrx.checkedCast(proxy)

server = meta.getServer(1)

channels = server.getChannels()



