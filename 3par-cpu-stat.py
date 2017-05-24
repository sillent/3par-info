#!/usr/bin/env python

from __future__ import print_function
import sys
import pickle


def parse(data, typ, node):
    for d in data:
        if typ in d:
            try:
                ret = d[typ][node]
            except KeyError:
                ret = 0
        else:
            ret = 0
    print(ret)


def getval(host, typ, node):
    fpath = "/tmp/%s-cpu.stat" % host
    try:
        with open(fpath, "r") as fi:
            data = pickle.load(fi)
    except IOError:
        print(0)
        sys.exit(1)

    if type(data) == list:
        if len(data) > 0:
            parse(data, typ, int(node))
        else:
            print(0)
    else:
        print(0)


def print_usage():
    print("%s < hostname > <type > <node_id> \n\
Where type is: \n\
    usr,sys,idl,intr,ctxt" % sys.argv[0])


def check_arg():
    if len(sys.argv) != 4:
        print_usage()
        sys.exit(1)


if __name__ == '__main__':
    check_arg()
    script, hostname, typ, node = sys.argv
    getval(hostname, typ, node)
