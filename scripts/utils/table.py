#!/usr/bin/env python3
# -*- coding:utf-8 -*-
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
    first_line += ' | '.join(cols_name)
    lines += [first_line]
    # print('1', lines)
    ## dividing line, such as ' :------: | :---------------: | :-----: | :-----: | :--------: | :-----: '
    SPLIT = ":{}:"
    dividing_line = ""
    tmp = []
    for i in range(len(cols_name)):
        tmp.append(SPLIT.format('-' * len(cols_name[i])))
    dividing_line = '|'.join(tmp)
    lines += [dividing_line]
    # print('2', lines)

    ## data
    for i in range(len(data)):
        for index, j in enumerate(data[i]):
            if j is None:
                data[i][index] = "None"
        tmp_line = ' | '.join(data[i])
        lines += [tmp_line]
    # print('3', lines)

    table = '\n'.join(lines)
    return table