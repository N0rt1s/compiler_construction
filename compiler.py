import re
from Tokenization import tokenization
# Regular expression patterns
Id = r"^[a-zA-Z_][a-zA-Z0-9_]*$"
numConst = r"^[0-9.]*$"
charConst = r"^[a-zA-Z0-9_]$"
strConst = r'^"[^"]*"$'
tokenizer = tokenization()
allTokens=[]
with open("CFG.txt", "r") as file:    
    lines = file.readlines()

with open('testing.tx', 'r') as file:
    for line in file:
        if len(line.strip()) != 0:
            tokens=tokenizer.makeTokens(line)
            allTokens.extend(tokens)


def check_parsing(token):
    valid_indic = [i for i, s in enumerate(lines) if s.startswith("#"+token)]
    print(lines[valid_indic[0]])
    paths = lines[valid_indic[0]].split("-->")[1].split("|")
    for item in paths:
        parseTokens = item.split(" ")
        print(parseTokens)
        for i in range(len(parseTokens)):
            token = parseTokens[i].replace("\n", "")
            if token != "":
                if token[0] == "<":
                    check_parsing(token)
                    


# def parse_line(token):
#     valid_indic = [i for i, s in enumerate(lines) if s.startswith("#"+token)]
#     print(lines[valid_indic[0]])

# print(content.split(" "))

# check_parsing("<Start>")
parts = tokenizer.makeParts(allTokens)
# print(parts)
for item in parts:
    print(f"Class: {item['class']}, Value: {item['value']}")
# Example Usage:
