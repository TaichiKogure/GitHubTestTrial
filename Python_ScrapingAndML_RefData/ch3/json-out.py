import json

price = {
    "date": "2017-05-10",
    "price": {
        "Apple": 80,
        "Orange": 55,
        "Banana": 40
    }}

s = json.dumps(price)
print(s)

