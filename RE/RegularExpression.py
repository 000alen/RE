from typing import *

from RE.FiniteAutomaton import FiniteAutomaton


class RegularExpression(FiniteAutomaton[str]):
    __current_state__: int

    def __init__(self):
        super().__init__({0}, {-1})
        self.AddDefaultStates({-2})
        
        self.__current_state__ = 0

    def Literal(self):
        pass

    def Concatenation(self):
        pass

    def Alternation(self):
        pass

    def Kleene(self):
        pass
