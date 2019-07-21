# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
#
################################################################################

import os
import sys
import conf
from reuse.reuse_ios import ReuseIOS
from reuse.reuse_android import ReuseAndroid
from reuse.reuse_rn import ReuseRN
from util.send_email import send
from decimal import Decimal

PROJECT_DIR = sys.argv[1]
openLib = True


class CodeReuse(object):
    """docstring for Node"""
    def __init__(self):
        super(CodeReuse, self).__init__()
        self.reuses_ios = []
        self.reuses_android = []
        self.reuses_rn = []

    @staticmethod
    def is_ios_pro(project_dir):
        if os.path.isdir(project_dir):
            for name in os.listdir(project_dir):
                filepath = os.path.join(project_dir, name)
                if os.path.isdir(filepath):
                    fileName, fileExtension = os.path.splitext(name)
                    if fileExtension == conf.IOS_PRO_PRESENT:
                        return True
                        break
                        pass
                    pass
            pass
        return False

    @staticmethod
    def is_android_pro(project_dir):
        if os.path.isdir(project_dir):
            for name in os.listdir(project_dir):
                if name == conf.ANDROID_PRO_PRESENT:
                    return True
                    break
                    pass
            return False

    @staticmethod
    def is_rn_pro(project_dir):
        if os.path.isdir(project_dir):
            for name in os.listdir(project_dir):
                if name == conf.RN_PRO_PRESENT:
                    return True
                    break
                    pass
            return False

    def cal_pro(self, project_dir):
        if not os.path.isdir(project_dir):
            return
        if project_dir.find(conf.COMMON_PRESET) != -1:
            return

        if self.is_ios_pro(project_dir):
            self.reuses_ios.append(ReuseIOS(project_dir))
            return
        if self.is_android_pro(project_dir):
            self.reuses_android.append(ReuseAndroid(project_dir))
            return
        if self.is_rn_pro(project_dir):
            self.reuses_rn.append(ReuseRN(project_dir))
            return

        for name in os.listdir(project_dir):
            if name in conf.PASS_FILE_DIR:
                continue
            filepath = os.path.join(project_dir, name)
            self.cal_pro(filepath)

    def begin_cal(self):
        for reuse in self.reuses_ios:
            reuse.beginCalculate()
        for reuse in self.reuses_android:
            reuse.beginCalculate()
        for reuse in self.reuses_rn:
            reuse.beginCalculate()

    def print_result(self):
        result = ""
        totalCommonLine = 0
        totalBusinessLine = 0
        totalCommonLine_all = 0
        totalBusinessLine_all = 0

        for reuse in self.reuses_ios:
            totalCommonLine += reuse.commonLine
            totalBusinessLine += reuse.businessLine
        for reuse in self.reuses_rn:
            totalCommonLine += reuse.commonLine
            totalBusinessLine += reuse.businessLine

        result += '------------------------------------------------------------------' + '</br>'
        result += '<div style="color: red"><strong>iOS总代码复用率为：</strong>' + '</br>'
        result += '<strong>占用commonkit代码行数：</strong>' + str(totalCommonLine) + '</br>'
        result += '<strong>业务代码行数：</strong>' + str(totalBusinessLine) + '</br>'
        result += '<strong>代码复用率：</strong>' + str(Decimal(float(totalCommonLine) / (totalBusinessLine + totalCommonLine) * 100).quantize(Decimal('0.00'))) + '%' + '</br></div>'

        totalBusinessLine_all += totalBusinessLine
        totalCommonLine_all += totalCommonLine

        totalCommonLine = 0
        totalBusinessLine = 0

        for reuse in self.reuses_android:
            totalCommonLine += reuse.commonLine
            totalBusinessLine += reuse.businessLine
        for reuse in self.reuses_rn:
            totalCommonLine += reuse.commonLine
            totalBusinessLine += reuse.businessLine

        result += '------------------------------------------------------------------' + '</br>'
        result += '<div style="color: red"><strong>Android总代码复用率为：</strong>' + '</br>'
        result += '<strong>占用commonkit代码行数：</strong>' + str(totalCommonLine) + '</br>'
        result += '<strong>业务代码行数：</strong>' + str(totalBusinessLine) + '</br>'
        result += '<strong>代码复用率：</strong>' + str(Decimal(float(totalCommonLine) / (totalBusinessLine + totalCommonLine) * 100).quantize(Decimal('0.00'))) + '%' + '</br></div>'


        totalBusinessLine_all += totalBusinessLine
        totalCommonLine_all += totalCommonLine

        result += '------------------------------------------------------------------' + '</br>'
        result += '<div style="color: red"><strong>iOS + Android 总代码复用率为：</strong>' + '</br>'
        result += '<strong>占用commonkit代码行数：</strong>' + str(totalCommonLine_all) + '</br>'
        result += '<strong>业务代码行数：</strong>' + str(totalBusinessLine_all) + '</br>'
        result += '<strong>代码复用率：</strong>' + str(
        Decimal(float(totalCommonLine_all) / (totalBusinessLine_all + totalCommonLine_all) * 100).quantize(
                Decimal('0.00'))) + '%' + '</br></div>'

        for reuse in self.reuses_ios:
            result += reuse.print_info()
        for reuse in self.reuses_android:
            result += reuse.print_info()
        for reuse in self.reuses_rn:
            result += reuse.print_info()

        send(result)


def main():
    """
    main method
    """

    reuse = CodeReuse()
    reuse.cal_pro(PROJECT_DIR)
    reuse.begin_cal()
    reuse.print_result()


if __name__ == '__main__':
    main()
