let instance

class JsonParser {
    constructor() {
        this.char = null
        this.index = 0
        this.escapee = {
            '"': '"',
            '\\': '\\',
            '/': '/',
            b: 'b',
            f: '\f',
            n: '\n',
            r: '\r',
            t: '\t',
        }
        this.text = null
        if (!instance) {
            instance = this
        }
        return instance
    }

    error(msg) {
        throw {
            name: 'SyntaxError',
            message: msg,
            at: this.index,
            text: this.text
        }
    }

    next(char) {
        if (char && char !== this.char) {
            this.error(`Expected ${char} instead of ${this.char}`)
        }
        this.char = this.text.charAt(this.index)
        this.index++
        return this.char
    }

    __addCurrentChar(str) {
        str += this.char
        return str
    }

    __continuous_nums(numStr) {
        while (this.char >= '0' && this.char <= '9') {
            numStr += this.char
            this.next()
        }
        return numStr
    }

    number() {
        let numStr = ''
        // statr with minus sign '-'
        if (this.char === '-') {
            numStr = this.__addCurrentChar(numStr)
            this.next('-')
        }

        // start with number
        numStr = this.__continuous_nums(numStr)

        // found point
        if (this.char === '.') {
            numStr = this.__addCurrentChar(numStr)
            numStr += this.__continuous_nums(numStr)
        }

        // found 'e' or 'E'
        if (this.char === 'e' || this.char === 'E') {
            numStr = this.__addCurrentChar(numStr)
            this.next()
            if (this.char === '-' || this.char === '+') {
                numStr = this.__addCurrentChar(numStr)
            }
            numStr = this.__continuous_nums(numStr)
        }

        let number = Number(numStr)
        if (isNaN(number)) {
            this.error('Bad number')
        } else {
            return number
        }
    }

    __escape_character(str) {
        if (this.char === 'u') {
            let uffff = 0
            for (let i = 0; i < 4; i++) {
                this.next()
                let hex = parseInt(this.char, 16)
                if (!isFinite(hex)) {
                    break
                }
                uffff = uffff * 16 + hex
            }
            str += String.fromCharCode(uffff)
        } else if (typeof this.escapee[this.char] === 'string') {
            str += this.escapee[this.char]
        } else {
            this.error('Bad String')
        }
        return str
    }

    string() {
        let string = ''
        if (this.char === '"') {
            while (this.next()) {
                // empty string
                if (this.char === '"') {
                    this.next()
                    return string
                } else if (this.char === '\\') {
                    this.next()
                    string += this.__escape_character(string)
                } else {
                    string += this.__addCurrentChar(string)
                }
            }
        }
        this.error('Bad String')
    }

    white() {
        while (this.char && this.char <= ' ') {
            this.next()
        }
    }

    word() {
        switch (this.char) {
            case 't':
                this.next('t')
                this.next('u')
                this.next('r')
                this.next('e')
                return true
            case 'f':
                this.next('f')
                this.next('a')
                this.next('l')
                this.next('s')
                this.next('e')
                return false
            case 'n':
                this.next('n')
                this.next('u')
                this.next('l')
                this.next('l')
                return null
        }
        this.error(`Unexpected ${this.char}`)
    }

    array() {
        let arr = []
        if (this.char === '[') {
            this.next('[')
            this.white()
        }

        // empty array
        if (this.char === ']') {
            this.next(']')
            return arr
        }

        while (this.char) {
            arr.push(this.value())
            if (this.char === ']') {
                this.next(']')
                return arr
            }
            this.next(',')
            this.white()
        }
        this.error('Bad Array')
    }

    object() {
        let object = {}
        if (this.char === '{') {
            this.next('{')
            this.white()
            if (this.char === '}') {
                this.next('}')
                return object
            }
            while (this.char) {
                let key = this.string()
                this.white()
                this.next(':')
                object[key] = this.value()
                this.white()
                if (this.char === '}') {
                    this.next('}')
                    return object
                }
                this.next(',')
                this.white()
            }
        }
        this.error('Bad Object')
    }

    value() {
        this.white()
        switch (this.char) {
            case '{':
                return this.object()
            case '[':
                return this.array()
            case '"':
                return this.string()
            case '-':
                return this.number()
            default:
                return '0' <= this.char && this.char <= '9' ? this.number() : this.word()
        }
    }

    parse(source, reviver) {
        this.text = source
        this.index = 0
        this.char = ' '
        const result = this.value()
        this.white()
        if (this.char) {
            this.error('Syntax error')
        }

        const walk = (holder, key) => {
            let val = holder[key]
            if (val && typeof val === 'object') {
                for (let k in val) {
                    if (Object.hasOwnProperty.call(val, k)) {
                        let v = walk(val, k)
                        if (v !== undefined) {
                            val[k] = v
                        } else {
                            delete val[k]
                        }
                    }
                }
            }
            return reviver.call(holder, key, val)
        }

        return typeof reviver === 'function' ? walk({'': result}, '') : result
    }
}

const test = () => {
    // test parse
    const Parser = new JsonParser()
    const jsonString = '{"a": 1,"b": 2, "c": "你好", "d": "\\u0026"}'
    const object = Parser.parse(jsonString)
    console.log('parsed object is: ', object)

    // test singleton
    const p1 = new JsonParser()
    const p2 = new JsonParser()
    console.log('singleton is ok: ', p1 === p2)
}

test()

