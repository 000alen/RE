from RE.RegularExpression import RegularExpression

expression = RegularExpression()
expression.AddSequence('1234')

for element, current_states in expression.Run(input()):
    print(current_states)

print(expression.InputSet)