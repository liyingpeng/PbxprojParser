# -*- coding: utf-8 -*-	1
################################################################################
#
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
#
################################################################################

"""
Stack
Authors: liyingpeng
Date:    2016 / 11 / 14
"""


class Stack(object):
    """
    Stack stucture
    """

    def __init__(self):
        super(Stack, self).__init__()
        self.stack = []

    def empty(self):
        """
        Return is the stack empty
        """
        return self.stack == []

    def push(self, data):
        """
        Push an object to statck
        """
        self.stack.append(data)

    def pop(self):
        """
        Pop an obj from stack
        """
        if self.empty():
            return None
        else:
            return self.stack.pop(-1)

    def top(self):
        """
        Return top element of the stack
        """
        if self.empty():
            return None
        else:
            return self.stack[-1]

    def length(self):
        """
        Return the length of stack
        """
        return len(self.stack)
