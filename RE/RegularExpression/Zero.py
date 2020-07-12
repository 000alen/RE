from typing import List, Tuple

from RE.FiniteStateMachine import FiniteStateMachine
from RE.RegularExpression import RegularExpression


class Zero(RegularExpression):
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
