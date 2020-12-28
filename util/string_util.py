import re


class StrUtil(object):

    @staticmethod
    def split_lines_omit_empty(text):
        return StrUtil.split_omit_empty('\r?\n', text)

    @staticmethod
    def split_omit_empty(separator, text):
        return list(filter(lambda x: x, re.split('\\s*{separator}\\s*'.format(separator=separator), text)))

    @staticmethod
    def indent(text, num=1, space_size=4):
        lines = re.split("\r?\n", text)
        return '\n'.join(list(map(lambda x: ' ' * num * space_size + x, lines)))


class StrLinesPool(object):

    def __init__(self, text, omit_empty=True):
        if omit_empty:
            self.__lines = StrUtil.split_lines_omit_empty(text)
        else:
            self.__lines = re.split('\r?\n', text)

    def has_next(self):
        return len(self.__lines) > 0

    def get_line(self):
        if self.has_next():
            return self.__lines.pop(0)
        else:
            raise RuntimeError
