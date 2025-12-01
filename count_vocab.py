import json

# Đếm số từ vựng trong mỗi cấp độ
levels = ['hsk1', 'hsk2', 'hsk3', 'hsk4', 'hsk5', 'hsk6']

for level in levels:
    try:
        with open(f'www/data/simplified/{level}.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f'{level.upper()}: {len(data["entries"])} từ')
    except FileNotFoundError:
        print(f'{level.upper()}: File không tồn tại')
