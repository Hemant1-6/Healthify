import json;

with open('blog_json.txt','r') as data:
    raw = data.read()
    data = json.loads(raw)

def blog_data():
 return data