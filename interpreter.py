from parsers import *
from tokens import *

"""
获得运行时结果

解释器: code -> 解释器 -> 结果
编译器: code -> 编译器 -> 可执行文件exe -> 执行程序获得结果
"""


class RTResult(object):
    def __init__(self):
        self.value = None
        self.error = None

    def success(self, value):
        self.value = value
        return self

    def failure(self, error):
        self.error = error
        return self

    def register(self, res):
        if res.error:
            self.error = res.error
        return res.value


class Context(object):
    def __init__(self, display_name: str, parent=None, parent_entry_pos: Position = None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos


class Number(object):
    def __init__(self, value):
        self.value = value
        #self.pos_start = None
        #self.pos_end = None
        #self.context = None
        self.set_pos()  # 报错的位置
        self.set_context()  # 方便定位错误,运行时报错上下文

    def set_pos(self, pos_start: Position = None, pos_end: Position = None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context: Context = None):
        self.context = context
        return self

    def added_by(self, other):
        # 加法
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None

    def subtracted_by(self, other):
        # 减法
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None

    def multiplicated_by(self, other):
        # 乘法
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None

    def divided_by(self, other):
        # 除法
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(other.pos_start, other.pos_end, "分母不能是0", self.context)
            return Number(self.value / other.value).set_context(self.context), None

    def __repr__(self):
        return str(self.value)


class Interpreter(object):
    def visit(self, node, context):
        """
        递归下降算法 -> ast node
        :param node: 起始节点
        :param context: 上下文，方便定位错误位置
        :return:
        """
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__}')

    def visit_NumberNode(self, node, context):
        return RTResult().success(
            Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_BinOpNode(self, node, context):
        res = RTResult()

        # 左递归
        left = res.register(self.visit(node.left_node, context))
        if res.error:
            return res
        # 右递归
        right = res.register(self.visit(node.right_node, context))
        if res.error:
            return res

        # 运算
        if node.op_tok.ttype == TT_PLUS:
            result, error = left.added_by(right)
        elif node.op_tok.ttype == TT_MINUS:
            result, error = left.subtracted_by(right)
        elif node.op_tok.ttype == TT_MUL:
            result, error = left.multiplicated_by(right)
        elif node.op_tok.ttype == TT_DIV:
            result, error = left.divided_by(right)
        else:
            raise Exception("未知操作")

        if error:
            return res.failure(error)

        return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        number = res.register(self.visit(node.node, context))
        if res.error:
            return res

        error = None
        if node.op_tok.type == TT_MINUS:
            number, error = number.multiplicated_by(Number(-1))

        if error:
            return res.failure(error)
        return res.success(number.set_pos(node.pos_start, node.pos_end))
