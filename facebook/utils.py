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


class MarkdownGenerator:
    def __init__(self):
        self._md = None

    def add_image(self, image: str):
        self._md += '\n![]({})'.format(image)

    def add_text(self, text: str):
        self._md += '\n' + text

    def add_table(self):
        raise NotImplementedError

    def write(self, file_name=''):
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(self._md)
