#!/usr/bin/env python3

# Automaton-based grep

import nfa
import regexp
import regular

class NFABuilder:
    union = staticmethod(regular.union)
    concat = staticmethod(regular.concat)
    star = staticmethod(regular.star)
    @staticmethod
    def symbol(a):
        return regular.singleton([a])
    @staticmethod
    def epsilon():
        return regular.singleton([])
    @staticmethod
    def group(a):
        return a

if __name__ == "__main__":
    import argparse
    import fileinput
    import sys
    
    argparser = argparse.ArgumentParser()
    argparser.add_argument('regexp', metavar='regexp', help='regular expression')
    argparser.add_argument('input', nargs='*', metavar='input', help='input file(s)')
    args = argparser.parse_args()

    try:
        m = regexp.parse(args.regexp, NFABuilder)
    except regexp.ParseError as e:
        sys.stderr.write("parse error: {}\n".format(e))
        sys.exit(1)

    for line in fileinput.input(args.input):
        w = line.rstrip('\n')
        flag, _ = nfa.match(m, w)
        if flag:
            print(w, flush=True)
