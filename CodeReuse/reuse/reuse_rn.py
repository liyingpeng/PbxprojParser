# -*- coding: utf-8 -*-	1
################################################################################
#
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
#
################################################################################

"""
React Native 代码复用统计
Authors: liyingpeng
Date:    2016 / 11 / 14
"""
import os
import re
from reuse import Reuse

COUNTING_FILES = [".js"]


class ReuseRN(Reuse):
    def __init__(self, project_dir):
        Reuse.__init__(self)
        self.projectDir = project_dir
        self.project_file = ""
        self.datastring = ""
        self.project_paths = []

    def findProjectFile(self, projectDir):
        for name in os.listdir(projectDir):
            filepath = os.path.join(projectDir, name)
            if not os.path.isdir(filepath):
                if name == "package.json":
                    with open(filepath) as f:
                        content = f.read()
                        self.projectName = re.compile(r'"name":\s"(.+)"').findall(content)[0]
        pass

    def reuseRatio(self):
        self.businessLine = self.fileUtil.cal_dir(self.projectDir, COUNTING_FILES)
        self.commonLine = self.businessLine

    def print_info(self):
        self.result += '------------------------------ ReactNative ' \
                       '------------------------------' + '</br>'
        self.result += '<strong>项目名称：</strong>' + \
                       str(self.projectName) + '</br>'
        self.result += '<strong>占用commonkit代码行数：</strong>' + \
                       str(self.commonLine) + '</br>'
        self.result += '<strong>业务代码行数：</strong>' + \
                       str(self.businessLine) + '</br>'
        self.result += '<strong>代码复用率：</strong>' + \
                       "100%" + '</br>' + '</br>' + '</br>'
        print self.result
        return self.result

    def beginCalculate(self):
        self.findProjectFile(self.projectDir)
        self.reuseRatio()
        pass