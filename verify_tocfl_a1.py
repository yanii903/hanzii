import json

# Load data
vocab_entries = json.load(open('www/data/traditional/tocfl_a1.json', 'r', encoding='utf-8'))
reading_data = json.load(open('www/data/traditional/reading_tocfl_a1.json', 'r', encoding='utf-8'))

all_words = set([entry['hanzi'] for entry in vocab_entries['entries']])

# Count used words
used_words = set()
for dialog in reading_data['dialogs']:
    text = dialog['lines'][0]['text']
    for word in all_words:
        # Handle special cases with parentheses
        base_word = word.split('(')[0].strip() if '(' in word else word
        alt_word = word.split('(')[1].replace(')', '').strip() if '(' in word else None
        
        if base_word in text or (alt_word and alt_word in text):
            used_words.add(word)

missing = all_words - used_words
coverage = len(used_words) / len(all_words) * 100

print(f"Độ phủ từ vựng TOCFL A1: {coverage:.2f}%")
print(f"Số từ đã sử dụng: {len(used_words)}/{len(all_words)}")

if missing:
    print(f"\nCòn thiếu {len(missing)} từ:")
    for word in sorted(missing):
        print(f"  - {word}")
else:
    print("\n🎉 ĐÃ HOÀN THÀNH 100%!")
