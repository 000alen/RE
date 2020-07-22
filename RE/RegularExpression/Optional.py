from typing import Tuple

from RE.FiniteStateMachine import FiniteStateMachine, Symbol
from RE.RegularExpression.Expression import Expression
from RE.RegularExpression.Group import Group

__all__ = (
    "Optional"
)


class Optional(Expression):
    """One-or-more expression implementation.

    Attributes:
        inner_blocks (list of Expression): The expression in order.

    Examples:
        >>> from RE.RegularExpression.Literal import Literal
        >>> from RE.RegularExpression.One import One
        >>> expression = One(Literal("0"))
        >>> expression.compile()
        >>> print(expression.match(input("> ")))
    """

    def __init__(self, *inner_blocks: Expression):
        super().__init__()
        self.inner_blocks = list(inner_blocks)

    def build(
            self,
            finite_state_machine: FiniteStateMachine,
            base_state: int,
            counter: int,
            end_state: int = None
    ) -> Tuple[int, int]:
        initial_state = base_state
        group = Group(*self.inner_blocks)
        base_state, counter = group.build(
            finite_state_machine, base_state, counter, end_state)
        finite_state_machine.add_transition(
            Symbol.EPSILON, initial_state, {base_state})
        return base_state, counter
