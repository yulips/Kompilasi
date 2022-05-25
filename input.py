import python_lexer
import python_parser
import python_interpreter

from sys import *

lexer = python_lexer.python_lexer()
parser = python_parser.python_parser()
env = {}

file = open(argv[1])
text = file.readlines()

for line in text:
    tree = parser.parse(lexer.tokenize(line))
    python_interpreter.python_interpreter(tree, env)
