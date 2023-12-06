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
            (r'"(?:[^\\"]|\\.)*"', "string"),
            (r"'(?:\\.|[^\\'])'", "char"),
            (r"-?\d*\.?\d+", "number"),
            (r"\b[a-zA-Z_][a-zA-Z0-9_]*\b", "Id"),
            (r"[\[\],(){};:.]", "Punctuators"),
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
                    if token_type == "number":
                        if len(tokens)!=0:
                            if value.__contains__("-") and tokens[-1]["value"] not in [";","(","=","==","<=",">=","<",">","[","+","-","*","/","%"]:
                                value="-"
                                tokens.append({"class": token_type, "value": value})
                                # tokens.extend(re.findall(r'-?\d+|\S', value))
                            else:        
                                tokens.append({"class": token_type, "value": value.strip()})
                        else:        
                            tokens.append({"class": token_type, "value": value.strip()})
                    elif token_type:
                        tokens.append({"class": token_type, "value": value.strip()})
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
code = """
interface ll{
    public char s,adsl,xc,asda;
    public char my();
}

public class bb{
    bb(){}
    public number mm=1;
    public number[] ms=1;
}

public class aa{
    aa(char st,number mm ) { }
    private char ml;
    public string ms="test";
}
"""

pattern = r'"([^"]*)"'

matches = re.findall(pattern, code)

for match in matches:
    print(f'Match: {match}')