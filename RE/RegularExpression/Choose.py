from typing import List, Tuple

from RE.FiniteStateMachine import FiniteStateMachine
from RE.RegularExpression.Expression import Expression


class Choose(Expression):
    inner_blocks: List[Expression]

    def __init__(self, *inner_blocks: Expression):
        super().__init__()
        self.inner_blocks = inner_blocks

    def __or__(self, expression: Expression):
        if isinstance(expression, Choose):
            self.inner_blocks += expression.inner_blocks
            return self
        return super().__or__(expression)

    def build(
        self,
        finite_state_machine: FiniteStateMachine,
        base_state: int,
        counter: int,
        end_state: int = None
    ) -> Tuple[int, int]:
        for i, inner_block in enumerate(self.inner_blocks, 1):
            end_state, counter = inner_block.build(
                finite_state_machine,
                base_state,
                counter,
                end_state
            )
        return end_state, counter
