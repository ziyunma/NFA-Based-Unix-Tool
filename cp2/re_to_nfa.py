#!/usr/bin/env python3

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
    import sys
    
    argparser = argparse.ArgumentParser()
    argparser.add_argument('regexp', metavar='regexp', help='regular expression')
    args = argparser.parse_args()

    try:
        m = regexp.parse(args.regexp, NFABuilder)
    except regexp.ParseError as e:
        sys.stderr.write("parse error: {}\n".format(e))
        sys.exit(1)
    nfa.write(m, sys.stdout)
    
