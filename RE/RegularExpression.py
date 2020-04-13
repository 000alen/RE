from typing import *

from RE.FiniteAutomaton import FiniteAutomaton


class RegularExpression(FiniteAutomaton[str]):
    __counter__: int

    def __init__(self):
        super().__init__({0}, {-1})
        self.AddDefaultStates({-2})
        self.__counter__ = 0

    @property
    def counter(self):
        self.__counter__ += 1
        return self.__counter__

    def Build(self):
        pass

    def Literal(
        self,
        sequence: str
    ) -> Callable:
        def Build(
            initial_state: int,
            final_state: int = None
        ) -> int:            
            if final_state is not None:
                *sequence, last_element = sequence
            current_state = initial_state
            for element in sequence:
                new_state = self.counter
                self.AddTransition(element, current_state, new_state)
                current_state = new_state
            if final_state is not None:
                self.AddTransition(last_element, current_state, final_state)
            else:
                final_state = current_state
            return final_state
        return Build

    def Concatenation(
        self,
        *sequence: Callable
    ) -> Callable:
        def Build(
            initial_state: int,
            final_state: int = None
        ) -> int:
            if final_state is not None:
                *sequence, last_element = sequence
            current_state = initial_state
            for element in sequence:
                current_state = element(current_state)
            if final_state is not None:
                last_element(current_state, final_state)
            else:
                final_state = current_state
            return final_state
        return Build

    def Alternation(
        self,
        *sequence: Callable
    ) -> Callable:
        def Build(
            initial_state: int,
            final_state: int = None
        ) -> int:
            if final_state is None:
                element, *sequence = sequence
                final_state = element(initial_state)
            for element in sequence:
                element(initial_state, final_state)
            return final_state
        return Build

    def Kleene(
        self,
        *sequence: Callable
    ) -> Callable:
        def Build(
            initial_state: int,
            final_state: int = None
        ) -> int:
            *sequence, last_element = sequence
            if final_state is not None:
                first_element = sequence[0]
            current_state = initial_state
            for i, element in enumerate(sequence):
                current_state = element(current_state)
                if not i:
                    loop_state = current_state
            if final_state is not None:
                first_element(final_state, loop_state)
            else:
                final_state = initial_state
            last_element(current_state, final_state)
            return final_state
        return Build
