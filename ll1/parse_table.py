class ll1_parse_table(dict):

    def __init__(self, grammer, start_sym, epsilon_sym):
        self.grammer = grammer

        self.START = start_sym
        self.EPSILON = epsilon_sym
        self.EOI = 'EOI'
        self.construct()

    def __repr__(self):
        table = 'Parse Table\n'
        for symbol in self.keys():
            table += symbol + ':\n'
            for first in self[symbol].keys():
                rule = ''
                line = '\t' + '{:<10}'.format(first + ':')
                for r in self[symbol][first]:
                    rule += r + ' '
                table += line + '[' + rule + ']\n'
        return table

    def construct(self):
        for symbol in self.grammer.keys():
            self[symbol] = {}

            firsts = self.first_set(symbol)
            follows = self.follow_set(symbol)
            for first in firsts:

                for rule in self.grammer[symbol]:
                    if first in self.first_set(rule[0]):
                        if first not in self[symbol]:
                            if first == self.EPSILON:

                                for follow in follows:
                                    self[symbol][follow] = [first]
                            else:
                                self[symbol][first] = rule
                        else:

                            raise BrokenPipeError()

    def first_set(self, symbol):
        firsts = []
        if symbol in self.grammer:
            rule_set = self.grammer[symbol]
            for rule in rule_set:

                if len(rule) > 0 and (rule[0] != symbol):
                    firsts = firsts + self.first_set(rule[0])
        else:

            firsts.append(symbol)
        return firsts

    def follow_set(self, symbol):
        follows = []

        if symbol == self.START:
            follows.append(self.EOI)
        for rule_symbol in self.grammer.keys():

            for rule in self.grammer[rule_symbol]:
                i = 0

                while i < len(rule):
                    if rule[i] == symbol:
                        if i + 1 < len(rule):
                            if rule[i + 1] not in self.grammer:
                                follows.append(rule[i + 1])
                            else:
                                for first in self.first_set(rule[i + 1]):
                                    if first == self.EPSILON:

                                        follows = follows + [x for x in iter(self.follow_set(rule_symbol)) if
                                                             x not in follows]
                                    elif first not in follows:
                                        follows.append(first)

                        elif rule_symbol != symbol:

                            follows = follows + [x for x in iter(self.follow_set(rule_symbol)) if x not in follows]
                    i = i + 1
        return follows
