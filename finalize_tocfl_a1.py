import json
from opencc import OpenCC
from pypinyin import pinyin, Style

cc = OpenCC('s2t')

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

# Đoạn văn bổ sung cuối cùng
FINAL_PASSAGES = [
    {
        "topic": "現代生活",
        "description": "Cuộc sống hiện đại",
        "text": "現在的生活和以前很不一樣了。每天早上，男人和女人都要去上班。有的人開車去，有的人坐公共汽車。很多人都有手機，在路上可以用手機看報紙、聽音樂或者和朋友聊天。我認識一位女人，她每天要去很遠的地方上班。她告訴我，雖然很累，但是她很喜歡她的工作。還有一位男人，他在家工作，不用去辦公室。他說這樣可以有更多時間陪孩子。現在的孩子們也很忙，他們要上學、做作業、參加各種活動。周末的時候，一家人會一起去公園或者商場。有時候我在想，為什麼現代人這麼忙呢？是因為生活節奏快，還是因為我們想要得到更多？這個問題很難回答。但是不管怎樣，我們都應該好好享受生活，多陪陪家人和朋友。",
        "translation": "Cuộc sống bây giờ rất khác so với trước. Mỗi sáng, đàn ông và phụ nữ đều phải đi làm. Có người lái xe đi, có người đi xe buýt. Rất nhiều người có điện thoại, trên đường có thể dùng điện thoại xem báo, nghe nhạc hoặc nói chuyện với bạn bè. Tôi quen một phụ nữ, cô mỗi ngày phải đi nơi rất xa đi làm. Cô nói cho tôi, mặc dù rất mệt, nhưng cô rất thích công việc của cô. Còn có một đàn ông, anh làm việc ở nhà, không cần đi văn phòng. Anh nói như vậy có thể có nhiều thời gian hơn ở cùng con cái. Trẻ em bây giờ cũng rất bận, chúng phải đi học, làm bài tập, tham gia các hoạt động. Cuối tuần, cả nhà sẽ cùng đi công viên hoặc trung tâm mua sắm. Đôi khi tôi nghĩ, tại sao người hiện đại bận thế? Là vì nhịp sống nhanh, hay vì chúng ta muốn có được nhiều hơn? Câu hỏi này rất khó trả lời. Nhưng dù sao, chúng ta đều nên tận hưởng cuộc sống, ở cùng gia đình và bạn bè nhiều hơn."
    },
    {
        "topic": "買衣服",
        "description": "Mua quần áo",
        "text": "星期六，我和媽媽去商場買衣服。商場裏有很多店，賣各種衣服、鞋子、手錶等等。我們先去看衣服。售貨員問我們要買什麼，我說想買幾件新衣服。售貨員很熱情，她給我們介紹了很多好看的衣服。有紅色的、黑色的、白色的，各種顏色都有。我試了好幾件，但是都不太合適。有的太大，有的太小。媽媽問我：你喜歡哪一件？我說我最喜歡那件藍色的。售貨員說：這件衣服很受歡迎，很多人都買。但是對不起，你要的號碼賣完了。我覺得有點兒失望。媽媽說：沒關係，我們再去別的店看看。我們又去了幾家店，最後找到了合適的衣服。這件衣服不貴也不便宜，價格剛剛好。我很高興，覺得沒有選錯。買完衣服，我們去吃午飯，然後就回家了。",
        "translation": "Thứ bảy, tôi và mẹ đi trung tâm mua sắm mua quần áo. Trong trung tâm có nhiều cửa hàng, bán đủ loại quần áo, giày, đồng hồ v.v. Chúng tôi trước tiên đi xem quần áo. Nhân viên bán hàng hỏi chúng tôi muốn mua gì, tôi nói muốn mua mấy bộ quần áo mới. Nhân viên rất nhiệt tình, cô giới thiệu cho chúng tôi nhiều quần áo đẹp. Có màu đỏ, đen, trắng, đủ màu sắc đều có. Tôi thử mấy bộ, nhưng đều không vừa lắm. Có cái quá to, có cái quá nhỏ. Mẹ hỏi tôi: con thích cái nào? Tôi nói tôi thích nhất cái màu xanh đó. Nhân viên nói: bộ quần áo này rất được ưa chuộng, nhiều người đều mua. Nhưng xin lỗi, số con muốn đã bán hết. Tôi thấy hơi thất vọng. Mẹ nói: không sao, chúng ta đi cửa hàng khác xem. Chúng tôi lại đi mấy cửa hàng, cuối cùng tìm thấy quần áo vừa. Bộ quần áo này không đắt cũng không rẻ, giá vừa phải. Tôi rất vui, thấy không chọn sai. Mua xong quần áo, chúng tôi đi ăn trưa, sau đó về nhà."
    }
]

# Load existing data
with open('www/data/traditional/reading_tocfl_a1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Convert and add new passages
for passage in FINAL_PASSAGES:
    # Convert text to traditional
    traditional_text = cc.convert(passage['text'])
    traditional_topic = cc.convert(passage['topic'])
    
    dialog = {
        "topic": traditional_topic,
        "description": passage['description'],
        "lines": [{
            "speaker": "",
            "text": traditional_text,
            "pinyin": text_to_pinyin(traditional_text),
            "translation": passage['translation']
        }]
    }
    data['dialogs'].append(dialog)

# Save updated data
with open('www/data/traditional/reading_tocfl_a1.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✓ Đã thêm {len(FINAL_PASSAGES)} đoạn văn cuối cùng")
print(f"✓ Tổng số đoạn văn: {len(data['dialogs'])}")

# Check final coverage
vocab_entries = json.load(open('www/data/traditional/tocfl_a1.json', 'r', encoding='utf-8'))
all_words = set([entry['hanzi'] for entry in vocab_entries['entries']])

used_words = set()
for dialog in data['dialogs']:
    text = dialog['lines'][0]['text']
    for word in all_words:
        if word in text:
            used_words.add(word)

missing = all_words - used_words
coverage = len(used_words) / len(all_words) * 100

print(f"\nĐộ phủ từ vựng TOCFL A1: {coverage:.2f}%")
print(f"Số từ đã sử dụng: {len(used_words)}/{len(all_words)}")

if missing:
    print(f"\nCòn thiếu {len(missing)} từ:")
    print(', '.join(sorted(missing)))
else:
    print("\n🎉 ĐÃ HOÀN THÀNH! Sử dụng đầy đủ 100% từ vựng TOCFL A1!")

# Check average length
lengths = [len(d['lines'][0]['text']) for d in data['dialogs']]
print(f"\nĐộ dài trung bình: {sum(lengths)//len(lengths)} ký tự")
print(f"Độ dài: từ {min(lengths)} đến {max(lengths)} ký tự")
