import json

with open('www/data/traditional/tocfl_a1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    print(f'Tổng số từ TOCFL A1: {len(data["entries"])}')
