#!/usr/bin/env python3
#-*-conding:utf8-*-

from scapy.all import *
import sys


def tcp_replay(srcip,dstip,srcport,dstport,data):
    replay_packet = IP(srcip,dstip)/TCP(srcport,dstport)/data
    send(replay_packet,inter = 1, count= 1)

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 tcp_replay_test.py /filepath/filename")
        exit(0)
    else:
        filename = sys.argv[1]
        pcaps = rdpcap(filename)
        packet = pcaps[0]
        src = packet.src
        dst = packet.dst
        sport = packet.sport
        dport = packet.dport
        payload = packet.load
        tcp_replay(src,dst,sport,dport,payload)

if __name__ == '__main__':
    main()
