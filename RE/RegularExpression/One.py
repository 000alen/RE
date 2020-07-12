from typing import List, Tuple

from RE.FiniteStateMachine import FiniteStateMachine
from RE.RegularExpression import RegularExpression
from RE.RegularExpression.Zero import Zero


class One(RegularExpression):
    inner_blocks: List[RegularExpression]

    def __init__(self, *inner_blocks: RegularExpression):
        super().__init__()
        self.inner_blocks = inner_blocks

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
