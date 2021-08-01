#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import subprocess
from typing import List
import re
import utils.constant as constant
import json
from utils.crawl import crawl_question_info
from utils.create_catalog import create_catalog, create_catalog_tornado
from utils.table import gen_table
import time

def gen_data(dir) -> List[List[str]]:
    # generate data from file name in directory

    notes_dir = os.path.join(constant.notes_dir, dir)
    codes_dir = os.path.join(constant.codes_dir, dir)
    note_file_names = os.listdir(notes_dir)
    code_dir_names = os.listdir(codes_dir)  # Go, Python...
    # sort by the question number
    note_file_names.sort()

    lang_code_file_names = {}
    for lang in code_dir_names:
        lang_code_file_names[lang] = os.listdir(os.path.join(codes_dir, lang))
    # data = []
    # start = time.time()
    # for note_file_name in note_file_names:
    #     data.append(create_catalog(dir, note_file_name))
    # end = time.time()
    # print("串行: ", end - start)
    # start = time.time()
    # print(note_file_names)
    data = create_catalog_tornado(dir, file_names=note_file_names, slugs=[])
    end = time.time()
    # print("tornado: ", end - start)
    # print(data)
    return data

def create_readme():
    file_name = "../README.md"
    dirs = constant.dirs
    readme_contents = []
    for dir in dirs:
        # print(gen_table(constant.col_name, gen_data(dir)))
        readme_contents.append("\n".join(["## {}".format(dir), gen_table(constant.col_name, gen_data(dir))]))

    tips = "公式无法渲染的小伙伴，如果用的是Chrome浏览器，可以安装[TexAlltheThings](https: // chrome.google.com / webstore / detail / tex-all-the-things / cbimabofgmfdkicghcadidpemeenbffn)扩展程序，刷新后就能正常显示啦。"

    readme_contents.append(tips)
    with open(file_name, "w", encoding="utf8") as f:
        f.write("\n\n".join(readme_contents))
    path = os.path.join(os.path.join(os.getcwd(), file_name))
    subprocess.Popen([r"/Applications/Typora.app/Contents/MacOS/Typora", path])
    return path


