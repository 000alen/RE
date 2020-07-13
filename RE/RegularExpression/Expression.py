from typing import List, Tuple, Iterator

from RE.FiniteStateMachine import FiniteStateMachine

__all__ = (
    "Expression"
)


class Expression:
    """Baseclass for Regular Expressions.

    Examples:
        >>> from RE.RegularExpression.Expression import Expression
        >>> from RE.Utility import import_finite_state_machine
        >>> expression = Expression(import_finite_state_machine("expression.json"))
        >>> expression.compile()
        >>> print(expression.match(input("> ")))
    """

    finite_state_machine: FiniteStateMachine
    blocks: List["Expression"]
    inner_blocks: List["Expression"]

    def __init__(
            self,
            finite_state_machine: FiniteStateMachine = None
    ):
        self.finite_state_machine = finite_state_machine
        self.blocks = []
        self.inner_blocks = []

    def __add__(self, expression: "Expression") -> "Expression":
        return self.concatenate(expression)

    def __mul__(self, i: int) -> "Expression":
        return self.repeat(i)

    def __or__(self, expression: "Expression") -> "Expression":
        return self.alternate(expression)

    def concatenate(self, expression: "Expression") -> "Expression":
        from RE.RegularExpression.Group import Group
        if isinstance(expression, Group):
            expression.blocks.insert(0, self)
            return expression
        return Group(self, expression)

    def repeat(self, i: int) -> "Expression":
        from RE.RegularExpression.Group import Group
        return Group(self).repeat(i)

    def alternate(self, expression: "Expression") -> "Expression":
        from RE.RegularExpression.Choose import Choose
        return Choose(self, expression)

    def compile(self):
        self.finite_state_machine = FiniteStateMachine(
            {0}, default_states={-1})
        base_state, counter = self.build(self.finite_state_machine, 0, 1)
        self.finite_state_machine.add_final_states({base_state})

    def match(self, string: str, start: int = 0, end: int = None) -> str:
        assert string
        if self.finite_state_machine is None:
            self.compile()
        if end is None:
            end = len(string)
        last_final_position = None
        for position, element, current_states in self.finite_state_machine.run(string[start:end]):
            if current_states & self.finite_state_machine.final_states:
                last_final_position = position
        if last_final_position is not None:
            return string[start: start + last_final_position + 1]

    def match_all(self, string: str, start: int = 0, end: int = None) -> Iterator[str]:
        assert string
        if self.finite_state_machine is None:
            self.compile()
        if end is None:
            end = len(string)
        while start < end:
            last_final_position = None
            for position, element, current_states in self.finite_state_machine.run(string[start:end]):
                if current_states & self.finite_state_machine.final_states:
                    last_final_position = position
            if last_final_position is not None:
                yield string[start: start + last_final_position + 1]
                start += last_final_position
            start += 1

    def search(self, string: str, start: int = 0, end: int = None) -> Tuple[int, str]:
        assert string
        if self.finite_state_machine is None:
            self.compile()
        if end is None:
            end = len(string)
        for i in range(start, end):
            match = self.match(string[i:end])
            if match:
                return i, match

    def search_all(self, string: str, start: int = 0, end: int = None) -> Iterator[Tuple[int, str]]:
        assert string
        if self.finite_state_machine is None:
            self.compile()
        if end is None:
            end = len(string)
        for i in range(start, end):
            match = self.match(string[i:end])
            if match:
                yield i, match

    def split(self, string: str, start: int = 0, end: int = None) -> Tuple[str]:
        assert string
        if self.finite_state_machine is None:
            self.compile()
        if end is None:
            end = len(string)
        new_string = []
        position = start
        for i, match in self.search_all(string[start:end]):
            new_string.append(string[position:i])
            position = i + 1
        return tuple(new_string)

    def build(
            self,
            finite_state_machine: FiniteStateMachine,
            base_state: int,
            counter: int,
            end_state: int = None
    ) -> Tuple[int, int]:
        raise NotImplementedError
