from typing import TypeVar, Generic, Set, Dict, List, Iterator, Tuple


ElementType = TypeVar('ElementType')


class FiniteAutomaton(Generic[ElementType]):
    __initial_states__: Set[int]
    __final_states__: Set[int]
    __default_states__: Set[int]

    __transitions__: Dict[ElementType, Dict[int, Set[int]]]

    def __init__(
        self,
        initial_states: Set[int] = set(),
        final_states: Set[int] = set(),
        default_states: Set[int] = set()
    ):
        super().__init__()
        self.__initial_states__ = initial_states
        self.__final_states__ = final_states
        self.__default_states__ = default_states
        self.__transitions__ = {}

    @property
    def InputSet(self) -> Set[ElementType]:
        return set(self.__transitions__)

    @property
    def InitialStates(self) -> Set[int]:
        return self.__initial_states__

    @property
    def FinalStates(self) -> Set[int]:
        return self.__final_states__

    @property
    def DefaultStates(self) -> Set[int]:
        return self.__default_states__

    def AddInitialStates(
        self,
        initial_states: Set[int]
    ):
        self.__initial_states__.update(initial_states)

    def RemoveInitialStates(
        self,
        initial_states: Set[int] = None
    ):
        if initial_states is not None:
            self.__initial_states__.difference_update(initial_states)
        else:
            self.__initial_states__.clear()

    def AddFinalStates(
        self,
        final_states: Set[int]
    ):
        self.__final_states__.update(final_states)

    def RemoveFinalStates(
        self,
        final_states: Set[int] = None
    ):
        if final_states is not None:
            self.__final_states__.difference_update(final_states)
        else:
            self.__final_states__.clear()

    def AddDefaultStates(
        self,
        default_states: Set[int]
    ):
        self.__default_states__.update(default_states)

    def RemoveDefaultStates(
        self,
        default_states: Set[int] = None
    ):
        if default_states is not None:
            self.__default_states__.difference_update(default_states)
        else:
            self.__default_states__.clear()

    def HasTransition(
        self,
        element: ElementType,
        from_state: int,
        to_states: Set[int] = None
    ) -> bool:
        context = element in self.__transitions__ \
            and from_state in self.__transitions__[element]
        if to_states is not None:
            return context and to_states in self.__transitions__[element][from_state]
        return context

    def AddTransition(
        self,
        element: ElementType,
        from_state: int,
        to_states: Set[int]
    ):
        if self.HasTransition(element, from_state):
            self.__transitions__[element][from_state].update(to_states)
        elif element in self.InputSet:
            self.__transitions__[element][from_state] = to_states
        else:
            self.__transitions__[element] = {from_state: to_states}

    def GetTransition(
        self,
        element: ElementType,
        from_state: int
    ) -> Set[int]:
        if self.HasTransition(element, from_state):
            return self.__transitions__[element][from_state]
        return self.__default_states__

    def RemoveTransition(
        self,
        element: ElementType,
        from_state: int,
        to_states: Set[int]
    ):
        assert self.HasTransition(element, from_state)
        self.__transitions__[element][from_state].difference_update(to_states)
        if not self.__transitions__[element][from_state]:
            del self.__transitions__[element][from_state]

    def HasState(
        self,
        state: int
    ) -> bool:
        return any(
            state in to_states
            for to_states in connections.values()
            for connections in self.__transitions__.values()
        )

    def AddState(
        self,
        state: int,
        connections: Dict[ElementType, Set[int]]
    ):
        for element, to_states in connections.items():
            self.AddTransition(element, state, to_states)

    def GetState(
        self,
        state: int
    ) -> Dict[ElementType, Set[int]]:
        return {
            element: to_states
            for from_state, to_states in self.__transitions__[element].items()
            if from_state == state
            for element in self.__transitions__
        }

    def RemoveState(
        self,
        state: int
    ):
        for element in self.__transitions__:
            for from_state, to_states in self.__transitions__[element].items():
                if state in to_states:
                    self.RemoveTransition(element, from_state, state)
                if from_state == state:
                    del self.__transitions__[element][state]
                if not self.__transitions__[element]:
                    del self.__transitions__[element]

    def Run(
        self,
        sequence: List[ElementType]
    ) -> Iterator[Tuple[ElementType, Set[int]]]:
        current_states = self.__initial_states__
        for element in sequence:
            current_states = {
                *self.GetTransition(element, state)
                for state in current_states
            }
            yield element, current_states

    def Last(
        self,
        sequence: List[ElementType]
    ) -> Set[input]:
        for _, last_states in self.Run(sequence):
            pass
        return last_states

    def Accept(
        self,
        sequence: List[ElementType]
    ) -> Set[int]:
        last_states = self.Last(sequence)
        return self.__final_states__.intersection(last_states)
