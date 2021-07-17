#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import re
import time
from typing import List

import numpy as np
import requests
from bs4 import BeautifulSoup
from crawl import Crawl
import re
import constant
import json
leetcode_problems_addr_prefix = r"https://leetcode.com/problems/"
# password next time change to command line input 
username = r"940015925@qq.com"

# TODO:: generate data from file name in directory
def gen_data(dir) -> List[List[str]]:
    dir = dir.strip()
    data = []
    print(dir)
    assert dir in constant.dir_dic.keys()
    crawler = Crawl(constant.is_en[dir])
    dir = constant.dir_dic[dir]
    dir = r"../../{}".format(dir)
    file_names = os.listdir(dir)

    # sort by the question number

    file_names.sort()
    # Crawl.login(username=username, password = password)
    # file name is in English，and has the question number
    for file_name in file_names:
        # Language needs to get from my file. Document analysis..
        path = os.path.join(dir, file_name)
        language = []
        index = ""
        print(file_name)
        with open(path, 'r', encoding = 'utf8') as f:
            note_data = f.read()
            pos = re.search("https://.+.com/problems/.+\s", note_data).span()
            print(pos)
            addr_split = note_data[pos[0]: pos[1]].strip().replace("\n", "").split("/")
            print(addr_split)
            index = addr_split[-1] if addr_split[-1] != "" else addr_split[-2]
            print(index)
            langs = ["Go", "Python", "Java", "C++"]
            for lang in langs:
                if lang in note_data or lang.lower() in note_data:
                    language.append(lang)
        if len(language) == 0:
            raise Exception("note中未能解析到language信息")

        id, slug = crawler.get_id_slug(index)
        # print(id, type(id), slug)
        link = crawler.url_base + r'/problems/' + slug
        question_all_data = crawler.get_problem_by_slug(slug)
        # analyze data
        title = question_all_data["questionTitle"]
        if dir != "Leetcode":
            title = " ".join(title.split()[:-1])
        content = question_all_data['content']
        difficulty = question_all_data["difficulty"]

        acRate = json.loads(question_all_data["stats"])["acRate"]
        similarQuestions = json.loads(question_all_data["similarQuestions"])
        topics = question_all_data["topicTags"]
        topic_values = []
        for topic in topics:
            topic_values.append(list(topic.values())[0])
        title_link = "[{}]({})".format(title, link)
        print()
        tmp_data = [str(id), title_link, difficulty, ",".join(language), ",".join(topic_values), str(acRate)]
        data.append(tmp_data)

    return data

# check title_link can get md file correctly through compare links in md with question's addr in leetcode web
# TODO:: do not think clearly, wait 
# def check_link_available(data, dir) -> bool:
#     for tmp_data in data:
#         title_link = tmp_data[1]
#         # "[Two Sum](https://leetcode.com/problems/two sum/)" -> "two sum"
#         title_lower = re.match('\[.*\]', title).group(0)[1:-1].lower()
#         # "two sum" -> "https://leetcode.com/problems/two-sum"
#         question_addr = leetcode_problems_addr_prefix + '-'.join(title_lower.split(' '))


# generate table(catalog) based on column name and data  
def gen_table(cols_name, data) -> str:
    """
    Params:
        cols_name: {list[str]} ， such as "Question Number| Title | Link | Language | Topic".
        data: {list[list[str]]}
    
    Returns:
        table: {str}
    """

    ## all lines include head, dividing line and data 
    lines = []
    ## head
    first_line = ""
    first_line += "| {} |".format(' | '.join(cols_name))
    lines += [first_line]
    # print('1', lines)
    ## dividing line, such as '| :------: | :---------------: | :-----: | :-----: | :--------: | :-----: |'
    SPLIT = ":{}:"
    dividing_line = ""
    for i in range(len(cols_name)):
        dividing_line = "{} {} |".format(dividing_line, SPLIT.format('-'*len(cols_name[i])))
    lines += [dividing_line]
    # print('2', lines)

    ## data
    for i in range(len(data)):
        tmp_line = "| {} |".format(' | '.join(data[i]))
        lines += [tmp_line]
    # print('3', lines)
    
    table = '\n'.join(lines)
    return table


def createREADME(data: str) -> None:
    """
    Params:
        data: {str} ， README's content.
    
    Returns:
        table: None
    """
    with open("TEST.md", 'w', encoding='utf8') as f:
        f.write(data)
    return 

 
if __name__ == '__main__':
    # id, title_link, difficulty, language, topic_values, acRate
    cols_name = ["Question id", "Title", "Level", "Language", "Topic", "AcRate"]
    dirs = ["lc", "lcci", "lcof"]
    for dir in dirs:
        data = gen_data(dir)
        print(gen_table(cols_name, data))
    # table = gen_catalogs(cols_name, data)
    # top = r'/Users/mac/Desktop/'
    # print(table)
    # createREADME(table)
    # 将table写入md文件
