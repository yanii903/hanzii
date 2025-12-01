import json
from opencc import OpenCC
from pypinyin import pinyin, Style

# Initialize converter
cc = OpenCC('s2t')  # Simplified to Traditional

def text_to_pinyin(text):
    """Convert Chinese text to pinyin"""
    result = pinyin(text, style=Style.TONE, heteronym=False)
    sentences = []
    current = []
    for item in result:
        syllable = item[0]
        current.append(syllable)
        if syllable in ['，', '。', '！', '？', '：', '；']:
            sentence = ' '.join(current[:-1])
            if sentence:
                sentence = sentence[0].upper() + sentence[1:] if len(sentence) > 0 else sentence
                sentences.append(sentence + syllable)
            current = []
    if current:
        sentence = ' '.join(current)
        sentence = sentence[0].upper() + sentence[1:] if len(sentence) > 0 else sentence
        sentences.append(sentence)
    return ' '.join(sentences)

def convert_to_traditional(data):
    """Convert reading data from simplified to traditional"""
    traditional_data = {"dialogs": []}
    
    for dialog in data['dialogs']:
        traditional_dialog = {
            "topic": cc.convert(dialog['topic']),
            "description": dialog['description'],  # Keep Vietnamese translation
            "lines": []
        }
        
        for line in dialog['lines']:
            traditional_text = cc.convert(line['text'])
            traditional_line = {
                "speaker": cc.convert(line['speaker']) if line['speaker'] else "",
                "text": traditional_text,
                "pinyin": text_to_pinyin(traditional_text),
                "translation": line['translation']
            }
            traditional_dialog['lines'].append(traditional_line)
        
        traditional_data['dialogs'].append(traditional_dialog)
    
    return traditional_data

# Load HSK1 reading data
with open('www/data/simplified/reading_hsk1.json', 'r', encoding='utf-8') as f:
    hsk1_data = json.load(f)

# Convert to traditional
tocfl_a1_data = convert_to_traditional(hsk1_data)

# Save TOCFL A1 reading data
with open('www/data/traditional/reading_tocfl_a1.json', 'w', encoding='utf-8') as f:
    json.dump(tocfl_a1_data, f, ensure_ascii=False, indent=2)

print(f"✓ Đã tạo file reading_tocfl_a1.json")
print(f"✓ Tổng số đoạn văn: {len(tocfl_a1_data['dialogs'])}")

# Check average length
lengths = [len(d['lines'][0]['text']) for d in tocfl_a1_data['dialogs']]
print(f"\nĐộ dài trung bình: {sum(lengths)//len(lengths)} ký tự")
print(f"Độ dài: từ {min(lengths)} đến {max(lengths)} ký tự")

# Check coverage with TOCFL A1 vocab
try:
    with open('www/data/traditional/tocfl_a1.json', 'r', encoding='utf-8') as f:
        vocab_data = json.load(f)
    
    all_words = set([entry['hanzi'] for entry in vocab_data['entries']])
    
    used_words = set()
    for dialog in tocfl_a1_data['dialogs']:
        text = dialog['lines'][0]['text']
        for word in all_words:
            if word in text:
                used_words.add(word)
    
    coverage = len(used_words) / len(all_words) * 100
    print(f"\nĐộ phủ từ vựng TOCFL A1: {coverage:.2f}%")
    print(f"Số từ đã sử dụng: {len(used_words)}/{len(all_words)}")
except Exception as e:
    print(f"\nKhông thể kiểm tra độ phủ từ vựng: {e}")
