import json
import random

def load_vocab(level):
    """Load vocabulary from HSK level file"""
    with open(f'www/data/simplified/{level}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['entries']

def get_all_words(entries):
    """Extract all hanzi words from vocabulary entries"""
    words = set()
    for entry in entries:
        words.add(entry['hanzi'])
    return words

def check_coverage(passages, vocab_words):
    """Check which words are covered and which are missing"""
    used_words = set()
    for passage in passages:
        text = passage['lines'][0]['text']
        for word in vocab_words:
            if word in text:
                used_words.add(word)
    
    missing = vocab_words - used_words
    coverage = len(used_words) / len(vocab_words) * 100
    
    return used_words, missing, coverage

def analyze_reading_file():
    """Analyze the current reading.json file"""
    with open('reading.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Load HSK1 vocabulary
    vocab = load_vocab('hsk1')
    vocab_words = get_all_words(vocab)
    
    print(f"Tổng số từ HSK1: {len(vocab_words)}")
    print(f"Tổng số đoạn văn: {len(data['dialogs'])}")
    
    # Check coverage
    used_words, missing_words, coverage = check_coverage(data['dialogs'], vocab_words)
    
    print(f"\nĐộ phủ từ vựng: {coverage:.2f}%")
    print(f"Số từ đã sử dụng: {len(used_words)}")
    print(f"Số từ còn thiếu: {len(missing_words)}")
    
    if missing_words:
        print(f"\n{len(missing_words)} từ còn thiếu:")
        missing_list = sorted(list(missing_words))
        for i in range(0, len(missing_list), 10):
            print('  ', ', '.join(missing_list[i:i+10]))
    
    # Calculate average passage length
    lengths = []
    for passage in data['dialogs']:
        text = passage['lines'][0]['text']
        lengths.append(len(text))
    
    print(f"\nĐộ dài đoạn văn:")
    print(f"  Trung bình: {sum(lengths)/len(lengths):.0f} ký tự")
    print(f"  Ngắn nhất: {min(lengths)} ký tự")
    print(f"  Dài nhất: {max(lengths)} ký tự")

if __name__ == '__main__':
    analyze_reading_file()
