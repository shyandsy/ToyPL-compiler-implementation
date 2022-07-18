class Position(object):
    def __init__(self, idx, line, col, fn, ftext):
        """
        :param idx: 索引
        :param line: 行号
        :param col: 列好
        :param fn: 文件名
        :param ftext: 内容
        """
        self.idx = idx
        self.line = line
        self.col = col
        self.fn = fn
        self.ftext = ftext

    def advance(self, current_char):
        self.idx += 1
        self.col += 1
        if current_char == '\n':
            self.col = 0
            self.line += 1

    def copy(self):
        return Position(self.idx, self.line, self.col, self.fn, self.ftext)