#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# import linecache
# import sys

# http://wangwei007.blog.51cto.com/68019/1242317

# filepath = sys.argv[1]

# count = len(open(filepath, 'rU').readlines())

# 处理大文件
# count = -1
# for count, line in enumerate(open(filepath, 'rU')):
#     pass
# count += 1

# 处理大文件
# count = 0
# thefile = open(filepath, 'rb')
# while True:
#     buffer = thefile.read(8192 * 1024)
#     if not buffer:
#         break
#     count += buffer.count('\n')
# thefile.close()

# print count

import os
from util.stack import Stack
import conf

class LineCalculate(object):
    """docstring for LineCalculte"""

    def __init__(self):
        super(LineCalculate, self).__init__()

    def calculate(self, filePath):
        # return len(open(filePath, 'rU').readlines())
        # 处理大文件
        count = 0
        thefile = open(filePath, 'rb')
        while True:
            buffer = thefile.read(8192 * 1024)
            if not buffer:
                break
            count += buffer.count('\n')
        thefile.close()
        return count

    def cal_dir(self, file_dir, cal_files):
        count = 0
        dir_stack = Stack()

        """
        广度优先遍历文件列表
        """
        if os.path.isdir(file_dir):
            dir_stack.push(file_dir)
            while dir_stack.length() > 0:
                curr_dir = dir_stack.pop()
                for name in os.listdir(curr_dir):
                    if name in conf.PASS_FILE_DIR:
                        continue
                    filepath = os.path.join(curr_dir, name)
                    if os.path.isdir(filepath):
                        dir_stack.push(filepath)
                    else:
                        fileName, fileExtension = os.path.splitext(name)
                        if fileExtension in cal_files:
                            count += self.calculate(filepath)
        else:
            fileName, fileExtension = os.path.splitext(file_dir)
            if fileExtension in cal_files:
                count += self.calculate(file_dir)

        return count

    def cal_dir_pro(self, file_dir, cal_files, project_common):
        common_count = 0
        busi_count = 0
        dir_stack = Stack()

        """
        广度优先遍历文件列表
        """
        if os.path.isdir(file_dir):
            dir_stack.push(file_dir)
            while dir_stack.length() > 0:
                curr_dir = dir_stack.pop()
                for name in os.listdir(curr_dir):
                    if name in conf.PASS_FILE_DIR:
                        continue
                    filepath = os.path.join(curr_dir, name)
                    if os.path.isdir(filepath):
                        dir_stack.push(filepath)
                    else:
                        fileName, fileExtension = os.path.splitext(name)
                        if fileExtension in cal_files:
                            iscommon = False
                            for common in project_common:
                                if filepath.find(common) != -1:
                                    iscommon = True
                            if iscommon:
                                common_count += self.calculate(filepath)
                            else:
                                busi_count += self.calculate(filepath)
        else:
            fileName, fileExtension = os.path.splitext(file_dir)
            if fileExtension in cal_files:
                iscommon = False
                for common in project_common:
                    if file_dir.find(common) != -1:
                        iscommon = True
                if iscommon:
                    common_count += self.calculate(file_dir)
                else:
                    busi_count += self.calculate(file_dir)

        return (busi_count, common_count)
