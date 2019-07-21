# -*- coding: utf-8 -*-	1
################################################################################
#
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
#
################################################################################

"""
安卓代码复用统计
Authors: liyingpeng
Date:    2016 / 11 / 14
"""

import os
import re
from reuse import Reuse
import conf
from decimal import Decimal

COUNTING_FILES = [".java"]
PROJECT_COMMON = ['com/baidu/nuomi/localtrain/views', 'com/baidu/nuomi/localtrain/mgr']

class ReuseAndroid(Reuse):
    def __init__(self, project_dir):
        Reuse.__init__(self)
        self.projectDir = project_dir
        self.project_file = ""
        self.datastring = ""
        self.project_paths = []

    def findProjectFile(self, projectDir):
        self.projectName = projectDir.split('/')[-1]
        for name in os.listdir(projectDir):
            filepath = os.path.join(projectDir, name)
            if not os.path.isdir(filepath):
                if name == "settings.gradle":
                    self.project_file = filepath
        pass

    def parseProjectFile(self):
        with open(self.project_file) as f:
            self.datastring = f.read()

        projectPat = re.compile(r'new\sFile\(rootProject\.projectDir,\s\'(.+)\'\)')
        self.project_paths = projectPat.findall(self.datastring)
        pass

    def reuseRatio(self):
        def isFromCommonkit(filepath):
            if filepath.find(conf.COMMON_ANDROID_PRESENT) != -1 or filepath.find('libraries') != -1:
                return True
            else:
                return False

        for path in self.project_paths:
            path_abs = os.path.join(self.projectDir, path)
            if isFromCommonkit(path_abs):
                count = self.fileUtil.cal_dir(path_abs, COUNTING_FILES)
                self.commonLine += count

        (busi_count, common_count) = self.fileUtil.cal_dir_pro(self.projectDir, COUNTING_FILES, PROJECT_COMMON)
        self.businessLine += busi_count
        self.commonLine += common_count

    def print_info(self):
        self.result += '------------------------------- Android ' \
                       '-------------------------------' + '</br>'
        self.result += '<strong>项目名称：</strong>' + \
                       str(self.projectName) + '</br>'
        self.result += '<strong>占用commonkit代码行数：</strong>' + \
                       str(self.commonLine) + '</br>'
        self.result += '<strong>业务代码行数：</strong>' + \
                       str(self.businessLine) + '</br>'
        self.result += '<strong>代码复用率：</strong>' + \
                       str(Decimal(float(self.commonLine) / (self.businessLine + self.commonLine) * 100).quantize(
                           Decimal('0.00'))) + '%' + '</br>' + '</br>' + '</br>'
        print self.result
        return self.result

    def beginCalculate(self):
        self.findProjectFile(self.projectDir)
        self.parseProjectFile()
        self.reuseRatio()
        pass
