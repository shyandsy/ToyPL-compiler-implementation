from tokens import *


"""
AST节点
"""


class NumberNode(object):
    def __init__(self, token: Token):
        self.tok = token

    def __repr__(self):
        return f'{self.tok}'


class BinOpNode(object):
    # 二元操作 + - * /
    def __init__(self, left_node: Token, op_tok: Token, right_node: Token):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

    def __repr__(self):
        return f'({self.left_node, self.op_tok, self.right_node})'


class UnaryOpNode(object):
    # 一元操作 -1   op_tok = -, node = 1
    def __init__(self, op_tok: Token, node: Token):
        self.op_tok = op_tok
        self.node = node

    def __repr__(self):
        return f'({self.op_tok, self.node})'
