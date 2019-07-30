# JSONParser

个人学习的 JSON 解析器
## 简介

有三类解析技术

### 1. 手写

* one-way: 扫一遍就可以解析完.
* LL(k): 边读边解析, 上古时代内存有限, 遗留的解析技术.

### 2. parser generator

* jison: bison的js版本, 配置词法和语法, 自动生成解析器的技术.
* antlr: 集成大多数编程语言的语法定义, 让使用者可以专注在AST的transform上.

### 3. parser combinator

* [例子](https://github.com/vlasovskikh/funcparserlib)
* [讨论](https://www.zhihu.com/question/35778359/answer/64769298)

jison 安装 `npm i -g jison`
测试命令 `jison ./json.jison && node json.js json.test`

### ref

[JSON 文法](http://www.json.org/)
[JSON String Regex](https://stackoverflow.com/questions/32155133/regex-to-match-a-json-string)
[JSON Number Regex](https://stackoverflow.com/questions/13340717/json-numbers-regular-expression)


功能
- 解析 JSON 支持的各种数据格式（字符串、数字（整数和小数，支持负数）、布尔值、null）
- 解析 JSON 支持的数据结构（包括数组和对象，支持嵌套）

![py_json_parser](./screenshot/py_json_parser.jpg)

![js-json-parser](./screenshot/js-json-parser.png)

