#!/usr/bin/env python3

import regexp

class ASTPrinter:
    @staticmethod
    def union(a, b):
        return f'union({a},{b})'
    @staticmethod
    def concat(a, b):
        return f'concat({a},{b})'
    @staticmethod
    def star(a):
        return f'star({a})'
    @staticmethod
    def epsilon():
        return 'epsilon()'
    @staticmethod
    def symbol(a):
        return f'symbol("{a}")'

if __name__ == "__main__":
    import sys
    import argparse
    argparser = argparse.ArgumentParser()
    argparser.add_argument('regexp', metavar='regexp', help='regular expression')
    args = argparser.parse_args()

    try:
        tree = regexp.parse(args.regexp, ASTPrinter)
    except regexp.ParseError as e:
        sys.stderr.write("parse error: {}\n".format(e))
        sys.exit(1)
    print(tree)
