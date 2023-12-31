import re


class tokenization:
    def __init__(self):
        self.operators = r"[+\-=/*%]"
        self.relationalOperators = r"(==|<=|>=|!=|<|>|!)"
        self.punctuators = r"[(){};]"
        self.keyWords = [
            "public",
            "private",
            "static",
            "class",
            "function",
            "struct",
            "new",
            "return",
            "break",
            "continue",
            "if",
            "else",
            "while",
            "for",
            "forEach",
            "switch",
            "case",
            "import"
        ]
        self.importer="#"
        self.dataTypes = ["number", "string", "char", "bool", "void"]
        self.arrayDataTypes = ["number[]", "string[]", "char[]"]
        self.inc_dec = ["++", "--"]
        self.quotes = r'["\']'
        self.Id = r"^[a-zA-Z_][a-zA-Z0-9_]*$"
        self.number = r"^[0-9.]*$"
        self.charConst = r"^[a-zA-Z0-9_]$"
        self.string = r'^"[^"]*"$'
        self.allTokens = []

    def makeParts(self, tokens):
        parts = []
        # print(tokens)
        for item in tokens:
            item=item.replace("\n","")
            dictionary1 = {"value": item}
            if(item==self.importer):
                dictionary1["class"] = "importer"
            elif re.match(self.relationalOperators, item):
                dictionary1["class"] = "RelationalOperators"
            elif re.match(self.operators, item):
                dictionary1["class"] = "Operator"
            elif re.match(self.punctuators, item):
                dictionary1["class"] = "Punctuators"
            elif item in self.keyWords:
                dictionary1["class"] = "KeyWord"
            elif item in self.dataTypes:
                dictionary1["class"] = "DataType"
            elif item in self.arrayDataTypes:
                dictionary1["class"] = "ArrayDataType"
            # elif re.search(r'["\']', item):
            #     dictionary1["class"] = "Quotes"
            elif re.match(self.Id, item):
                dictionary1["class"] = "Id"
            elif re.match(self.number, item):
                dictionary1["class"] = "number"
            elif re.match(self.charConst, item):
                dictionary1["class"] = "char"
            elif re.match(self.string, item):
                dictionary1["class"] = "string"
            else:
                dictionary1["class"] = "InvalidToken"
            parts.append(dictionary1)
        return parts

    def makeTokens(self, line):
        tokens = []
        token = ""
        line.replace("\n", "")
        # print("line=>", line)
        for item in line:
            # print("item=>",item," token=>",token)
            if item == " ":
                if token and token!="\n":
                    tokens.append(token.strip())
                token = ""
            elif token and re.match(self.quotes,token[0]):
                # print("token")
                if(token[0]==item):
                    token+=item
                    tokens.append(token.strip())
                    token = ""  
                else:    
                    token+=item

            elif (self.inc_dec.__contains__(token)):
                tokens.append(token.strip())
                tokens.append(item)
                token = ""

            elif re.match(f"{self.relationalOperators}", token):
                tokens.append(token.strip())
                token = ""

            elif (
                re.search(r'["\']', item)
                or re.match(f"[{re.escape(self.operators)}]", item)
                or re.match(f"[{re.escape(self.punctuators)}]", item)
                or re.match(f"[{re.escape(self.relationalOperators)}]", item)
                or re.match(self.quotes,item)
            ):
                if token == "=" and item == "=":
                    token += item
                elif token == "+" and item == "+":
                    token += item 
                elif token == "-" and item == "-":
                    token += item     
                else:
                    if token and token!="\n":
                        tokens.append(token.strip())
                        if(re.match(self.quotes,item) or item=="+" or item == "-"):
                            token = ""
                            token+=item
                            continue
                        else:
                            token = ""
                    if item == "=":
                        token = ""
                        token += item
                    elif re.match(f"[{re.escape(self.punctuators)}]", item):
                        tokens.append(item)
                    elif re.match(f"[{re.escape(self.relationalOperators)}]", item):
                        tokens.append(item)    
                    elif re.match(f"[{re.escape(self.operators)}]", item):
                        tokens.append(item)   
                    else:
                        if token and token!="\n" and not re.match(self.quotes,token):
                            tokens.append(item)
                            token = ""
            elif (
                token == "="
                and not re.match(f"[{re.escape(self.operators)}]", item)
            ):
                if token and token!="\n":
                    tokens.append(token)
                    token = ""
                    token += item

            else:
                token += item

        if token and token!="\n":
            tokens.append(token)

        return tokens
