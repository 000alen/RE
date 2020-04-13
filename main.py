from RE.RegularExpression import RegularExpression

e = RegularExpression()

e.Concatenation(
    e.Literal('Hola, '),
    e.Alternation(e.Literal('Alen'), e.Literal('Mundo')),
    e.Kleene(e.Literal('!'))
)

print(e.__transitions__)