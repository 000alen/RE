from typing import Tuple

from RE.FiniteStateMachine import FiniteStateMachine
from RE.RegularExpression.Expression import Expression

__all__ = (
    "Group"
)


class Group(Expression):
    """Group expression implementation.

    Attributes:
        inner_blocks (list of Expression): The expression that are concatenated
            in order.

    Examples:
        >>> from RE.RegularExpression.Literal import Literal
        >>> from RE.RegularExpression.Group import Group
        >>> expression = Group(Literal("a"), Literal("b"))
        >>> expression.compile()
        >>> print(expression.match(input("> ")))
    """

    def __init__(self, *blocks: Expression):
        super().__init__()
        self.blocks += blocks

    def build(
            self,
            finite_state_machine: FiniteStateMachine,
            base_state: int,
            counter: int,
            end_state: int = None
    ) -> Tuple[int, int]:
        for i, block in enumerate(self.blocks, 1):
            base_state, counter = block.build(
                finite_state_machine,
                base_state,
                counter,
                end_state
                if i == len(self.blocks)
                else None
            )
        return base_state, counter
