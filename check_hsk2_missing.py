import json

# Load HSK2 vocab
with open('www/data/simplified/hsk2.json', 'r', encoding='utf-8') as f:
    vocab_data = json.load(f)

all_words = set([entry['hanzi'] for entry in vocab_data['entries']])

# Load current reading data
with open('www/data/simplified/reading_hsk2.json', 'r', encoding='utf-8') as f:
    reading_data = json.load(f)

# Check which words are used
used_words = set()
for dialog in reading_data['dialogs']:
    text = dialog['lines'][0]['text']
    for word in all_words:
        if word in text:
            used_words.add(word)

missing = all_words - used_words

print(f"Còn thiếu {len(missing)} từ:")
missing_list = sorted(list(missing))
for i in range(0, len(missing_list), 10):
    print('  ', ', '.join(missing_list[i:i+10]))
