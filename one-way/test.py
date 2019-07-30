from parser import parse


def ensure(condition, error_msg):
    if not condition:
        print(error_msg)


def main():
    code = """
    {
        "na\\\"m\\te\\n": "lua",
        "height": 170,
        "male": true,
        "following": [{
            "ping": 100,
            "pong": true
        }, 100, false, null]
    }
    """
    actual = parse(code)
    expected = {
        "na\"m\te\n": "lua",
        "height": 170,
        "male": True,
        "following": [{
            "ping": 100,
            "pong": True
        }, 100, False, None]
    }
    ensure(actual == expected, "parse error")


if __name__ == '__main__':
    main()
