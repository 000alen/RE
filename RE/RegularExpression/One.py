from typing import Tuple

from RE.FiniteStateMachine import FiniteStateMachine
from RE.RegularExpression.Expression import Expression
from RE.RegularExpression.Zero import Zero

__all__ = (
    "One"
)


class One(Expression):
    """One-or-more expression implementation.

    Attributes:
        inner_blocks (list of Expression): The expressions in order.

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
        for i, inner_block in enumerate(self.inner_blocks, 1):
            base_state, counter = inner_block.build(
                finite_state_machine,
                base_state,
                counter,
                end_state if i == len(self.inner_blocks) else None
            )
        _, counter = Zero(*self.inner_blocks).build(
            finite_state_machine,
            base_state,
            counter
        )
        return base_state, counter
