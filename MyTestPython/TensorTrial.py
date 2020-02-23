# test
from janome.tokenizer import Tokenizer
t = Tokenizer()
for token in t.tokenize('今日も一日がんばるぞい'):
    print(token.surface)

