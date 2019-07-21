# -*- coding: utf-8 -*-	1
################################################################################
#
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
#
################################################################################

"""
代码复用统计基类
Authors: liyingpeng
Date:    2016 / 11 / 14
"""

from util.line_cal import LineCalculate


class Reuse(object):
    """
    顶层基类
    """

    def __init__(self):
        self.projectName = ''
        self.commonLine = 0
        self.businessLine = 0
        self.result = ''
        self.fileUtil = LineCalculate()

    def findProjectFile(self):
        return None

    def reuseRatio(self):
        return None

    def beginCalculate(self):
        return None