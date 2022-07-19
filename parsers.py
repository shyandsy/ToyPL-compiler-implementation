from ast_node import *
from errors import *
from tokens import *


class ParserResult(object):
    """
    语法解析结果
    """
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


class Parser(object):
    """
    词法分析器
    """
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