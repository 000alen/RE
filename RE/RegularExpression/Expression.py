from typing import List, Tuple, Iterator

from RE.FiniteStateMachine import FiniteStateMachine

__all__ = (
    "Expression"
)


# TODO: Use abc.ABCMeta and @abstractmethod
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
        """Expression: Returns a concatenation (Group) of this RE (self) and the other RE (expression)."""
        from RE.RegularExpression.Group import Group
        if isinstance(expression, Group):
            expression.blocks.insert(0, self)
            return expression
        return Group(self, expression)

    def repeat(self, i: int) -> "Expression":
        """Expression: Returns a repetition (Group) of this RE (self)."""
        from RE.RegularExpression.Group import Group
        return Group(self).repeat(i)

    def alternate(self, expression: "Expression") -> "Expression":
        """Expression: Returns a alternation (Choose) of this RE (self) and the other RE (expression)."""
        from RE.RegularExpression.Choose import Choose
        return Choose(self, expression)

    def compile(self, recompile=False):
        """Generates the FSM."""
        if self.finite_state_machine is None or recompile:
            self.finite_state_machine = FiniteStateMachine(
                initial_states={0}
            )
            base_state, counter = self.build(self.finite_state_machine, 0, 1)
            self.finite_state_machine.add_final_states({base_state})

    def match(self, string: str, start: int = 0, end: int = None) -> str:
        """str: Returns the first match of this RE (self) in the string."""
        assert string
        self.compile()
        end = len(string) if end is None else end
        last_match = None
        for position in range(start + 1, end + 1):
            if self.finite_state_machine.accepts(string[start:position]):
                last_match = string[start:position]
        if last_match:
            return last_match

    def match_all(self, string: str, start: int = 0, end: int = None) -> Iterator[str]:
        """iter of str: Yields the matches of this RE (self) in the string."""
        assert string
        self.compile()
        end = len(string) if end is None else end
        while start < end:
            last_match = None
            for position in range(start + 1, end + 1):
                if self.finite_state_machine.accepts(string[start:position]):
                    last_match = string[start:position]
            if last_match:
                yield last_match
                start += len(last_match)
            start += 1

    def search(self, string: str, start: int = 0, end: int = None) -> Tuple[int, str]:
        """tuple of int and str: Returns the first match and its position of this RE (self) in the string."""
        assert string
        self.compile()
        end = len(string) if end is None else end
        while start < end:
            last_match = None
            for position in range(start + 1, end + 1):
                if self.finite_state_machine.accepts(string[start:position]):
                    last_match = string[start:position]
            if last_match:
                return start, last_match
            start += 1

    def search_all(self, string: str, start: int = 0, end: int = None) -> Iterator[Tuple[int, str]]:
        """iter of tuple of int and str: Yields all the matches and its positions of this RE (self) in the string."""
        assert string
        self.compile()
        end = len(string) if end is None else end
        while start < end:
            last_match = None
            for position in range(start + 1, end + 1):
                if self.finite_state_machine.accepts(string[start:position]):
                    last_match = string[start:position]
            if last_match:
                yield start, last_match
                start += len(last_match)
            start += 1

    def split(self, string: str, start: int = 0, end: int = None) -> Tuple[str]:
        """tuple of str: Returns sequence that is separated in the matches of this RE (self) from the string."""
        assert string
        self.compile()
        end = len(string) if end is None else end
        new_sequence = []
        position = None
        match = None
        for position, match in self.search_all(string, start, end):
            new_sequence.append(
                string[start:position]
            )
            start += len(match) + 1
        new_sequence.append(string[position + len(match):end])
        return tuple(new_sequence)

    def build(
            self,
            finite_state_machine: FiniteStateMachine,
            base_state: int,
            counter: int,
            end_state: int = None
    ) -> Tuple[int, int]:
        """tuple of int and int: Builds the expression in the FSM."""
        raise NotImplementedError
