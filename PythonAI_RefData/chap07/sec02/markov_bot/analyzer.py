import re

from janome.tokenizer import Tokenizer


def analyze(text):
    t = Tokenizer()
    tokens = t.tokenize(text)
    result = []
    for token in tokens:
        result.append(
            [token.surface,
             token.part_of_speech])
    return(result)

def keyword_check(part):
    return re.match('名詞,(一般|固有名詞|サ変接続|形容動詞語幹)', part)

def parse(text):
    t = Tokenizer()
    tokens = t.tokenize(text)
    result = []
    for token in tokens:
        result.append(token.surface)
    return(result)