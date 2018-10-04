#! /usr/bin/env python3

# Echo client program
import socket, sys, re

sys.path.append("../lib")       # for params
import params

from framedSock import framedSend, framedReceive


switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "fileClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)


s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break
if s is None:
    print('could not open socket')
    sys.exit(1)
cmd = input('ftp$ ')
para = cmd.split()
if (len(para) == 2 and para[0]=='put'):
    try:#check if put and filename
        print(para[1])
        file = open(para[1], 'r')

    except:
        print('file not found')
        exit(0)

    if True:
        filenam = './' + para[1]#send filename
        #print(filenam)
        framedSend(s, filenam.encode(), debug)
        print("received:", framedReceive(s, debug))

    while True:#read file

        data = file.read(100)#.encode()
        data = data.strip()

        if not data:# end of file
            framedSend(s, '~'.encode(), debug)
            print("received:", framedReceive(s, debug))
            break
        #print(data.encode())
        framedSend(s, data.encode(), debug)#send file by 100 byte increments
        print("received:", framedReceive(s, debug))


else:
    print('no command or missing parameter')