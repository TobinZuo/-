#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from utils.create_readme import create_readme
from utils.create_note import create_notes
import time

if __name__ == "__main__":
    start = time.time()
    create_notes()
    print("更新所有笔记内容：", time.time() - start)

    start = time.time()
    create_readme()
    print("生成README：", time.time() - start)




