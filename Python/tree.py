#!/usr/bin/python
# -*- coding: UTF-8 -*-


class Tree(object):
    """docstring for Tree"""

    def __init__(self):
        super(Tree, self).__init__()
        self.pendingDict = {}
        self.root = None

    def searchElement(self, elementId):
        pass

    def insertNode(self, node):
        if node.filename is None:
            self.root = node
        self.pendingDict[node.md5] = node

    def generate(self):
        self.generateTreeStruct(self.root)

    def generateTreeStruct(self, root):
        for node in root.children:
            if node.isLeafNode:
                continue
            self.mergeNodeValue(node, self.pendingDict[node.md5])
            self.generateTreeStruct(node)

    def mergeNodeValue(self, node, newNode):
        node.filename = newNode.filename
        node.parent = newNode.parent
        node.children = newNode.children
        node.isLeafNode = newNode.isLeafNode

    def printDesc(self):
        self.printNode(self.root)

    def printNode(self, node):
        print node.md5 + " " + ('' if node.filename is None else node.filename)
        if not node.isLeafNode:
            for n in node.children:
                if n.isLeafNode:
                    print n.md5 + " " + ('' if n.filename is None else n.filename)
                else:
                    self.printNode(n)



class TreeNode(object):
    """docstring for TreeNode"""

    def __init__(self):
        super(TreeNode, self).__init__()
        self.md5 = None
        self.filename = None
        self.parent = None
        self.children = []
        self.isLeafNode = False
