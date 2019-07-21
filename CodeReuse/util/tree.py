#!/usr/bin/python
# -*- coding: UTF-8 -*-


class Tree(object):
    """docstring for Tree"""

    def __init__(self):
        super(Tree, self).__init__()
        self.searchPath = ''
        self.treeArray = []

    def searchElement(self, elementId):
        pass

    def insertElement(self, element):
        '''
        插入新的节点
        '''
        newTNode = TreeNode()
        newTNode.data = element
        for tNode in self.treeArray:
            for child in tNode.data.children:
                if child.id == element.id:
                    newTNode.parent = tNode
                    tNode.children.append(newTNode)
                    break
                    pass
        for child in element.children:
            for tNode in self.treeArray:
                if child.id == tNode.data.id:
                    newTNode.children.append(tNode)
                    tNode.parent = newTNode
                    break
                    pass

        self.treeArray.append(newTNode)
        pass

    def treeEmpty(self):
        pass

    def treeDepth(self):
        pass

    def valueForElement(self, element):
        pass

    def traverse(self):
        pass

    def passAll(self, tNode):
        '''
        将tNode节点下所有的节点标记为passed
        '''
        tNode.passed = True
        if not len(tNode.children):
            return

        for child in tNode.children:
            self.passAll(child)
        pass

    def updateStatus(self):
        """
        将所有节点的passed更新为false
        """
        for tNode in self.treeArray:
            tNode.passed = False
        pass

    def findRoots(self):
        roots = []
        for tNode in self.treeArray:
            if not tNode.parent:
                roots.append(tNode)
                pass
        return roots
        pass


class TreeNode(object):
    """docstring for TreeNode"""

    def __init__(self):
        super(TreeNode, self).__init__()
        self.data = None
        self.parent = None
        self.children = []
        self.passed = False
