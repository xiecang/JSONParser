from typing import List

__all__ = ['parse']

from lexer import Type, json_tokens, Token


def match(token, type):
    return token.type == type


def parsed_string(tokens, index):
    t1 = tokens[index]
    return t1.value, index + 1


def parsed_number(tokens, index):
    t1 = tokens[index]
    val = int(t1.value)
    return val, index + 1


def parsed_null(tokens, index):
    return None, index + 1


def parsed_boolean(tokens, index):
    t1 = tokens[index]
    val = True if t1.value == 'true' else False
    return val, index + 1


def parsed_members(tokens, index):
    val, index = parsed_value(tokens, index)
    members = [val]
    t1 = tokens[index]
    while match(t1, Type.comma):
        val, i = parsed_value(tokens, index + 1)
        members.append(val)
        index = i
        t1 = tokens[i]
    return members, index


def parsed_array(tokens, index):
    members, i = parsed_members(tokens, index + 1)
    t1 = tokens[i]
    if match(t1, Type.bracketRight):
        return members, i + 1
    else:
        raise Exception("expected {} found {} ".format("]", t1))


def parsed_value(tokens, index):
    t1 = tokens[index]
    d = {
        Type.string: parsed_string,
        Type.number: parsed_number,
        Type.null: parsed_null,
        Type.boolean: parsed_boolean,
        Type.braceLeft: parsed_dict,
        Type.bracketLeft: parsed_array,
    }
    fn = d.get(t1.type)
    if fn is not None:
        return fn(tokens, index)
    else:
        raise Exception("invalid {}, while parsing value".format(t1))


def parsed_pair(tokens, index):
    t1 = tokens[index]
    t2 = tokens[index + 1]
    if match(t1, Type.string) and match(t2, Type.colon):
        key, i = parsed_string(tokens, index)
        val, i = parsed_value(tokens, i + 1)
        return (key, val), i
    else:
        raise Exception("expected {} found {} {}".format("string:", t1, t2))


def parsed_pairs(tokens, index):
    pair, index = parsed_pair(tokens, index)
    pairs = [pair]
    t1 = tokens[index]
    while match(t1, Type.comma):
        p, i = parsed_pair(tokens, index + 1)
        pairs.append(p)
        index = i
        t1 = tokens[i]
    return pairs, index


def parsed_dict(tokens, index):
    paris, i = parsed_pairs(tokens, index + 1)
    t1 = tokens[i]
    if match(t1, Type.braceRight):
        return dict(paris), i + 1
    else:
        raise Exception("expected {}, found: {}".format("}", t1))


def parsed_json(tokens: List[Token]):
    t1 = tokens[0]
    if match(t1, Type.braceLeft):
        return parsed_dict(tokens, 0)[0]
    elif match(t1, Type.bracketLeft):
        return parsed_array(tokens, 0)[0]
    else:
        raise Exception("expected {} found {} ".format("{ or [", t1))


def parse(code: str):
    tokens = json_tokens(code)
    r = parsed_json(tokens)
    return r
