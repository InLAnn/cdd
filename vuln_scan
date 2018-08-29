#!/usr/bin/env python3
#-*- codinf: utf-8 -*-

import sys
import os
import socket

def retBanner(ip,port):
    try:
        socket.setdefaulttimeout(2)
        s = socket.socket()
        s.connect((ip,port))
        banner = s.recv(1024)
        return banner
    except:
        return

def checkVulns(banner,filename):
    f = open(filename,'r')
    for line in f.readline():
        if line.strip('\n') in banner:
            print('[+] Server is vulnerable: ' + banner.strip('\n'))

def main():
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        if not os.path.isfile(filename):
            print('[-] ' + filename + 'does not exist.')
            exit(0)
        elif not os.access(filename,os.R_OK):
            print('[-] ' + filename + 'access denied.')
            exit(0)
        else:
            print('[-] Usage: ' + str(sys.argv[0]) + ' <vuln filename>')
            exit(0)

        portList = [21,22,25,80,110,443]
        for x in range(1,254):
            ip = '192.168.30.' + str(x)
            for port in portList:
                banner = retBanner(ip,port)
                if banner:
                    print('[+]' + ip + ': ' + banner)
                    checkVulns(banner,filename)
                else:
                    print('No')

if __name__ == '__main__':
    main()

