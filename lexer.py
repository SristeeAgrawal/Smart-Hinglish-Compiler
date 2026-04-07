
import re

#  Updated Token Patterns
token_specification = [
    ('KEYWORD', r'\b(bolo|likho|dikhao|agar|warna|jabtak|ke_liye|function|input_lo)\b'),
    ('NUMBER', r'\b\d+\b'),
    ('STRING', r'\".*?\"'),
    ('IDENTIFIER', r'\b[a-zA-Z_]\w*\b'),
    ('OPERATOR', r'[+\-*/><=]+'),
    ('NEWLINE', r'\n'),
    ('SKIP', r'[ \t]+'),
]

#  Combine all patterns into one regex
tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)

def tokenize(code):
    tokens = []

    for match in re.finditer(tok_regex, code):
        kind = match.lastgroup
        value = match.group()

        if kind == "SKIP":
            continue

        tokens.append((kind, value))

    return tokens

