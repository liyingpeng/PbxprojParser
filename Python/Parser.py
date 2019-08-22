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

    def parseProjectFile(self):
        with open(self.project_file) as f:
            self.projectSettingContent = f.read()
        
        projectPat = re.compile(
            r'/\*\sBegin\sPBXGroup\ssection\s\*/[\s\S]*/\*\sEnd\sPBXGroup\ssection\s\*/')
            # /* Begin PBXGroup section */
            # /* End PBXGroup section */
        rootNamePat = re.compile(r'/\*\s.+\s\*/\s=') 
            # 9C4A634822E4828700037752 /* Products */ = {
        namePat = re.compile(r'/\*\s.+\s\*/') 
            # /* TestForProjectParser.app */
        nameIdPat = re.compile(r'[0-9A-Z]+\s/\*\s.+\s\*/') 
            # 9C4A634722E4828700037752 /* TestForProjectParser.app */,
        idPat = re.compile(r'[0-9A-Z]+') 
            # 9C4A634822E4828700037752
        childrenPat = re.compile(r'children\s=\s([\s\S]*)')
            # children = (
			# 	9C4A634722E4828700037752 /* TestForProjectParser.app */,
			# 	9C4A635F22E4828800037752 /* TestForProjectParserTests.xctest */,
			# 	9C4A636A22E4828800037752 /* TestForProjectParserUITests.xctest */,
			# );

        rootItem = re.findall(
            r'[0-9A-Z]+\s=\s{[^{}]*};', projectPat.findall(self.projectSettingContent)[0])[0]

        contentItemArray = re.findall(
            r'[0-9A-Z]+\s/\*\s.+\s\*/\s=\s{[^{}]*};', projectPat.findall(self.projectSettingContent)[0])

        contentItemArray.insert(0, rootItem) # 插入根节点
        
        for contentItem in contentItemArray:
            node = tree.TreeNode()
            node.md5 = idPat.findall(contentItem)[0]
            if len(rootNamePat.findall(contentItem)) > 0:
                nameSplit = rootNamePat.findall(contentItem)[0].split(' ')
                node.filename = nameSplit[1]

                if len(node.filename.split('.')) > 1:
                    node.isLeafNode = True

            for children in nameIdPat.findall(childrenPat.findall(contentItem)[0]):
                childrenNode = self.nodeWithNameIDString(children)
                node.children.append(childrenNode)
            '''
            插入节点
            '''
            self.tree.insertNode(node)
        pass

        self.tree.generate()
        # self.tree.printDesc()

    def nodeWithNameIDString(self, nameIdString):
        idPat = re.compile(r'[0-9A-Z]+') 
        namePat = re.compile(r'/\*\s.+\s\*/')
        node = tree.TreeNode()
        node.md5 = idPat.findall(nameIdString)[0]
        if len(namePat.findall(nameIdString)) > 0:
            nameSplit = namePat.findall(nameIdString)[0].split(' ')
            node.filename = nameSplit[1]
            if len(node.filename.split('.')) > 1:
                node.isLeafNode = True
        return node

    def resolveConflict(self):
        conflictPat = re.compile(r'<<<<<<<[^<]*>>>>>>>\s[0-9A-Za-z-_]*')
        conflictList = conflictPat.findall(self.projectSettingContent)
        for conflict in conflictList:
            print "------------------------ deal with ------------------------"
            print conflict
            nameIdPat = re.compile(r'[0-9A-Z]+\s/\*\s.+\s\*/,') 
            for children in nameIdPat.findall(conflict):
                node = self.nodeWithNameIDString(children)
                if not self.tree.findNode(node):
                    self.deleteContentInFile(children)
                else:
                    print children + " ✅"

        print "------------------------ done ------------------------"
        pass

    def deleteContentInFile(self, content):
        
        with open(self.project_file,"r") as f:
            lines = f.readlines()
            #print(lines)
        with open(self.project_file,"w") as f_w:
            for line in lines:
                if content == line.strip():
                    print content + " ❌"
                    continue
                f_w.write(line)


def main():
    """
    main method
    """

if __name__ == '__main__':
    main()
    parser = Parser()
    parser.findProjectPath(parser)
    parser.parseProjectFile()
    parser.resolveConflict()