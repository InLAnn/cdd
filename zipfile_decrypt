#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import zipfile
import threading

def extractFile(zFile,password):
    try:
        zFile.extractall(pwd = password)
        print('Found Passwd : ',password)
        return password
    except:
        pass

def main():
    zFile = zipfile.ZipFile('unzip.zip')
    passFile = open('dictionary.txt')
    for line in passFile.readline():
        password = line.strip('\n')
        t = threading.Thread(target=extractFile, args=(zFile,password))
        t.start()
        #One thread
        '''
        guess =extractFile(zFile,password)
        if guess:
            print('Password = ', password)
            return
        else:
            print('Cannot find password')
            return 
        '''

if __name__ == '__main__':
    main()
