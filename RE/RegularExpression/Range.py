from typing import Tuple

from RE.FiniteStateMachine import FiniteStateMachine
from RE.RegularExpression.Choose import Choose
from RE.RegularExpression.Expression import Expression
from RE.RegularExpression.Literal import Literal

__all__ = (
    "Range"
)


class Range(Expression):
    """Range expression implementation.

    Attributes:
        from_literal (Literal): The Literal of length 1 that starts the range.
        to_literal (Literal): The literal of length 1 that ends the range.

    Examples:
        >>> from RE.RegularExpression.Literal import Literal
        >>> from RE.RegularExpression.Range import Range
        >>> expression = Range(Literal("0"), Literal("9"))
        >>> expression.compile()
        >>> print(expression.match(input("> ")))
    """

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
