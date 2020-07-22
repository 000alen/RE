"""A very basic definition of BaseTypes using RE."""

from RE.Lexer import Lexer
from RE.Parser import Parser, Branch
from RE.RegularExpression.Literal import Literal
from RE.RegularExpression.One import One

expressions = {
    "boolean": Literal("true") | Literal("false"),
    "AND": Literal("and"),
    "OR": Literal("or"),
    "NOT": Literal("not"),
    "L": Literal("("),
    "R": Literal(")"),
    "WHITESPACE": One(Literal(" "))
}

lexer = Lexer(**expressions)

sentences = {
    "expression": [
        ["boolean"],
        ["NOT", "expression"],
        ["L", "expression", "R"],
        ["expression", "AND", "expression"],
        ["expression", "OR", "expression"]
    ]
}

parser = Parser(**sentences)

string = input("> ")

tokens = list(token for _, token in lexer.lex(string) if token.name != "WHITESPACE")
print("tokens:", tokens)

tree = parser.parse(tokens)
print("tree:", tree)

tree = [
    Branch(
        name='expression',
        children=[
            Branch(
                name='boolean',
                children='true'
            )
        ]
    ),
    Branch(
        name='AND',
        children='and'
    ),
    Branch(
        name='boolean',
        children='false'
    )
]
