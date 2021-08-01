#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import subprocess
from utils.create_note import *
import click

# python code.py -d lcof -l Python -s
# python code.py -d lc -l Python -s two-sum
# python code.py -d lcci -l Python -s
@click.command()
@click.option("-d", "--dir", type=click.Choice(["lc", "lcci", "lcof"]), help="Leetcode, 程序员面试金典, 剑指offer")
@click.option("-l", "--lang", type=click.Choice(["Python", "Go"]), help="编程语言")
@click.option("-s", "--slug", default="", help="题目链接最后面的一段")

def create_note_content_by_lang(dir, lang, slug):
    path = create_note_content(dir, slug, lang)
    subprocess.Popen([r"/Applications/Typora.app/Contents/MacOS/Typora", path])
    return path

if __name__ == "__main__":
    create_note_content_by_lang()



