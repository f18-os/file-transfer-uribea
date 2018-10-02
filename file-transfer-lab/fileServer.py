#! /usr/bin/env python3
import sys, os, socket
sys.path.append("../lib")       # for params
import params



switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "fileserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

while True:
    sock, addr = lsock.accept()

    from framedSock import framedSend, framedReceive

    if not os.fork():
        print("new child process handling connection from", addr)
        while True:
            payload = framedReceive(sock, debug)
            if debug: print("rec'd: ", payload)
            if not payload:
                if debug: print("child exiting")
                sys.exit(0)
            # payload = payload.decode()
            print(payload)
            payload = payload.decode()
            if payload.startswith('./'):
                print(payload)
                #payload = payload.decode()
                fileDir = os.path.dirname(os.path.realpath('__file__'))
                filename = os.path.join(fileDir, 'server/'+payload)
                file = open(filename, 'w')
            elif payload.startswith('~'):
               file.close()
            else:
                print(payload)
                file.write(payload)
            payload = payload.encode()
            payload += b"!"             # make emphatic!
            framedSend(sock, payload, debug)