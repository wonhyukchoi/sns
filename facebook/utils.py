import os
import json


def json_files_to_list(path, msg='messages') -> list:
    file_names = [name for name in os.listdir(path)
                  if name.endswith('.json')]
    messages = []
    for json_file in file_names:
        file_path = os.path.join(path, json_file)
        with open(file_path, 'r', encoding='utf-8') as f:
            messages += json.load(f)[msg]
    return messages
