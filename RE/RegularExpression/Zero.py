from typing import Tuple

from RE.FiniteStateMachine import FiniteStateMachine
from RE.RegularExpression.Expression import Expression

__all__ = (
    "Zero"
)


class Zero(Expression):
    """Zero-or-more expression implementation.

    Attributes:
        inner_blocks (list of Expression): The expressions in order.

    Examples:
        >>> from RE.RegularExpression.Literal import Literal
        >>> from RE.RegularExpression.Zero import Zero
        >>> expression = Literal("0") + Zero(Literal("0"))
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
        loop_state = counter
        for i, inner_block in enumerate(self.inner_blocks, 1):
            if i == len(self.inner_blocks) and end_state is not None:
                for element, to_state in finite_state_machine.get_state(initial_state):
                    if to_state == {loop_state}:
                        finite_state_machine.add_transition(
                            element, end_state, {loop_state})
                return end_state, counter
            base_state, counter = inner_block.build(
                finite_state_machine,
                base_state,
                counter,
                initial_state if i == len(self.inner_blocks) else None
            )
        return initial_state, counter
