from RE.FiniteStateMachine import FiniteStateMachine

FSM = FiniteStateMachine(
    {0},
    {1},
    {-1}
)

for _ in [
    FSM.InputSet,
    FSM.StateSet,
    FSM.InitialStates,
    FSM.FinalStates,
    FSM.DefaultStates
]:
    print(_)
