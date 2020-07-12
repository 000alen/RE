from typing import Tuple

from RE.FiniteStateMachine import FiniteStateMachine
from RE.RegularExpression.Range import Range


class Literal(RegularExpression):
    literal: str

    def __init__(self, literal: str):
        super().__init__()
        self.literal = literal

    def __add__(self, expression: RegularExpression):
        if isinstance(expression, Literal):
            self.literal += expression.literal
            return self
        return super().__add__(expression)

    def __rshift__(self, expression: RegularExpression):
        if isinstance(expression, Literal):
            return Range(self, expression)
        raise TypeError

    def build(
        self,
        finite_state_machine: FiniteStateMachine,
        base_state: int,
        counter: int,
        end_state: int = None
    ) -> Tuple[int, int]:
        for i, character in enumerate(self.literal, 1):
            finite_state_machine.add_transition(
                character,
                base_state,
                {end_state}
                if i == len(self.literal) and end_state is not None
                else {counter}
            )
            if i == len(self.literal) and end_state is not None:
                return end_state, counter
            base_state = counter
            counter += 1
        return base_state, counter
