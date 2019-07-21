# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
#
################################################################################

import os
import sys
import re
from decimal import Decimal
import tree

openLib = True
IOS_PRO_PRESENT = ".xcodeproj"

class Parser(object):
    """docstring for Node"""
    def __init__(self):
        super(Parser, self).__init__()
        self.project_file = None
        self.projectSettingContent = None
        self.nodeArray = []
        self.tree = tree.Tree()

    @staticmethod
    def findProjectPath(self):
        projectDir = sys.argv[1]
        for name in os.listdir(projectDir):
            if os.path.splitext(name)[1] == '.xcodeproj':
                filepath = os.path.join(projectDir, name)
                for name_sub in os.listdir(filepath):
                    if name_sub == 'project.pbxproj':
                        self.project_file = os.path.join(
                            filepath, name_sub)
                        break
                        pass
                pass
        pass

    def parseProjectFile(self):
        with open(self.project_file) as f:
            self.projectSettingContent = f.read()
        
        projectPat = re.compile(
            r'/\*\sBegin\sPBXGroup\ssection\s\*/[\s\S]*/\*\sEnd\sPBXGroup\ssection\s\*/')
        rootNamePat = re.compile(r'/\*\s.+\s\*/\s=')
        namePat = re.compile(r'/\*\s.+\s\*/')
        idPat = re.compile(r'[0-9A-Z]+')
        nameIdPat = re.compile(r'[0-9A-Z]+\s/\*\s.+\s\*/')
        propertyPat = re.compile(r'[a-zA-Z]+\s=\s.+;')
        childrenPat = re.compile(r'children\s=\s([\s\S]*)')

        rootItem = re.findall(
            r'[0-9A-Z]+\s=\s{[^{}]*};', projectPat.findall(self.projectSettingContent)[0])[0]

        contentItemArray = re.findall(
            r'[0-9A-Z]+\s/\*\s.+\s\*/\s=\s{[^{}]*};', projectPat.findall(self.projectSettingContent)[0])

        contentItemArray.insert(0, rootItem)
        
        for contentItem in contentItemArray:
            node = tree.TreeNode()
            node.md5 = idPat.findall(contentItem)[0]
            if len(rootNamePat.findall(contentItem)) > 0:

                nameSplit = rootNamePat.findall(contentItem)[0].split(' ')
                if len(nameSplit) > 2:
                    nameSplit.remove('=')
                    nameSplit.pop(0)
                    nameSplit.pop(len(nameSplit) - 1)

                node.filename = " ".join(nameSplit)


                if len(node.filename.split('.')) > 1:
                    node.isLeafNode = true

            for children in nameIdPat.findall(childrenPat.findall(contentItem)[0]):
                childrenNode = tree.TreeNode()
                childrenNode.md5 = idPat.findall(children)[0]
                if len(namePat.findall(contentItem)) > 0:

                    nameSplit = namePat.findall(children)[0].split(' ')
                    if len(nameSplit) > 2:
                        nameSplit.pop(0)
                        nameSplit.pop(len(nameSplit) - 1)

                    childrenNode.filename = " ".join(nameSplit)
                    
                    if len(childrenNode.filename.split('.')) > 1:
                        childrenNode.isLeafNode = True
                node.children.append(childrenNode)
            '''
            插入节点
            '''
            self.tree.insertNode(node)
        pass

        self.tree.generate()
        self.tree.printDesc()

def main():
    """
    main method
    """

if __name__ == '__main__':
    main()
    parser = Parser()
    parser.findProjectPath(parser)
    parser.parseProjectFile()