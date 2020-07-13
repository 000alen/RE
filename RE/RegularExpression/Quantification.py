from typing import Tuple

from RE.FiniteStateMachine import FiniteStateMachine
from RE.RegularExpression.Choose import Choose
from RE.RegularExpression.Expression import Expression
from RE.RegularExpression.Group import Group
from RE.RegularExpression.Zero import Zero

__all__ = (
    "Quantification"
)


class Quantification(Expression):
    """Quantification expression implementation.

    Attributes:
        inner_blocks (list of Expression): The expression in order.
        exact (int): The exact number of times that the inner_blocks must
            appear.
        minimum (int): The minimum number of times that the inner_blocks must
            appear.
        maximum (int): The maximum number of times that the inner_blocks must
            appear.

    Examples:
        >>> from RE.RegularExpression.Literal import Literal
        >>> from RE.RegularExpression.Quantification import Quantification
        >>> expression = Quantification(Literal("0"), exact=5)
        >>> expression.compile()
        >>> print(expression.match(input("> ")))
    """

    exact: int
    minimum: int
    maximum: int

    def __init__(self, *inner_blocks: Expression, exact: int = None, minimum: int = None, maximum: int = None):
        super().__init__()
        assert not (exact is None and minimum is None and maximum is None)
        self.exact = exact
        self.minimum = minimum
        self.maximum = maximum
        self.inner_blocks = list(inner_blocks)

    def build(
            self,
            finite_state_machine: FiniteStateMachine,
            base_state: int,
            counter: int,
            end_state: int = None
    ) -> Tuple[int, int]:
        group = Group(*self.inner_blocks)
        if self.exact is not None:
            assert self.exact > 0
            base_state, counter = (group * self.exact).build(
                finite_state_machine,
                base_state,
                counter,
                end_state
            )
        elif self.minimum is not None and self.maximum is not None:
            assert self.minimum < self.maximum
            base_state, counter = Choose(
                *list(
                    group * i
                    for i in range(self.minimum, self.maximum + 1)
                )
            ).build(
                finite_state_machine,
                base_state,
                counter,
                end_state
            )
        elif self.minimum is not None:
            assert self.minimum > 0
            base_state, counter = (group * self.minimum).build(
                finite_state_machine,
                base_state,
                counter,
                end_state
            )
            base_state, counter = Zero(group).build(
                finite_state_machine,
                base_state,
                counter,
            )
        elif self.maximum is not None:
            base_state, counter = Choose(
                *list(
                    group * i
                    for i in range(1, self.maximum + 1)
                )
            ).build(
                finite_state_machine,
                base_state,
                counter,
                end_state
            )
        return base_state, counter
