import os
from utils.crawl import crawl_question_info
from utils.common import get_index_from_file


# 主要用于生成相似题目目录和从文件名生成目录
def create_catalog(dir, file_name="", index=""):
    langs = []

    index = get_index_from_file(file_name) if file_name != "" and index == "" else index
    if index == "":
        print("create_catalog: index does not exist!")
    for lang in os.listdir(os.path.join(os.path.join(os.getcwd(), ".."), "Codes")):
        if file_name in os.listdir(os.path.join(os.path.join(os.getcwd(), ".."), "Codes", lang)):
            langs.append(lang)
    id, link, title, _, difficulty, ac_rate, _, topics, file_name = crawl_question_info(dir, index)
    id_link = "[{}]({})".format(id, link)
    notes_path = os.path.join(os.path.join(os.getcwd(), ".."), "Notes")
    title = "[{}]({})".format(title, "../Notes/{}".format(file_name)) if file_name in os.listdir(notes_path) else title
    topic_values = []
    for topic in topics:
        topic_values.append(topic["name"])
    return [id_link, title, difficulty, ",".join(langs), ",".join(topic_values), ac_rate]
