# -*- coding: utf-8 -*-	1
################################################################################
#
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
#
################################################################################

"""
iOS代码复用统计
Authors: liyingpeng
Date:    2016 / 11 / 14
"""

import os
import re
import util.tree as tree
from reuse import Reuse
from decimal import Decimal


class ReuseIOS(Reuse):
    def __init__(self, projectDir):
        Reuse.__init__(self)
        self.projectDir = projectDir
        self.tree = tree.Tree()

        self.calculateFileDirs = ['.h', '.m', '.c', '.swift', 'js']
        self.project_file = None
        self.commonDir = None
        self.nodeArray = []
        self.datastring = ''
        self.calculatLib = True

    def findProjectFile(self, projectDir):
        for name in os.listdir(projectDir):
            filepath = os.path.join(projectDir, name)
            if os.path.isdir(filepath):
                fileName, fileExtension = os.path.splitext(name)
                if fileExtension == '.xcodeproj':
                    self.commonDir = os.path.join(os.path.join(
                        projectDir, os.path.pardir), os.path.pardir)
                    self.projectName = fileName
                    for name_sub in os.listdir(filepath):
                        if name_sub == 'project.pbxproj':
                            self.project_file = os.path.join(
                                filepath, name_sub)
                            break
                            pass
                    pass
                pass
        pass

    def parseProjectFile(self):
        with open(self.project_file) as f:
            self.datastring = f.read()

        projectPat = re.compile(
            r'/\*\sBegin\sPBXGroup\ssection\s\*/[\s\S]*/\*\sEnd\sPBXGroup\ssection\s\*/')
        namePat = re.compile(r'/\*\s.+\s\*/')
        idPat = re.compile(r'[0-9A-Z]+')
        nameIdPat = re.compile(r'[0-9A-Z]+\s/\*\s.+\s\*/')
        propertyPat = re.compile(r'[a-zA-Z]+\s=\s.+;')
        childrenPat = re.compile(r'children\s=\s([\s\S]*)')

        contentString = re.findall(
            r'[0-9A-Z]+\s/\*\s.+\s\*/\s=\s{[^{}]*}', projectPat.findall(self.datastring)[0])
        # print len(contentString)
        # print contentString
        for contentItem in contentString:
            # print contentItem
            node = Node()
            node.id = idPat.findall(contentItem)[0]
            node.filename = namePat.findall(contentItem)[0].split(' ')[1]
            for propertyString in propertyPat.findall(contentItem):
                propertyName = propertyString.split(' ')[0]
                propertyValue = propertyString.split(
                    ' ')[2].lstrip('"').rstrip('";')
                setattr(node, propertyName, propertyValue)
            for children in nameIdPat.findall(childrenPat.findall(contentItem)[0]):
                childrenNode = Node()
                childrenNode.id = idPat.findall(children)[0]
                childrenNode.filename = namePat.findall(children)[
                    0].split(' ')[1]
                node.children.append(childrenNode)
            # print node.__dict__
            self.nodeArray.append(node)
        # print len(self.nodeArray)
        pass

    def constructTree(self):
        for node in self.nodeArray:
            self.tree.insertElement(node)
        # print len(self.tree.treeArray)
        # for tNode in self.tree.treeArray:
        #     if not tNode.parent:
        #         print tNode.data.id
        #         pass
            # if not len(tNode.children):
            #     print tNode.data.id
            #     pass
        pass

    def reuseRatio(self):
        def isFromCommonkit(filepath):
            if filepath.find('commonkit-ios') == -1:
                return False
                pass
            else:
                return True

        def dealWithCommonPath(path):
            return path[(path.find('commonkit-ios')):]
            pass

        for tNode in self.tree.treeArray:
            if not tNode.passed:
                if tNode.data.path == '':
                    continue
                    pass
                '''
                寻找节点的所有上级路径，拼接成路径串headpath
                '''
                nodeFilePath = ''
                headPath = ''
                path = tNode.data.path
                if isFromCommonkit(path):
                    headPath = dealWithCommonPath(path)
                    pass
                else:
                    nodeFilePath = path
                    pass

                node = tNode
                while node.parent:
                    node = node.parent
                    if isFromCommonkit(node.data.path):
                        headPath = dealWithCommonPath(
                            node.data.path) + '/' + nodeFilePath
                        break
                        pass
                    nodeFilePath = node.data.path + '/' + nodeFilePath
                    pass

                if headPath == '':
                    headPath = nodeFilePath
                    pass

                headPath_abs = ''
                if headPath.find('commonkit-ios') != -1:
                    headPath_abs = os.path.join(self.commonDir, headPath)
                    pass
                else:
                    headPath_abs = os.path.join(self.projectDir, headPath)

                '''
                根据上层路径串遍历所有的子节点，并且标记为pass
                '''
                '''
                深度优先遍历节点（后续遍历）
                '''
                if len(tNode.children) == len(tNode.data.children):
                    continue
                    pass

                for node in tNode.data.children:
                    isFileNode = True
                    for tNode in tNode.children:
                        if node.id == tNode.data.id:
                            isFileNode = False
                            break
                            pass
                    '''
                    如果是叶子节点才是需要计算行数的文件
                    '''
                    if isFileNode:
                        fn = node.filename
                        fileName, fileExtension = os.path.splitext(fn)
                        if fileExtension in self.calculateFileDirs:
                            filepath_abs = os.path.join(headPath_abs, fn)
                            if filepath_abs.find('commonkit-ios/Lib') != -1 and not self.calculatLib:
                                continue
                                pass
                            try:
                                linecount = self.fileUtil.calculate(
                                    filepath_abs)
                                pass
                            except Exception:
                                continue
                                raise

                            if filepath_abs.find('commonkit-ios') != -1\
                                    or filepath_abs.find('CustomViews') != -1 \
                                    or filepath_abs.find('ViewController/Base') != -1 \
                                    or filepath_abs.find('Utility') != -1 \
                                    or filepath_abs.find('PanguCommon') != -1:
                                self.commonLine += linecount
                                pass
                            else:
                                self.businessLine += linecount
                                pass
                            # print filepath_abs
                            pass
                        pass

            pass

    def print_info(self):
        self.result += '--------------------------------- iOS ' \
                       '---------------------------------' + '</br>'
        self.result += '<strong>项目名称：</strong>' + \
                       str(self.projectName) + '-ios' + '</br>'
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
        self.constructTree()
        self.reuseRatio()
        pass


class Node(object):
    """docstring for Node"""

    def __init__(self):
        super(Node, self).__init__()
        self.id = ''
        self.isa = ''
        self.filename = ''
        self.children = []
        self.path = ''
        self.sourceTree = ''
