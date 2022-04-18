
from ll1 import log
from ll1 import parser
from ll1 import parse_table

def ll1_init(grammar, start_sym, epsilon_sym, lexemes):
    table = parse_table.ll1_parse_table(grammar, start_sym, epsilon_sym)
    return parser.ll1_parser(lexemes, table)


def ll1_load_grammar(grammar_filename, start_sym, epsilon_sym):

    lexemes = []
    rule_map = {}
    file = open(grammar_filename)
    if file != None:
        i = 0
        lines = file.read().split('$')
        for line in lines:
            production = line.split(':=')
            if len(production) == 2:

                symbol = production[0].strip()
                rule_list = []
                has_rule = True

                for rules in production[1].split('|'):
                    rule = []
                    rules = rules.strip()
                    if rules[0] == '\'':
                        definition = rules.split('\'')
                        if len(definition) == 3:
                            if symbol.lower().strip() == 'none':
                                symbol = None
                            lexemes.append((symbol, str(definition[1])))
                            has_rule = False
                    else:
                        for rule_symbol in rules.split(' '):
                            if rule_symbol != '':
                                rule.append(rule_symbol)
                        rule_list.append(rule)
                if has_rule:
                    rule_map[symbol] = rule_list
    else:
        print("Could not open Grammar File ", grammar_filename)
        return None
    return ll1_init(rule_map, start_sym, epsilon_sym, lexemes)
