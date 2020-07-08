from typing import *

from RE.FiniteStateMachine import FiniteStateMachine


class Operator:
    blocks: List["Operator"]

    def __init__(self):
        self.blocks = []

    def __add__(self, operator: "Operator"):
        self.blocks.append(operator)
        return self

    def match(self, string: str):
        pass

    def build(self, finite_state_machine: FiniteStateMachine, current_state: int, counter: int) -> Tuple[int, int]:
        raise NotImplementedError


class Literal(Operator):
    literal: str

    def __init__(self, literal: str):
        super().__init__()
        self.literal = literal

    def build(self, finite_state_machine: FiniteStateMachine, current_state: int, counter: int) -> Tuple[int, int]:
        finite_state_machine.add_transition(
            self.literal[0], current_state, counter)
        current_state = counter
        counter += 1
        for character in self.literal[1::]:
            finite_state_machine.add_transition(
                character, counter, counter + 1)
            counter += 1
        return counter, counter


class Optional(Operator):
    inner_blocks: List[Operator]

    # TODO: Check this
    def __init__(self, *inner_blocks: Operator):
        super().__init__()
        self.inner_blocks = inner_blocks

    def build(self, finite_state_machine: FiniteStateMachine, current_state: int, counter: int) -> Tuple[int, int]:
        return super().build(finite_state_machine, current_state, counter)


class Zero(Operator):
    inner_blocks: List[Operator]

    def __init__(self, *inner_blocks: Operator):
        super().__init__()
        self.inner_blocks = inner_blocks


class One(Operator):
    inner_blocks: List[Operator]

    def __init__(self, *inner_blocks: Operator):
        super().__init__()
        self.inner_blocks = inner_blocks


class Quantification(Operator):
    minimun: int
    maximun: int
    inner_blocks: List[Operator]

    def __init__(self, minimun: int, maximun: int, *inner_blocks: Operator):
        super().__init__()
        self.minimun = minimun
        self.maximun = maximun
        self.inner_blocks = inner_blocks


class Wildcard(Operator):
    def __init__(self):
        super().__init__()
