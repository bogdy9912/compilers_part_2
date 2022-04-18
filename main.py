
from ll1 import parse_table
from ll1 import parser
from ll1 import *
from ll1 import log

def main():
    with open('input.txt') as f:
        lines = f.readlines()

    try:
        ll1_parser = ll1_load_grammar('grammar.txt', 'START', 'EPSILON')
        for line in lines:
            try:
                parse_root = ll1_parser.parse(line)

                ll1_parser.print_tree(parse_root)
            except PermissionError:
                log.debug("VALIDATION: FAILURE")
    except BrokenPipeError:
        log.debug("GRAMMAR INVALID FOR LL1")

    print(ll1_parser.table)


if __name__ == "__main__":
    main()
