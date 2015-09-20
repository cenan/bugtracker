#!/usr/bin/env python

import zlib
import struct

path = "/home/cenan/projects/old/bugtrack/.git/"

def read_tree(obj):
    idx = 5
    idx = obj.index("\0") + 1
    files = []
    while idx < len(obj):
        p1 = obj.index(" ", idx)
        p2 = obj.index(chr(0), p1+1)
        access_code = obj[idx:p1]
        file_name = obj[p1+1:p2]
        sha1hash = ''.join(("%02x" % int(ord(y)) for y in obj[p2+1:p2+21]))
        idx = p2+21
        files.append({'filename': file_name, 'access_code': access_code, 'hash': sha1hash.__str__()})
    return files

def read_blob(hash):
    return read_object(hash)

def read_object(obj):
    try:
        cont = zlib.decompress(open(path+'objects/'+obj[0:2]+'/'+obj[2:], 'rb').read())
    except IOError:
        return ""
    if cont[0:4] == 'tree':
        return read_tree(cont)
    if cont[0:4] == 'blob':
        pos = cont.index("\0")
        return cont[pos:]
    if cont[0:6] == 'commit':
        return cont[7:]
    print 'UNKNOWN OBJECT TYPE'

def read_history():
    head = open(path+'HEAD').read().split()[1]
    head_commit_hash = open(path+head).read().strip()
    head_commit_obj = read_object(head_commit_hash)
    if head_commit_obj == "":
        return []
    parent, parent_hash = head_commit_obj.split("\n")[1].split(' ')[0:2]
    history = []
    while parent == 'parent':
        history.append(parent_hash)
        commit_obj = read_object(parent_hash)
        if commit_obj == "":
            break
        parent, parent_hash = commit_obj.split("\n")[1].split(' ')[0:2]
    return history

def head_hash():
    head = open(path+'HEAD').read().split()[1]
    return open(path+head).read().strip()

def read_head():
    head = open(path+'HEAD').read().split()[1]
    head_commit_hash = open(path+head).read().strip()
    head_commit_obj = read_object(head_commit_hash)
    x = head_commit_obj.split()
    print head_commit_obj
    if len(x) == 0:
        return []
    head_commit_tree = x[1].strip()
    files = read_object(head_commit_tree)
    return files
