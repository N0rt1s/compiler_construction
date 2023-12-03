import re


class tokenization:
    def __init__(self) -> None:
        self.patterns = [
            (r"#", "importer"),
            (
                r"\b(for|public|private|static|class|function|struct|new|return|break|continue|if|elif|else|while|for|forEach|in|switch|case|import)\b",
                "KeyWord",
            ),
            (r"\s*(number\[\]|char\[\]|bool\[\]|string\[\])\s*", "ArrayDataType"),
            (r"\b(number|char|bool|string)\b", "DataType"),
            (r'true|false$',"bool"),
            (r'^"[^"]*"$', "string"),
            (r"'(?:\\.|[^\\'])'", "char"),
            (r"[0-9]+", "number"),
            (r"\b[a-zA-Z_][a-zA-Z0-9_]*\b", "Id"),
            (r"[\[\],(){};:]", "Punctuators"),
            (r"==|!=|<=|>=|<|>", "RelationalOperators"),
            (r"\+\+|--", "IncDecOperator"),
            (r"[+\-=/*%]", "Operator"),
            (r"\s+", None),  # Ignore whitespace
            (r"\?\?[^\n]*", None),  # Ignore single-line comments
            (r"\?\*[\s\S]*?\*\?", None),  # Ignore multi-line comments
        ]

    def makeTokens(self,code):
        tokens = []
        while code:
            for pattern, token_type in self.patterns:
                match = re.match(pattern, code)
                if match:
                    value = match.group(0)
                    if token_type:
                        tokens.append({"class":token_type,"value":value.strip()})
                    code = code[len(value) :].lstrip()
                    break
            else:
                raise SyntaxError(f"Unexpected character: {code[0]}")

        return tokens



# testing
# code = """

#         number asd= aas + 12 - 78 < llls + 121;
#         for(number i= 30+32 ; 232<12;i++){
#             asd++;
#         }
#      }
# }
# """
# token= tokenization()
# tokens=token.makeTokens(code)
# for token in tokens:
#     print(token)
