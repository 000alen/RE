from typing import Tuple

from RE.FiniteStateMachine import FiniteStateMachine
from RE.RegularExpression.Expression import Expression

__all__ = (
    "Choose"
)


class Choose(Expression):
    """Choose expression implementation.

    Attributes:
        inner_blocks (list of Expression): The options to choose: at a given point, there will be multiple paths in the
            FSM, and those paths are defined by these blocks.

    Examples:
        >>> from RE.RegularExpression.Literal import Literal
        >>> from RE.RegularExpression.Choose import Choose
        >>> expression = Choose(Literal("0"), Literal("1"))
        >>> expression.compile()
        >>> print(expression.match(input("> ")))
    """

    def __init__(self, *inner_blocks: Expression):
        super().__init__()
        self.inner_blocks = list(inner_blocks)

    def alternate(self, expression: "Expression") -> "Expression":
        if isinstance(expression, Choose):
            self.inner_blocks += expression.inner_blocks
            return self
        return super().concatenate(expression)

    def build(
            self,
            finite_state_machine: FiniteStateMachine,
            base_state: int,
            counter: int,
            end_state: int = None
    ) -> Tuple[int, int]:
        for inner_block in self.inner_blocks:
            end_state, counter = inner_block.build(
                finite_state_machine,
                base_state,
                counter,
                end_state
            )
        return end_state, counter
