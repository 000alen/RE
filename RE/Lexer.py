from collections import namedtuple
from typing import Dict, Iterator, Tuple, List

from RE.RegularExpression.Expression import Expression

__all__ = (
    "Lexer"
)

Token = namedtuple("Token", ["name", "match"])


class Lexer:
    expressions: Dict[str, Expression]

    def __init__(self, **expressions: Expression):
        self.expressions = {**expressions}

    def __contains__(self, name: str) -> bool:
        return self.has_expression(name)

    def __setitem__(self, name: str, expression: Expression):
        self.add_expression(name, expression)

    def __getitem__(self, name: str) -> Expression:
        return self.get_expression(name)

    def __delitem__(self, name: str):
        self.remove_expression(name)

    def has_expression(self, name: str) -> bool:
        return name in self.expressions

    def add_expression(self, name: str, expression: Expression):
        self.expressions[name] = expression

    def get_expression(self, name: str) -> Expression:
        return self.expressions[name]

    def remove_expression(self, name: str):
        del self.expressions[name]

    def lex(self, string: str) -> Iterator[Tuple[int, Token]]:
        position = 0
        while position < len(string):
            tokens: List[Token] = []
            for name, expression in self.expressions.items():
                match = expression.match(string, position)
                if match:
                    tokens.append(Token(name, match))
            if tokens:
                token = max(tokens, key=lambda _: len(_.match))
                yield position, token
                position += len(token.match)
            else:
                yield position, Token('UNDEFINED', string[position:])
                return