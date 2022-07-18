from position import Position


class Error(object):
    def __init__(self, pos_start: Position, pos_end: Position, error_name: str, details: str):
        """
        :param pos_start: 错误起始位置
        :param pos_end: 错误终止为止
        :param error_name: 错误类型名称
        :param details: 错误细节
        """
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        res = f'{self.error_name}: {self.details}'
        res += f'File: {self.pos_start.fn}, line {self.pos_end.line + 1}'
        return res


class IllegalCharError(Error):
    # 非法字符错误
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Illegal Character", details)


class InvalidSyntaxError(Error):
    # 无效语法
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Invalid Syntax", details)