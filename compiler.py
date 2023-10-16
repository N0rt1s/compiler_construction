
from Tokenization import tokenization
tokenizer = tokenization()
allTokens=[]
with open("CFG.txt", "r") as file:    
    lines = file.readlines()

with open('testing.tx', 'r') as file:
    for line in file:
        if len(line.strip()) != 0:
            tokens=tokenizer.makeTokens(line)
            allTokens.extend(tokens)

parts = tokenizer.makeParts(allTokens)
for item in parts:
    print(f"Class: {item['class']}, Value: {item['value']}")

def check_parsing(token):
    token_index=0
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
                elif token=="null":
                    break
                else:
                    print(allTokens[token_index])


                    


# def parse_line(token):
#     valid_indic = [i for i, s in enumerate(lines) if s.startswith("#"+token)]
#     print(lines[valid_indic[0]])

# print(content.split(" "))

# check_parsing("<Start>")
# print(parts)
# Example Usage:
