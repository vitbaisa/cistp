#!/usr/bin/python3

import sys

pos = int(sys.argv[1])

sen = []


while 1:
    try:
        line = sys.stdin.readline()
    except:
        continue
    if not line:
        break
    if line.startswith('<'):
        if line.startswith('<s'):
            sen = []
        elif line.startswith('</s'):
            for i in range(len(sen)):
                print("%s\t%d\t%d" % (sen[i], len(sen), i+1))
            sen = []
    else:
        try:
            sen.append(line.strip().split('\t')[pos])
        except:
            continue
