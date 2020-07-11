from typing import List, Tuple

from RE.FiniteStateMachine import FiniteStateMachine


__all__ = (
    "Expression",
    "Group",
    "Literal",
    "Optional",
    "Zero",
    "One",
    "Quantification",
    "Wildcard"
)


class Expression:
    finite_state_machine: FiniteStateMachine
    blocks: List["Operator"]

    def __init__(self):
        self.finite_state_machine = None
        self.blocks = []

    def __add__(self, expression: "Expression"):
        if isinstance(self, Group):
            if isinstance(expression, Group):
                self.blocks += expression.blocks
            else:
                self.blocks.append(expression)
            return self
        elif isinstance(expression, Group):
            expression.blocks.insert(0, self)
            return expression
        return Group(self, expression)

    def __mul__(self, i: int):
        if isinstance(self, Group):
            return Group(*(self.blocks * i))
        else:
            return Group(self).__mul__(i)

    def __or__(self, operator: "Operator"):
        return Optional(self, operator)

    def compile(self):
        self.finite_state_machine = FiniteStateMachine(
            {0}, default_states={-1})
        base_state, counter = self.build(self.finite_state_machine, 0, 1)
        for block in self.blocks:
            base_state, counter = block.build(
                self.finite_state_machine, base_state, counter)
        self.finite_state_machine.add_final_states({base_state})

    def match(self, string: str):
        assert string != ""
        if self.finite_state_machine is None:
            self.compile()
        return self.finite_state_machine.accepts(string)

    def build(
        self,
        finite_state_machine: FiniteStateMachine,
        base_state: int,
        counter: int,
        end_state: int = None
    ) -> Tuple[int, int]:
        raise NotImplementedError


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
    ):
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


class Literal(Expression):
    literal: str

    def __init__(self, literal: str):
        super().__init__()
        self.literal = literal

    def __add__(self, expression: Expression):
        if isinstance(expression, Literal):
            self.literal += expression.literal
            return self
        return super().__add__(expression)

    def build(
        self,
        finite_state_machine: FiniteStateMachine,
        base_state: int,
        counter: int,
        end_state: int = None
    ) -> Tuple[int, int]:
        for i, character in enumerate(self.literal, 1):
            finite_state_machine.add_transition(
                character,
                base_state,
                {end_state}
                if i == len(self.literal) and end_state is not None
                else {counter}
            )
            if i == len(self.literal) and end_state is not None:
                return end_state, counter
            base_state = counter
            counter += 1
        return base_state, counter


class Optional(Expression):
    inner_blocks: List[Expression]

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
        for i, inner_block in enumerate(self.inner_blocks, 1):
            end_state, counter = inner_block.build(
                finite_state_machine,
                base_state,
                counter,
                end_state
            )
        return end_state, counter


class Zero(Expression):
    inner_blocks: List[Expression]

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


class One(Expression):
    inner_blocks: List[Expression]

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


class Quantification(Expression):
    exact: int
    minimum: int
    maximum: int
    inner_blocks: List[Expression]

    def __init__(self, *inner_blocks: Expression, exact: int = None, minimum: int = None, maximum: int = None):
        super().__init__()
        if exact == minimum == maximum == None:
            raise Exception
        self.exact = exact
        self.minimum = minimum
        self.maximum = maximum
        self.inner_blocks = inner_blocks

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
            base_state, counter = Optional(
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
            base_state, counter = Optional(
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


class Wildcard(Expression):
    pass
