from typing import List, Tuple, Union

from RE.FiniteStateMachine import FiniteStateMachine


DIGITS = frozenset("0123456789")

LETTERS_LOWER = frozenset("abcdefghijklmnopqrstuvwxyz")
LETTERS_UPPER = frozenset("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
LETTERS = LETTERS_LOWER | LETTERS_UPPER


class Expression:
    finite_state_machine: FiniteStateMachine
    blocks: List["Expression"]
    inner_blocks: List["Expression"]

    def __init__(
        self,
        finite_state_machine: FiniteStateMachine = None
    ):
        self.finite_state_machine = finite_state_machine
        self.blocks = []
        self.inner_blocks = []

    def __add__(self, expression: "Expression"):
        from RE.RegularExpression.Group import Group
        if isinstance(self, Group):
            if isinstance(expression, Group):
                self.blocks += expression.blocks
            else:
                self.blocks.append(expression)
            return self
        elif isinstance(expression, Group):
            expression.blocks.insert(0, self)
            return expression
        return Group(self, expression)

    def __mul__(self, i: int):
        from RE.RegularExpression.Group import Group
        if isinstance(self, Group):
            self.blocks *= i
            return self
        return Group(self).__mul__(i)

    def __or__(self, expression: "Expression"):
        from RE.RegularExpression.Choose import Choose
        return Choose(self, expression)

    def compile(self):
        self.finite_state_machine = FiniteStateMachine(
            {0}, default_states={-1})
        base_state, counter = self.build(self.finite_state_machine, 0, 1)
        self.finite_state_machine.add_final_states({base_state})

    def match(self, string: str):
        assert string != ""
        if self.finite_state_machine is None:
            self.compile()
        return self.finite_state_machine.accepts(string)

    def build(
        self,
        finite_state_machine: FiniteStateMachine,
        base_state: int,
        counter: int,
        end_state: int = None
    ) -> Tuple[int, int]:
        raise NotImplementedError
