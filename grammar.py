from basic import (Token, Lexer)
from constant import (TT_INT, TT_FLOAT, TT_PLUS, TT_MINUS, TT_MUL, TT_DIV, TT_LPAREN, TT_RPAREN, TT_EOF)
from errors import (InvalidSyntaxError)

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


"""
语法解析结果
"""


class ParserResult(object):
    def __init__(self):
        self.error = None
        self.node = None

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self

    def register(self, res):
        if isinstance(res, ParserResult):
            if res.error:
                self.error = res.error
            return res.node
        return res


"""
词法分析器
"""


class Parser(object):
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.current_tok: Token = None
        self.advance()

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def parse(self):
        res = self.expr()
        if not res.error and self.current_tok.ttype != TT_EOF:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start.copy(),
                self.current_tok.pos_end.copy(),
                "Expected '+', '-', '*', or '/'"
            ))
        return res

    def factor(self):
        """
        factor -> INT | FLOAT
            -> (PLUS | MINUS ) factor
            -> LPAREN expr RPAREN
        :return:
        """
        res = ParserResult()
        tok = self.current_tok

        """
        1 + 1
        INT -> 1
        tok = +
        并不需要error判断，他只是一个简单的token
        
        -1 + 1
        MINUS -> 0
        tok = 1
        tok = factor
        factor 非终止符
        因为是非终止符，会继续匹配，匹配过程中，可能发现error
        因此需要error判断
        """
        if tok.ttype in (TT_INT, TT_FLOAT):  # factor -> INT | FLOAT
            res.register(self.advance())
            return res.success(NumberNode(tok))  # (PLUS | MINUS ) factor

        elif tok.ttype in (TT_PLUS, TT_MINUS):
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOpNode(tok, factor))

        elif tok.ttype == TT_LPAREN:
            res.register(self.advance())
            expr = res.register(self.expr())
            if res.error:
                return res

            if self.current_tok.ttype == TT_RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start.copy(),
                    self.current_tok.pos_end.copy(),
                    "Expected ')'"
                ))
        return res.failure(InvalidSyntaxError(
            self.current_tok.pos_start.copy(),
            self.current_tok.pos_end.copy(),
            "Expected int or float"
        ))

    def term(self):
        """
        term -> factor ( MUL | DIV ) factor)*
        :return:
        """
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))

    def expr(self):
        """
        exp -> term (( PLUS | MINUS ) term)*
        :return:
        """
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    def bin_op(self, func, ops):
        """
        common function for term and expr
        递归调用，构建AST
        :param func: function
        :param ops:
        :return:
        """
        res = ParserResult()
        left = res.register(func())
        while self.current_tok.ttype in ops:
            op_tok = self.current_tok
            res.register(self.advance())
            right = res.register(func())
            left = BinOpNode(left, op_tok, right)
        return res.success(left)


def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_token()
    print(tokens)
    # 生成AST
    parser = Parser(tokens)
    ast = parser.parse()
    return ast.node, ast.error
