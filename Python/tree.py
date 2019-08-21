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

    # 生成已root为根节点的树结构
    def generateTreeStruct(self, root):
        nodeRemoved = []
        for node in root.children:
            if node.isLeafNode:
                continue
            realNode = self.pendingDict[node.md5]
            if node.filename != realNode.filename:
                # 当页面发生冲突时需要校验 md5和文件名 以免文件名修改（文件名修改的冲突，md5是不会变的）
                nodeRemoved.append(node)
                continue
            self.mergeNodeValue(node, realNode)
            self.generateTreeStruct(node)

        # 删除非法节点
        for node in nodeRemoved:
            root.children.remove(node)

    # 因为 node 只有md5 所以需要从pending 里面 merge property
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
