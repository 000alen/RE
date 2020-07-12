from typing import Tuple

from RE.FiniteStateMachine import FiniteStateMachine
from RE.RegularExpression import RegularExpression
from RE.RegularExpression.Literal import Literal
from RE.RegularExpression.Choose import Choose


class Range(RegularExpression):
    from_literal: Literal
    to_literal: Literal

    def __init__(self, from_literal: Literal, to_literal: Literal):
        super().__init__()
        assert len(from_literal.literal) == 1
        assert len(to_literal.literal) == 1
        self.from_literal = from_literal
        self.to_literal = to_literal

    def build(
        self,
        finite_state_machine: FiniteStateMachine,
        base_state: int,
        counter: int,
        end_state: int = None
    ) -> Tuple[int, int]:
        base_state, counter = Choose(*[
            Literal(chr(i))
            for i in range(ord(self.from_literal.literal), ord(self.to_literal.literal) + 1)
        ]).build(
            finite_state_machine,
            base_state,
            counter,
            end_state
        )
        return base_state, counter
