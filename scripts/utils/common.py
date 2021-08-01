import os
import re


def get_index_from_file(dir, file_name):
    file_path = "../Notes/{}/{}".format(dir, file_name)
    # print(file_path)
    try:
        with open(file_path, 'r', encoding='utf8') as f:
            note_data = f.read()
            pos = re.search("https://.+.com/problems/.+\s", note_data).span()
            addr_split = note_data[pos[0]: pos[1]].strip().replace("\n", "").split("/")
            index = addr_split[-1] if addr_split[-1] != "" else addr_split[-2]
    except:
        print("{} does not exist!".format(file_path))
    return index

def get_detail_data(question_data):
    id = question_data[0]
    link = question_data[1]
    title = question_data[2]
    content = question_data[3]
    difficulty = question_data[4]
    ac_rate = question_data[5]
    similar_questions_indexes = question_data[6]
    topics = question_data[7]
    file_name = question_data[8]
    return [id, link, title, content, difficulty, ac_rate, similar_questions_indexes, topics, file_name]
