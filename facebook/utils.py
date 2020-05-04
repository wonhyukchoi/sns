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
    def __init__(self, title='TITLE'):
        self._md = ''
        self._md += '\n# {}\n'.format(title)

    def add_image(self, image: str):
        self._md += '\n![]({})'.format(image)

    def add_text(self, text: str):
        self._md += '\n' + text

    def add_table(self, data: dict):
        divisor = ' | '
        columns = data.keys()
        header = ['----'] * len(columns)

        column_data = list(data.values())
        num_rows = len(column_data[0])
        rows = []
        for i in range(num_rows):
            ith_row = []
            for j in range(len(columns)):
                ith_row.append(str(column_data[j][i]))
            rows.append(ith_row)

        table = divisor.join(columns) + '\n'
        table += divisor.join(header) + '\n'
        for each_row in rows:
            table += divisor.join(each_row) + '\n'

        self._md += table

    def write(self, file_name=''):
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(self._md)


if __name__ == "__main__":
    md = MarkdownGenerator()
    test_data = {'a': [1, 2], 'b': [3, 4], 'c': [5, 6]}
    md.add_table(test_data)
    md.write('test.md')
