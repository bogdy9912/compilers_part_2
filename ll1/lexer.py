import re

def lex(input, token_definitions):
    tokens = []
    i = 0
    while i < len(input):
        regex_match = None
        for token_expr in token_definitions:

            token_tag, regex_pattern = token_expr
            regex_obj = re.compile(regex_pattern)

            regex_match = regex_obj.match(input, i)
            if regex_match:
                lexeme = regex_match.group(0)
                if token_tag != None:
                    tokens.append((token_tag, lexeme))
                break

        if regex_match:
            j = regex_match.end(0)
            if i is j:
                break
            else:
                i = j
        else:
            raise PermissionError()
    return tokens
