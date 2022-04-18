from ll1 import lexer, log


class ll1_parser(object):
    def __init__(self, lexemes, parse_table):
        self.table = parse_table
        self.lexemes = lexemes

    def parse(self, input):
        tokens = lexer.lex(input, self.lexemes)
        if len(tokens) <= 0:
            log.error('No TOKENS')
            return None

        tokens.append((self.table.EOI, None))
        self.validate(tokens)

        root = self.parse_token([self.table.START, None], tokens)
        return root

    def parse_token(self, root, tokens):
        if len(tokens) <= 0: return root

        if root != None:
            root_tag = root[0]
            root_value = root[1]
            next_token = tokens[0]
            next_tag = next_token[0]
            next_value = next_token[1]
            if root_tag == next_tag:
                tokens.pop(0)
                return next_token
            elif root_tag in self.table and next_tag in self.table[root[0]]:
                value = []
                if self.table[root_tag][next_tag] == None:
                    log.error('ERROR: No Rule for ROOT:' + str(root_tag))
                    return None

                for rule_tag in self.table[root_tag][next_tag]:

                    if rule_tag != self.table.EPSILON:

                        rule_token = self.parse_token([rule_tag, None], tokens)

                        if rule_token != None and len(rule_token) > 1:

                            value.append(rule_token)
                        else:
                            log.error("Could not parse rule")
                            return None
                    else:
                        value.append(None)
                root[1] = value
        return root

    def validate(self, tokens):
        token_stack = [(self.table.START, None)]
        index = 0
        valid = True
        while len(token_stack) > 0 and valid:
            top_token = token_stack[-1]
            if top_token[0] == tokens[index][0]:
                token_stack.pop()
                index += 1
            elif tokens[index][0] in self.table[top_token[0]]:
                rule = []
                for symbol in self.table[top_token[0]][tokens[index][0]]:
                    rule.append(symbol)
                token_stack.pop()
                if rule[0] != self.table.EPSILON:
                    while len(rule) > 0:
                        token_stack.append((rule[-1], None))
                        rule.pop()
            else:
                valid = False
        if valid:
            log.debug('VALIDATION: SUCCESS')

        return valid

    def print_tree(self, root):
        print(self.print_tree_str(root))

    def print_tree_str(self, root, i=0):
        if root is not None:
            tag = root[0]
            value_list = root[1]
            if tag in self.table:
                if value_list is not None:
                    for value in value_list:
                        try:
                            if value[1][0] is not None:
                                print(list(self.table.keys()).index(value[0]))
                        except:
                            pass
                        self.print_tree_str(value, i + 1)

        return ''
