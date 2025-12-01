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

# Đoạn văn cuối cùng chứa 3 từ còn thiếu: 千, 旅游, 生病
final_passage = {
    "topic": "假期旅游",
    "description": "Du lịch kỳ nghỉ",
    "text": "去年夏天，我和家人去云南旅游。这是我第一次去那么远的地方旅游。我们坐飞机去的，飞机票很贵，一个人要两千多元。虽然贵，但是很值得。云南的风景真美啊！我们去了很多地方：大理、丽江、香格里拉。每个地方都有不同的特色。在大理，我们看到了洱海，湖水很清澈。在丽江，我们参观了古城，那里的建筑很有特色。但是在旅游的第三天，我弟弟突然生病了。他发烧，而且肚子也疼。我们很担心，赶紧带他去医院。医生检查以后说，可能是吃坏了东西，需要休息几天。我们只好在酒店休息了两天。好在弟弟很快就好了，我们又可以继续旅游了。虽然中间出了点儿小问题，但是这次旅游还是很愉快的。我拍了上千张照片，记录了这次美好的旅行。回家以后，我常常看这些照片，回忆那段快乐的时光。",
    "translation": "Mùa hè năm ngoái, tôi và gia đình đi du lịch Vân Nam. Đây là lần đầu tiên tôi đi du lịch nơi xa như vậy. Chúng tôi đi máy bay, vé máy bay rất đắt, một người hơn 2000 tệ. Mặc dù đắt, nhưng rất đáng. Phong cảnh Vân Nam thật đẹp! Chúng tôi đi nhiều nơi: Đại Lý, Lệ Giang, Shangri-La. Mỗi nơi đều có đặc sắc khác nhau. Ở Đại Lý, chúng tôi thấy hồ Nhĩ Hải, nước hồ rất trong. Ở Lệ Giang, chúng tôi tham quan cổ trấn, kiến trúc ở đó rất có đặc sắc. Nhưng ngày thứ ba du lịch, em trai tôi đột nhiên bị ốm. Em ấy sốt, và bụng cũng đau. Chúng tôi rất lo, vội đưa em ấy đi bệnh viện. Bác sĩ khám xong nói, có thể ăn hỏng bụng, cần nghỉ mấy ngày. Chúng tôi chỉ còn cách nghỉ ở khách sạn hai ngày. May mà em trai nhanh chóng khỏe lại, chúng tôi lại có thể tiếp tục du lịch. Mặc dù giữa chừng có chút vấn đề nhỏ, nhưng chuyến du lịch này vẫn rất vui vẻ. Tôi chụp trên nghìn tấm ảnh, ghi lại chuyến du lịch đẹp này. Về nhà sau, tôi thường xem những tấm ảnh này, nhớ lại khoảng thời gian vui vẻ đó."
}

# Load existing data
with open('www/data/simplified/reading_hsk2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Add final passage
text = final_passage['text']
pinyin_text = text_to_pinyin(text)
translation = final_passage['translation']

dialog = {
    "topic": final_passage['topic'],
    "description": final_passage['description'],
    "lines": [{
        "speaker": "",
        "text": text,
        "pinyin": pinyin_text,
        "translation": translation
    }]
}
data['dialogs'].append(dialog)

# Save updated data
with open('www/data/simplified/reading_hsk2.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✓ Đã thêm đoạn văn cuối cùng")
print(f"✓ Tổng số đoạn văn: {len(data['dialogs'])}")

# Check final coverage
vocab_entries = json.load(open('www/data/simplified/hsk2.json', 'r', encoding='utf-8'))
all_words = set([entry['hanzi'] for entry in vocab_entries['entries']])

used_words = set()
for dialog in data['dialogs']:
    text = dialog['lines'][0]['text']
    for word in all_words:
        if word in text:
            used_words.add(word)

missing = all_words - used_words
coverage = len(used_words) / len(all_words) * 100

print(f"\nĐộ phủ từ vựng HSK2: {coverage:.2f}%")
print(f"Số từ đã sử dụng: {len(used_words)}/{len(all_words)}")

if missing:
    print(f"\nCòn thiếu {len(missing)} từ:")
    print(', '.join(sorted(missing)))
else:
    print("\n✓ Đã sử dụng đầy đủ 100% từ vựng HSK2!")

# Check average length
lengths = [len(d['lines'][0]['text']) for d in data['dialogs']]
print(f"\nĐộ dài trung bình: {sum(lengths)//len(lengths)} ký tự")
print(f"Độ dài: từ {min(lengths)} đến {max(lengths)} ký tự")
