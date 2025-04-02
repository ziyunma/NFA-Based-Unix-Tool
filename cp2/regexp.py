from collections import namedtuple
import nfa

class ParseError(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)

Symbol = namedtuple('Symbol', ['name'])
Expr = Symbol('E')
MaybeTerm = Symbol('M')
Term = Symbol('T')
Factor = Symbol('F')
Primary = Symbol('P')
Bottom = Symbol('$')
End = Symbol('⊣')

def parse(s, sem):
    toks = list(s) + [End]
    stack = [Bottom]
    values = []
    pos = 0

    while True:
        # Just for error messages
        if toks[pos] == End:
            next = "end of string"
        else:
            next = toks[pos]

        # reduce S → $ E
        if stack == [Bottom, Expr] and toks[pos:] == [End]:
            return values[-1]

        # reduce E → E | M
        elif stack[-3:] == [Expr, '|', MaybeTerm]:
            stack[-3:] = [Expr]
            values[-2:] = [sem.union(values[-2], values[-1])]

        # reduce E → M
        elif stack[-1:] == [MaybeTerm] and stack[-2] in [Bottom, '(']:
            stack[-1:] = [Expr]

        # reduce M → ε
        elif stack[-1] in [Bottom, '(', '|'] and toks[pos] in ['|', ')', End]:
            stack.append(MaybeTerm)
            values.append(sem.epsilon())
        
        # reduce M → T
        elif stack[-1:] == [Term] and toks[pos] in ['|', ')', End]:
            stack[-1:] = [MaybeTerm]

        # reduce T → T F
        elif stack[-2:] == [Term, Factor]:
            stack[-2:] = [Term]
            values[-2:] = [sem.concat(values[-2], values[-1])]

        # reduce T → F
        elif stack[-1:] == [Factor] and stack[-2] in [Bottom, '(', '|']:
            stack[-1:] = [Term]

        # reduce F → P *
        elif stack[-2:] == [Primary, '*']:
            stack[-2:] = [Factor]
            values[-1] = sem.star(values[-1])

        # reduce F → P
        elif stack[-1] == Primary and toks[pos] != '*':
            stack[-1] = Factor

        # reduce P → a
        elif isinstance(stack[-1], str) and stack[-1] not in ['(', ')', '|', '*', '\\']:
            sym = stack[-1]
            stack[-1] = Primary
            values.append(sem.symbol(sym))

        # reduce P → ( E )
        elif stack[-3:] == ['(', Expr, ')']:
            stack[-3:] = [Primary]
            values[-1] = values[-1]

        # shift a or (
        elif stack[-1] in [Term, '(', '|', Bottom]:
            if toks[pos] not in [')', '|', '*']:
                stack.append(toks[pos])
                pos += 1
            else:
                raise ParseError(f'expected symbol or ( but found {next}')

        # shift ) or |
        elif stack[-1] == Expr:
            if toks[pos] in [')', '|']:
                stack.append(toks[pos])
                pos += 1
            else:
                raise ParseError(f'expected ) or | but found {next}')

        # shift *
        elif stack[-1] == Primary:
            if toks[pos] == '*':
                stack.append(toks[pos])
                pos += 1
            else:
                raise ParseError(f'expected * but found {next}')

        else:
            raise ParseError(f'unexpected {next}')
