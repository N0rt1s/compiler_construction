
from Tokenization import tokenization
from parse import Parser

tokenizer = tokenization()

allTokens=[]
with open('testing.tx', 'r') as file:
    code=file.read()
tokens = tokenizer.makeTokens(code)
# for item in parts:
#     print(f"Class: {item['class']}, Value: {item['value']}")
def check_parsing():
    cfg_parser = Parser(tokens) 
    cfg_parser.start()

check_parsing()



