import json
import time
import utils.constant as constant
from tornado.gen import coroutine
from tornado import gen
from tornado.ioloop import IOLoop
from tornado.httpclient import AsyncHTTPClient, HTTPError
from tornado.httpclient import HTTPRequest
import queue
from typing import List
import urllib
#urls与前面相同

HEADERS = {'Content-Type': 'application/json'}
class Crawler(object):

    def __init__(self, dir="lc"):
        self.user_agent = r'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
        self.http = AsyncHTTPClient()
        self.post_api_url = constant.post_api[dir]
        self.get_api_url = constant.get_api[dir]
        self.dir = dir
        self.queue = queue.Queue()

    @coroutine
    def get(self, titles: List[str]):
        request = HTTPRequest(url=self.get_api_url,
                              method="GET",
                              headers=HEADERS,
                              connect_timeout=10.0,
                              request_timeout=10.0,
                              user_agent=self.user_agent)


        response = yield self.http.fetch(request, raise_error=False)
        slugs = []
        if response.code == 200:
            slugs = yield self.resolve_slugs(json.loads(response.body), titles)
        else:
            print("get error, http_error_code = {}, slug = {}".format(response.code, titles))
        # raise gen.Return(response)
        return slugs

    @coroutine
    def post(self, slug):
        post_data = {'operationName': "getQuestionDetail",
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
                            translatedContent
                        }
                    }'''
                     }
        post_data = json.dumps(post_data)
        request = HTTPRequest(url=self.post_api_url,
                              method='POST',
                              headers=HEADERS,
                              connect_timeout=10.0,
                              request_timeout=10.0,
                              user_agent=self.user_agent,
                              body=post_data)


        response = yield self.http.fetch(request, raise_error=False)
        if response.code == 200:
            question_info = yield self.resolve_question_info(json.loads(response.body))
            self.queue.put(question_info)
        else:
            print("post error, http_error_code = {}, slug = {}".format(response.code, slug))
        raise gen.Return(response)

        # yield self.http.fetch(request, callback=self.find, raise_error=False)
    @coroutine
    def resolve_question_info(self, question_all_data):
        question_all_data = question_all_data['data']['question']
        id = question_all_data["questionFrontendId"]
        slug = question_all_data["questionTitleSlug"]
        title = question_all_data["questionTitle"]

        # 方便排序
        if self.post_api_url != "https://leetcode.com/graphql":
            title = " ".join(title.split()[:-1])
        else:
            id = "0"*(4-len(id)) + id

        link = constant.url_base[self.dir] + r'/problems/' + slug
        content = question_all_data['content']
        if self.dir not in ["lc", "Leetcode"]:
            content = question_all_data['translatedContent']
        difficulty = question_all_data["difficulty"]
        ac_rate = json.loads(question_all_data["stats"])["acRate"]
        similarQuestions = json.loads(question_all_data["similarQuestions"])
        topics = question_all_data["topicTags"]
        similar_questions_indexes = []
        for similarQuestion in similarQuestions:
            similar_questions_indexes.append(list(similarQuestion.values())[0])
        file_name = ".".join([str(id), title, "md"])

        return [id, link, title, content, difficulty, ac_rate, similar_questions_indexes, topics, file_name]
    @coroutine
    def resolve_slugs(self, question_list, titles):
        slugs = []
        for title in titles:
            if self.dir in ["lcci", "程序员面试金典"]:
                title += " LCCI"
            elif self.dir in ["lcof", "剑指offer"]:
                title += " LCOF"
            for question in question_list['stat_status_pairs']:
                # 题目编号
                question_id = question['stat']['frontend_question_id']
                question_title = question['stat']['question__title']
                question_slug = question['stat']['question__title_slug']
                # print(question_id, question_title, "\n")
                if str(title) in [str(question_id).strip(), str(question_title).strip(), str(question_slug).strip()]:
                    slugs.append(question['stat']['question__title_slug'])
                    break
        if len(slugs) == 0:
            print("can not get slug by these titles: {}".format(titles))
        return slugs




class Question_info(object):

    def __init__(self, dir, slugs):
        self.crawler = Crawler(dir)
        self.slugs = slugs
    @coroutine
    def get_question_info(self):
        # print(u'基于tornado的并发抓取')
        starttime = time.time()
        yield [self.crawler.post(slug) for slug in self.slugs]
        endtime=time.time()
        # print("get question info, time={}".format(endtime - starttime))
        all_question_info = []
        while not self.crawler.queue.empty():
            all_question_info.append(self.crawler.queue.get())
        all_question_info.sort(key=lambda x: x[0])
        return all_question_info
    # @coroutine
    # def resolve(self):
class All_question_data(object):
    def __init__(self, dir, titles):
        self.dir = dir
        self.crawler = Crawler(dir)
        self.titles = titles
    @coroutine
    def get_slugs(self):
        starttime = time.time()
        slugs = yield self.crawler.get(self.titles)
        endtime=time.time()
        # print("get all question info, time={}, dir={}".format(endtime-starttime, self.dir))
        return slugs

def crawl_question_info_tornado(dir, slugs):
    question_info = Question_info(dir, slugs)
    loop = IOLoop.current()
    return loop.run_sync(question_info.get_question_info)
def crawl_slugs(dir, titles):
    all_question_data = All_question_data(dir, titles)
    loop = IOLoop.current()
    return loop.run_sync(all_question_data.get_slugs)


if __name__ == '__main__':
    question_info = Question_info("lc", slugs)
    loop = IOLoop.current()
    loop.run_sync(question_info.get_question_info)

