import os
from utils.crawl import crawl_question_info
from utils.common import get_index_from_file, get_detail_data
import utils.constant as constant
from utils.crawl_tornado import crawl_question_info_tornado

# 主要用于生成相似题目目录和从文件名生成目录
def create_catalog_tornado(dir, file_names=[], index=""):
    dic = {}
    file_names.sort()
    slugs = []
    for file_name in file_names:
        slugs.append(get_index_from_file(dir, file_name))
    all_question_data = crawl_question_info_tornado(dir, slugs)
    catalog_datas = []
    for i, question_data in enumerate(all_question_data):
        id, link, title, content, difficulty, ac_rate, similar_questions_indexes, topics, file_name = get_detail_data(question_data)

        langs = []
        for lang in os.listdir(os.path.join(constant.codes_dir, dir)):
            if file_name in os.listdir(os.path.join(constant.codes_dir, dir, lang)):
                langs.append("[{}]({})".format(lang, os.path.join(constant.codes_dir, dir, lang, file_name)))
        id_link = "[{}]({})".format(id, link)
        notes_path = os.path.join(constant.notes_dir, dir)
        title = "[{}]({})".format(title, r"../Notes/{}/{}".format(dir, file_name)) if file_name in os.listdir(
            notes_path) else title
        topic_values = []
        for topic in topics:
            topic_values.append(topic["name"])
        catalog_datas.append([id_link, title, difficulty, ",".join(langs), ",".join(topic_values), ac_rate])

    return catalog_datas

    # return [id_link, title, difficulty, ",".join(langs), ",".join(topic_values), ac_rate]



def create_catalog(dir, file_name="", index=""):
    langs = []

    index = get_index_from_file(dir, file_name) if file_name != "" and index == "" else index
    if index == "":
        print("create_catalog: index does not exist!")
    for lang in os.listdir(os.path.join(constant.codes_dir, dir)):
        if file_name in os.listdir(os.path.join(constant.codes_dir, dir, lang)):
            langs.append("[{}]({})".format(lang, os.path.join(constant.codes_dir, dir, lang, file_name)))
    id, link, title, _, difficulty, ac_rate, _, topics, file_name = crawl_question_info(dir, index)
    id_link = "[{}]({})".format(id, link)
    notes_path = os.path.join(constant.notes_dir, dir)
    title = "[{}]({})".format(title, r"../Notes/{}/{}".format(dir, file_name)) if file_name in os.listdir(notes_path) else title
    # print("file_name: ", file_name)
    topic_values = []
    for topic in topics:
        topic_values.append(topic["name"])
    return [id_link, title, difficulty, ",".join(langs), ",".join(topic_values), ac_rate]
