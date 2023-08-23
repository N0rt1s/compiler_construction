import re

token_classes = [
    ("INTEGER", r'\d+'),
    ("IDENTIFIER", r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ("OPERATOR", r'\+|\-|\*|\/'),
    ("ASSIGNMENT", r'='),
    ("SEMICOLON", r';'),
    # ... other token classes ...
]

def tokenize(source_code):
    tokens = []
    position = 0

    while position < len(source_code):
        match = None
        for token_class, pattern in token_classes:
            regex = re.compile(pattern)
            match = regex.match(source_code, position)
            if match:
                value = match.group(0)
                tokens.append((token_class, value))
                position = match.end()
                break
        
        if not match:
            raise ValueError(f"Unrecognized token at position {position}")

    return tokens

source_code = "int x = 42 + y;"
tokens = tokenize(source_code)
print(tokens)
