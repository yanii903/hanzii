import json

with open('www/data/simplified/reading_hsk1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Tổng số đoạn văn: {len(data['dialogs'])}")

lengths = [len(d['lines'][0]['text']) for d in data['dialogs']]
print(f"Độ dài trung bình: {sum(lengths)//len(lengths)} ký tự")
print(f"Độ dài: từ {min(lengths)} đến {max(lengths)} ký tự")

# Check if all have pinyin and translation
complete = 0
for d in data['dialogs']:
    if d['lines'][0]['pinyin'] and d['lines'][0]['translation']:
        if 'TODO' not in d['lines'][0]['pinyin'] and 'TODO' not in d['lines'][0]['translation']:
            complete += 1

print(f"\nĐoạn văn có đầy đủ pinyin và dịch: {complete}/{len(data['dialogs'])}")

# Show topics
print(f"\nCác chủ đề:")
for i, d in enumerate(data['dialogs'], 1):
    print(f"  {i}. {d['topic']} - {d['description']}")
