
from Tokenization import tokenization
from cfg import cfg

tokenizer = tokenization()

allTokens=[]
with open("CFG.txt", "r") as file:    
    lines = file.readlines()

with open('testing.tx', 'r') as file:
    code=file.read()
tokens = tokenizer.makeTokens(code)
# for item in parts:
#     print(f"Class: {item['class']}, Value: {item['value']}")
def check_parsing():
    cfg_parser = cfg(tokens) 
    cfg_parser.start()

check_parsing()



