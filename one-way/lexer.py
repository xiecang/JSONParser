__all__ = ['Type', 'Token', 'json_tokens']

from enum import Enum


class Type(Enum):
    auto = 0  # auto 指 6 个单字符符号 `:,{}[]` , 用来方便写代码的
    colon = 1  # :
    comma = 2  # ,
    braceLeft = 3  # {
    braceRight = 4  # }
    bracketLeft = 5  # [
    bracketRight = 6  # ]
    number = 7  # 169
    string = 8  # "name"
    boolean = 9  # true
    null = 10  # null


class Token(object):
    def __init__(self, token_type, token_value):
        d = {
            ':': Type.colon,
            ',': Type.comma,
            '{': Type.braceLeft,
            '}': Type.braceRight,
            '[': Type.bracketLeft,
            ']': Type.bracketRight,
        }
        if token_type == Type.auto:
            self.type = d[token_value]
        else:
            self.type = token_type
        self.value = token_value

    def __repr__(self):
        return '({}, {})'.format(self.value, self.type)


class JSONDecodeError(ValueError):
    pass


def string_end(code, index):
    s = ''
    offset = index
    while offset < len(code):
        c = code[offset]
        if c == '"':
            # 找到了字符串的结尾
            # s = code[index:offset]
            return s, offset
        elif c == '\\':
            # 处理转义符, 现在只支持 \" \t \n \\
            d = {
                '"': '"',
                't': '\t',
                'n': '\n',
                '\\': '\\',
            }
            next = d.get(code[offset + 1])
            if next is not None:
                s += next
                offset += 2
            else:
                # 这是一个错误, 非法转义符
                raise JSONDecodeError("Illegal escape character")
        else:
            s += c
            offset += 1
    # 程序出错, 没有找到反引号 "
    raise JSONDecodeError('Unterminated string')


def boolean_end(code, index):
    i = index - 1
    c = code[i]
    expected = {
        't': 'true',
        'f': 'false',
    }[c]
    offset = len(expected)
    actual = code[i: i + offset]
    if actual == expected:
        return actual, i + offset - 1
    else:
        raise JSONDecodeError("Invalid Token {}".format(actual))


def null_end(code, index):
    i = index - 1
    expected = 'null'
    offset = len(expected)
    actual = code[i: i + offset]
    if actual == expected:
        return actual, i + offset - 1
    else:
        raise JSONDecodeError("Invalid Token {}".format(actual))


def json_tokens(code):
    length = len(code)
    tokens = []
    spaces = '\n\t\r'
    digits = '1234567890'
    # 当前下标
    i = 0
    while i < length:
        # 先看看当前应该处理啥
        c = code[i]
        i += 1
        if c in spaces:
            # 空白符号要跳过, space tab return
            continue
        elif c in ':,{}[]':
            # 处理 6 中单个符号
            t = Token(Type.auto, c)
            tokens.append(t)
        elif c == '"':
            # 处理字符串
            s, offset = string_end(code, i)
            i = offset + 1
            t = Token(Type.string, s)
            tokens.append(t)
        elif c in digits:
            # 处理数字, 现在不支持小数和负数
            end = 0
            for offset, char in enumerate(code[i:]):
                if char not in digits:
                    end = offset
                    break
            n = code[i - 1:i + end]
            i += end
            t = Token(Type.number, n)
            tokens.append(t)
        elif c in 'tf':
            # 处理布尔值
            b, offset = boolean_end(code, i)
            i = offset + 1
            t = Token(Type.boolean, b)
            tokens.append(t)
        elif c == 'n':
            # 处理null值
            b, offset = null_end(code, i)
            i = offset + 1
            t = Token(Type.null, b)
            tokens.append(t)
        else:
            # 出错了
            pass
    return tokens
