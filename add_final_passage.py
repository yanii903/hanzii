import json
from pypinyin import pinyin, Style

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

# Đoạn văn thứ 13 sử dụng 6 từ còn thiếu: 儿子, 先生, 哪里/哪儿, 小姐, 本, 读
new_passage = {
    "topic": "在图书馆",
    "description": "Ở thư viện",
    "text": "今天下午，我去图书馆。图书馆在哪儿？就在学校后面。我进去以后，看见一位小姐在前台工作。我问她：小姐，请问中文书在哪里？她很好，她说：中文书在二楼，你上去就看见了。我说谢谢。我上楼，看到很多书。我想买三本书，一本汉语书，一本英语书，还有一本数学书。我很喜欢读书。我在图书馆坐下，开始读书。这时候，我看见我的老师王先生也在这里。王先生是我的汉语老师。他有一个儿子，他的儿子也在这个学校学习。王先生看见我，他说：小明，你也在这里读书吗？我说：是的，王先生，我很喜欢来图书馆读书。王先生说：很好，多读书对你有好处。我们一起看书。图书馆很安静，很适合学习。我很喜欢图书馆。",
    "translation": "Chiều nay, tôi đi thư viện. Thư viện ở đâu? Ngay phía sau trường. Sau khi tôi vào, thấy một cô ở quầy làm việc. Tôi hỏi cô ấy: Cô ơi, cho hỏi sách tiếng Trung ở đâu? Cô ấy rất tốt, cô ấy nói: Sách tiếng Trung ở tầng 2, bạn lên là thấy. Tôi nói cảm ơn. Tôi lên lầu, thấy rất nhiều sách. Tôi muốn mua ba quyển sách, một quyển sách tiếng Hán, một quyển sách tiếng Anh, còn có một quyển sách toán. Tôi rất thích đọc sách. Tôi ngồi xuống ở thư viện, bắt đầu đọc sách. Lúc này, tôi thấy giáo viên của tôi ông Vương cũng ở đây. Ông Vương là giáo viên tiếng Hán của tôi. Ông có một con trai, con trai của ông cũng học ở trường này. Ông Vương thấy tôi, ông nói: Tiểu Minh, em cũng đọc sách ở đây à? Tôi nói: Vâng, thầy Vương, em rất thích đến thư viện đọc sách. Ông Vương nói: Rất tốt, đọc nhiều sách có lợi cho em. Chúng tôi cùng xem sách. Thư viện rất yên tĩnh, rất thích hợp để học. Tôi rất thích thư viện."
}

# Load current data
with open('www/data/simplified/reading_hsk1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Add pinyin to new passage
new_passage_with_pinyin = {
    "topic": new_passage["topic"],
    "description": new_passage["description"],
    "lines": [{
        "speaker": "",
        "text": new_passage["text"],
        "pinyin": text_to_pinyin(new_passage["text"]),
        "translation": new_passage["translation"]
    }]
}

# Append new passage
data["dialogs"].append(new_passage_with_pinyin)

# Save
with open('www/data/simplified/reading_hsk1.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✓ Đã thêm đoạn văn '{new_passage['topic']}'")
print(f"✓ Tổng số đoạn văn: {len(data['dialogs'])}")

# Check coverage now
def check_word_usage(passages, all_words):
    used_words = set()
    for passage in passages:
        text = passage['lines'][0]['text']
        for word in all_words:
            if word in text:
                used_words.add(word)
    return used_words

# Load vocab
with open('www/data/simplified/hsk1.json', 'r', encoding='utf-8') as f:
    vocab_data = json.load(f)

all_words = set([entry['hanzi'] for entry in vocab_data['entries']])
used_words = check_word_usage(data['dialogs'], all_words)
missing = all_words - used_words
coverage = len(used_words) / len(all_words) * 100

print(f"\nĐộ phủ từ vựng: {coverage:.2f}%")
print(f"Số từ đã sử dụng: {len(used_words)}/{len(all_words)}")

if missing:
    print(f"Còn thiếu {len(missing)} từ: {', '.join(sorted(missing))}")
else:
    print("✓ Đã sử dụng đầy đủ tất cả từ vựng HSK1!")
