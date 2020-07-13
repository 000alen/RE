from typing import Union, Tuple

from RE.FiniteStateMachine import FiniteStateMachine, SIGMA
from RE.RegularExpression.Expression import Expression

__all__ = (
    "Wildcard"
)


class Wildcard(Expression):
    """Wildcard expression implementation.

    Attributes:
        wildcard_set (Union of str and frozenset): The set which contains the
            expected elements.

    Examples:
        >>> from RE.RegularExpression.Wildcard import Wildcard
        >>> expression = Wildcard()
        >>> expression.compile()
        >>> print(expression.match(input("> ")))
    """

    wildcard_set: Union[str, frozenset]

    def __init__(self, wildcard_set: Union[str, frozenset] = SIGMA):
        super().__init__()
        self.wildcard_set = wildcard_set

    def build(
            self,
            finite_state_machine: FiniteStateMachine,
            base_state: int,
            counter: int,
            end_state: int = None
    ) -> Tuple[int, int]:
        finite_state_machine.add_transition(
            self.wildcard_set,
            base_state,
            {counter}
            if end_state is None
            else {end_state}
        )
        if end_state is None:
            base_state = counter
            counter += 1
        else:
            base_state = end_state
        return base_state, counter
