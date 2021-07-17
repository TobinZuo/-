#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys 
import os
import getopt
import subprocess
from utils.create_note import create_note
def usage():
    print("python test.py -t <dir> -n <index>\nindex can be question_title or question_number but question_number is only use in leetcode")
    print("for example:\n   python main.py -d lc -i 123\n")
    print("   python main.py -d lcci -i Sparse Similarity LCCI\n")
    print("   python main.py -d lcof -i 二叉树的最近公共祖先 LCOF\n")


def get_dir_index(args):
    dir, index = "", "" # if question_number is in Roman, how to fix
    try:
        optlist, args = getopt.getopt(args, "hd:i:", ["help", "dir=", "index="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    #print(optlist, args)
    for o, a in optlist:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("--dir", "-d"):
            dir = a
        elif o in ("--index", "-i"):
            index = a
        else:
            assert False, "unhandled option"
    return dir, index, args

if __name__ == "__main__":
    args = sys.argv[1:]
    dir, index, args = get_dir_index(args)
    index = " ".join([index.strip()] + args)
    # get template path
    path = create_template(dir, index)
    # use Typora open this template
    subprocess.Popen([r"/Applications/Typora.app/Contents/MacOS/Typora", path])
    # subprocess.Popen(["/Users/admin/Downloads/Visual Studio Code.app/Contents/MacOS/Electron", path])

    

