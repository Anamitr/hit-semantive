import json


def read_hit_content(path="") -> dict:
    path = str(path)
    if path and path[-1] != '/':
        path += '/'
    file = open(path + ".hit/hit", 'r')
    result = json.load(file)
    file.close()
    return result


def save_hit_content(hit_content):
    with open('.hit/hit', 'w') as f:
        json.dump(hit_content, f, indent=4)
