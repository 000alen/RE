from typing import *

from RE.FiniteStateMachine import FiniteStateMachine


class Operator:
    blocks: List["Operator"]

    def __init__(self):
        self.blocks = []

    def __add__(self, operator: "Operator"):
        self.blocks.append(operator)
        return self

    def __or__(self, operator: "Operator"):
        return Optional(self, operator)

    def match(self, string: str):
        assert string != ""
        finite_state_machine = FiniteStateMachine({0})
        base_state, counter = self.build(finite_state_machine, 0, 1)
        for block in self.blocks:
            base_state, counter = block.build(finite_state_machine, base_state, counter)
        finite_state_machine.add_final_states({base_state})
        return finite_state_machine.accepts(string)

    def build(
        self, 
        finite_state_machine: FiniteStateMachine, 
        base_state: int, 
        counter: int, 
        end_state: int = None
    ) -> Tuple[int, int]:
        raise NotImplementedError


class Literal(Operator):
    literal: str

    def __init__(self, literal: str):
        super().__init__()
        self.literal = literal

    def build(
        self, 
        finite_state_machine: FiniteStateMachine, 
        base_state: int, 
        counter: int,
        end_state: int = None
    ) -> Tuple[int, int]:
        for i, character in enumerate(self.literal, 1):
            if i == len(self.literal) and end_state is not None:
                finite_state_machine.add_transition(
                    character, 
                    base_state, 
                    {end_state}
                )
                return end_state, counter
            finite_state_machine.add_transition(
                character, 
                base_state, 
                {counter}
            )
            base_state = counter
            counter += 1
        return base_state, counter


class Optional(Operator):
    inner_blocks: List[Operator]

    # TODO: Check this
    def __init__(self, *inner_blocks: Operator):
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


class Zero(Operator):
    inner_blocks: List[Operator]

    def __init__(self, *inner_blocks: Operator):
        super().__init__()
        self.inner_blocks = inner_blocks

    def build(
        self, 
        finite_state_machine: FiniteStateMachine, 
        base_state: int, 
        counter: int, 
        end_state: int = None
    ):
        initial_state = base_state
        for i, inner_block in enumerate(self.inner_blocks, 1):
            if i == 1 and end_state is not None:
                loop_state = counter
            if i == len(self.inner_blocks):
                if end_state is None:
                    _, counter = inner_block.build(
                        finite_state_machine,
                        base_state,
                        counter,
                        initial_state
                    )
                    return initial_state, counter
                else:
                    for element, to_state in finite_state_machine.get_state(initial_state):
                        if to_state == {loop_state}:
                            finite_state_machine.add_transition(element, end_state, {loop_state})
                    return end_state, counter
            base_state, counter = inner_block.build(
                finite_state_machine,
                base_state,
                counter
            )
        return initial_state, counter
            

class One(Operator):
    inner_blocks: List[Operator]

    def __init__(self, *inner_blocks: Operator):
        super().__init__()
        self.inner_blocks = inner_blocks

    def build(
        self, 
        finite_state_machine, 
        base_state, 
        counter, 
        end_state=None
    ):
        for i, inner_block in enumerate(self.inner_blocks, 1):
            if i == len(self.inner_blocks):
                base_state, counter = inner_block.build(
                    finite_state_machine,
                    base_state,
                    counter,
                    end_state
                )
            else:
                base_state, counter = inner_block.build(
                    finite_state_machine,
                    base_state,
                    counter
                )
        _, counter = Zero(*self.inner_blocks).build(
            finite_state_machine,
            base_state,
            counter
        )
        return base_state, counter


class Quantification(Operator):
    minimun: int
    maximun: int
    inner_blocks: List[Operator]

    def __init__(self, minimun: int, maximun: int, *inner_blocks: Operator):
        super().__init__()
        self.minimun = minimun
        self.maximun = maximun
        self.inner_blocks = inner_blocks


class Group(Operator):
    pass


class Wildcard(Operator):
    def __init__(self):
        super().__init__()
