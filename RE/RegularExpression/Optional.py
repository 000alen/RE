from typing import Tuple

from RE.FiniteStateMachine import FiniteStateMachine, EPSILON
from RE.RegularExpression.Expression import Expression
from RE.RegularExpression.Group import Group


class Optional(Expression):
    def __init__(self, *inner_blocks: Expression):
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
        group = Group(*self.inner_blocks)
        base_state, counter = group.build(
            finite_state_machine, base_state, counter, end_state)
        finite_state_machine.add_transition(
            EPSILON, initial_state, {base_state})
        return base_state, counter
