from collections import namedtuple
from typing import Dict, List

from RE.Lexer import Token

__all__ = (
    "Parser"
)

Branch = namedtuple("Branch", ["name", "children"])


class Parser:
    sentences: Dict[str, List[List[str]]]

    def __init__(self, **sentences):
        self.sentences = {**sentences}

    def __contains__(self, name: str) -> bool:
        return self.has_sentence(name)

    def __setitem__(self, name: str, sentences: List[List[Token]]):
        self.add_sentence(name, sentences)

    def __getitem__(self, name: str) -> List[List[Token]]:
        return self.get_sentence(name)

    def __delitem__(self, name: str):
        self.remove_sentence(name)

    def __call__(self, tokens: List[Token]) -> List[Branch]:
        return self.parse(tokens)

    def has_sentence(self, name: str) -> bool:
        return name in self.sentences

    def add_sentence(self, name: str, sentences: List[List[Token]]):
        self.sentences[name] = sentences

    def get_sentence(self, name: str) -> List[List[Token]]:
        return self.sentences[name]

    def remove_sentence(self, name: str):
        del self.sentences[name]

    def parse(self, tokens: List[Token]) -> List[Branch]:
        tree = tokens.copy()
        while len(tree) > 1:
            for name, sentences in self.sentences.items():
                for sentence in sentences:
                    if len(sentence) > len(tree):
                        continue
                    for offset in range(len(tree) - len(sentence) + 1):
                        if all(
                                sentence[i] == tree[j]
                                for i, j in enumerate(range(offset, offset + len(sentence)))
                        ):
                            # reduce
                            tree = [
                                *tree[:offset],
                                Branch(name, tree[offset:offset + len(sentence)]),
                                *tree[offset + len(sentence):]
                            ]
                            print(tree)
        return tree
