import json


with open('list_marks.json', 'r', encoding='utf-8') as file:
    content = file.read()
    data = json.loads(content.replace('\n', '').replace('\r', ''))
    list_data = list(set([val.lower() for val in data['marks']]))
    with open('list_marks2.json', 'w', encoding='utf-8') as file:
        json.dump({'marks': list_data}, file)
