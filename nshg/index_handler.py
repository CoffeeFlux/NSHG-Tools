import os, json, hashlib

def save_index(index, directory):
    with open(os.path.join(directory, '_index.json'), 'w') as index_file:
        index_file.write(json.dumps(index))

def load_index(directory):
    with open(os.path.join(directory, '_index.json'), 'r') as index_file:
        return json.loads(index_file.read())

def format_entry(node, data):
    return {
                'node': node,
                'hash': hashlib.sha256(data).hexdigest()
           }
