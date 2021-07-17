#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import json
from .crawl import Crawl
from utils.crawl import crawl_question_info
import utils.table as table
import utils.constant as constant
from utils.create_catalog import create_catalog

def create_note_content(dir, index, lang: str):
    lang.lower()
    lang[0:1].upper()
    raw_dir = dir
    id, link, title, content, difficulty, acRate, similarQuestions, topics, file_name = crawl_question_info(raw_dir, index)
    dir = constant.dir_dic[dir]

    solving_idea = "### 解题思路"
    complexit_analysis = "### 复杂度分析\n**时间复杂度**：$O()$。\n**空间复杂度**：$O()$。"
    code = "### 解题代码\n```\n```"
    # 构造笔记内容路径
    path = os.path.join(constant.codes_dir, dir, lang, file_name)
    print(lang, path)
    if os.path.exists(path):
        print("code has been existed, open it.  path = {}".format(path))
        return path
    content = '\n'.join([solving_idea, complexit_analysis, code])
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return path

# 题目信息，相似题目，相关topic
def create_note_frame(dir, index):
    raw_dir = dir
    id, link, title, content, difficulty, ac_rate, similar_questions_indexes, topics, file_name = \
        crawl_question_info(raw_dir, index)
    dir = constant.dir_dic[dir]
    # 题目信息
    head = "[Toc]\n## 题目信息\n**题目链接**: {}\n".format(link)
    link_content_data = head + content

    # 相似题目
    similar_questions= "## 相似题目"
    if len(similar_questions_indexes) == 0:
        similar_questions += "\n无"
    else:
        # col_names = ['title | titleSlug | difficulty | translatedTitle']
        col_name = constant.col_name
        sim_catalog = []
        for similar_questions_index in similar_questions_indexes:
            sim_catalog.append(create_catalog(raw_dir, "", similar_questions_index))

        similar_questions_table = table.gen_table(col_name, sim_catalog)
        similar_questions = '\n'.join([similar_questions, similar_questions_table])

    # 相关topic
    related_topics = "## 相关topic"
    if len(topics) == 0:
        related_topics = '\n'.join([related_topics, "无"])
    else:
        # name, slug
        col_name = ["Topic", "Link"]
        topic_catalog = []
        for topic in topics:
            topic_slug = topic["slug"]
            topic_link = link[:len(link) - len(link.split("/")[-1])] + topic_slug
            topic_catalog.append([topic["name"], topic_link])
        topics_table = table.gen_table(col_name, topic_catalog)
        related_topics = '\n'.join([related_topics, topics_table])

    return link_content_data, similar_questions, related_topics, file_name

def get_note_content(dir, index, file_name):
    note_content = []
    for lang in os.listdir(os.path.join(constant.codes_dir, dir)):
        if file_name in os.listdir(os.path.join(constant.codes_dir, dir, lang)):
            code_path = os.path.join(constant.codes_dir, dir, lang, file_name)
            with open(code_path, encoding="utf-8") as f:
                code_data = f.read()
                note_content.append("\n".join(["## {}".format(lang), code_data]))
    return "\n".join(note_content)

def create_note(dir, index):
    raw_dir = dir
    link_content_data, similar_questions, related_topics, file_name = create_note_frame(raw_dir, index)
    dir = constant.dir_dic[dir]
    note_content = get_note_content(dir, index, file_name)
    # 构造笔记文件路径
    path = os.path.join(os.path.abspath(os.path.join(os.getcwd(), "..")), "Notes", dir, file_name)
    print(path)
    if os.path.exists(path):
        print("note has been existed, update it！path = {}".format(path))
    else:
        print("note isn't existed, create it！path = {}".format(path))
    all_data = "\n".join([link_content_data, note_content, similar_questions, related_topics])
    with open(path, 'w', encoding="utf-8") as f:
        f.write(all_data)
    return path

if __name__ == '__main__':
    create()


