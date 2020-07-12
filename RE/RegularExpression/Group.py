from typing import List, Tuple

from RE.FiniteStateMachine import FiniteStateMachine
from RE.RegularExpression.Expression import Expression


class Group(Expression):
    blocks: List[Expression]

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
