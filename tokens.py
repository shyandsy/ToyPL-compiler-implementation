from position import Position

DIGITS = "0123456789"

# token type => TT
TT_INT = "INT"
TT_FLOAT = "FLOAT"
TT_PLUS = "PLUS"
TT_MINUS = "MINUS"
TT_MUL = "MUL"
TT_DIV = "DIV"
TT_LPAREN = "LPAREN"
TT_RPAREN = "RPAREN"
TT_EOF = "EOF"  # 终止符


class Token(object):
    # <token-name, attribute-value >
    def __init__(self, ttype: str, value=None, pos_start: Position = None, pos_end: Position = None):
        """
        :param ttype: 类型
        :param value:
        :param pos_start: Position类实例，当前起始位置
        :param pos_end: Position类实例，当前结束位置
        """
        self.ttype = ttype
        self.value = value
        if pos_start:
            # Token 单个字符, + => pos_start = pos_end, advance
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance(self.value)
        if pos_end:
            self.pos_end = pos_end.copy()

    def __repr__(self):
        if self.value:
            return f'{self.ttype}: {self.value}'
        return f'{self.ttype}'