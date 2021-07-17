#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# crawel leetcode data, such as questionId, topic, content et.
# most codes copied from https://gcyml.github.io/2019/03/03/Python%E7%88%AC%E5%8F%96Leetcode%E9%A2%98%E7%9B%AE%E5%8F%8AAC%E4%BB%A3%E7%A0%81/
import requests, json
from requests_toolbelt import MultipartEncoder
import utils.constant as constant

# simulate login
class Crawl:
    def __init__(self, is_en=True):
        self.session = requests.Session()
        self.user_agent = r'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
        self.is_en = is_en
        if is_en:
            self.url_base = r'https://leetcode.com'
        else:
            self.url_base = r'https://leetcode-cn.com'

    def login(self, username, password):

        # cookies = crawler.session.get(url).cookies

        # for cookie in cookies:
        #     if cookie.name == 'csrftoken':
        #         csrftoken = cookie.value

        url = self.url_base + r"/accounts/login"

        #  because leetcode-cn do not use csrftoken, I deprecate it.
        params_data = {
            # 'csrfmiddlewaretoken': csrftoken,
            'login': username,
            'password': password,
            'next': 'problems'
        }
        headers = {'User-Agent': self.user_agent, 'Connection': 'keep-alive', 'Referer': url,
                   "origin": self.url_base}
        m = MultipartEncoder(params_data)

        headers['Content-Type'] = m.content_type
        self.session.post(url, headers=headers, data=m, timeout=10, allow_redirects=False)
        is_login = self.session.cookies.get('LEETCODE_SESSION') != None
        return is_login

    # get all question data
    def get_problems(self):
        if self.is_en:
            url = r"https://leetcode.com/api/problems/all"
        else:
            url = r"https://leetcode-cn.com/api/problems/all"

        headers = {'User-Agent': self.user_agent, 'Connection': 'keep-alive'}
        resp = self.session.get(url, headers=headers, timeout=10)

        question_list = json.loads(resp.content.decode('utf-8'))

        for question in question_list['stat_status_pairs']:
            # 题目编号
            question_id = question['stat']['question_id']
            # 题目名称
            question_slug = question['stat']['question__title_slug']
            # 题目状态
            question_status = question['status']

            # 题目难度级别，1 为简单，2 为中等，3 为困难
            level = question['difficulty']['level']

            # 是否为付费题目
            if question['paid_only']:
                continue

    # import requests,json

    # session = requests.Session()
    # # my inc mac 
    # user_agent = r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
    # get one specific question data
    def get_problem_by_slug(self, slug):
        print("slug: ", slug)
        if self.is_en:
            url = r"https://leetcode.com/graphql"
        else:
            url = r"https://leetcode-cn.com/graphql"

        params = {'operationName': "getQuestionDetail",
                  'variables': {'titleSlug': slug},
                  'query': '''query getQuestionDetail($titleSlug: String!) {
                question(titleSlug: $titleSlug) {
                    questionId
                    questionFrontendId
                    questionTitle
                    questionTitleSlug
                    content
                    difficulty
                    stats
                    similarQuestions
                    categoryTitle
                    topicTags {
                            name
                            slug
                    }
                }
            }'''
                  }

        json_data = json.dumps(params).encode('utf8')

        headers = {'User-Agent': self.user_agent, 'Connection':
                   'keep-alive', 'Content-Type': 'application/json',
                   'Referer': self.url_base + r'/problems' + slug}
        resp = self.session.post(url, data=json_data, headers=headers, timeout=10)
        content = resp.json()
        # print(content)
        # 题目详细信息
        question_all_data = content['data']['question']
        # print(question)

        return question_all_data

    # input is index. for LCOF , LCCI of else , index is only question title(english title, login leetcode to check it, for leetcode, index can represent question_number.
    def get_id_slug(self, index: str):
        if self.is_en:
            url = r"https://leetcode.com/api/problems/all"
        else:
            url = r"https://leetcode-cn.com/api/problems/all"

        headers = {'User-Agent': self.user_agent, 'Connection': 'keep-alive'}
        resp = self.session.get(url, headers=headers, timeout=10)
        question_list = json.loads(resp.content.decode('utf-8'))

        slug = ""
        id = ""
        for question in question_list['stat_status_pairs']:
            # 题目编号
            question_id = question['stat']['frontend_question_id']
            question_title = question['stat']['question__title']
            question_slug = question['stat']['question__title_slug']
            # print(question_id, question_title, "\n")

            if str(index) in [str(question_id).strip(), str(question_title).strip(), str(question_slug).strip()]:
                slug = question['stat']['question__title_slug']
                id = question_id
                break
        if slug == "":
            print("can not get slug by this index: {}".format(index))
        return str(id), slug
    def get_all_info(self, dir, index):
        id, slug = self.get_id_slug(index)
        link = self.url_base + r'/problems/' + slug
        question_all_data = self.get_problem_by_slug(slug)
        # analyze data
        title = question_all_data["questionTitle"]
        if dir != "lc":
            title = " ".join(title.split()[:-1])
        else:
            id = "0"*(4-len(id)) + id
        print("title==========", title)

        print("id=========", id)
        content = question_all_data['content']
        difficulty = question_all_data["difficulty"]
        ac_rate = json.loads(question_all_data["stats"])["acRate"]
        similarQuestions = json.loads(question_all_data["similarQuestions"])
        topics = question_all_data["topicTags"]
        # topic_values = []
        # for topic in topics:
        #     topic_values.append(list(topic.values())[0])
        similar_questions_indexes = []
        for similarQuestion in similarQuestions:
            similar_questions_indexes.append(list(similarQuestion.values())[0])
        file_name = ".".join([str(id), title, "md"])

        return id, link, title, content, difficulty, ac_rate, similar_questions_indexes, topics, file_name


def crawl_question_info(dir, index):
    dir, index = str(dir).strip(), str(index).strip()
    assert dir in constant.dir_dic.keys()
    crawler = Crawl(constant.is_en[dir])
    return crawler.get_all_info(dir, index)

if __name__ == "__main__":
    print(crawl_question_info("lc", "11")[1])