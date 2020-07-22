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
        exact (int): The exact number of times that the inner_blocks must appear.
        minimum (int): The minimum number of times that the inner_blocks must appear.
        maximum (int): The maximum number of times that the inner_blocks must appear.

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

        def _exact() -> Tuple[int, int]:
            assert self.exact > 0
            return (group * self.exact).build(
                finite_state_machine,
                base_state,
                counter,
                end_state
            )

        def _minimum_maximum() -> Tuple[int, int]:
            assert self.minimum < self.maximum
            return Choose(
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

        def _minimum() -> Tuple[int, int]:
            assert self.minimum > 0
            _base_state, _counter = (group * self.minimum).build(
                finite_state_machine,
                base_state,
                counter,
                end_state
            )
            return Zero(group).build(
                finite_state_machine,
                _base_state,
                _counter,
            )

        def _maximum() -> Tuple[int, int]:
            return Choose(
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

        group = Group(*self.inner_blocks)
        if self.exact is not None:
            return _exact()
        elif self.minimum is not None and self.maximum is not None:
            return _minimum_maximum()
        elif self.minimum is not None:
            return _minimum()
        elif self.maximum is not None:
            return _maximum()
        raise Exception
