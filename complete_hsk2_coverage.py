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

# Đoạn văn bổ sung để đủ 100% từ vựng HSK2
ADDITIONAL_PASSAGES = [
    {
        "topic": "家庭介绍",
        "description": "Giới thiệu gia đình",
        "text": "大家好！我姓李，叫李明。今天我给大家介绍一下我的家庭。我家有六口人。我的爷爷奶奶都已经退休了。我爸爸是医生，我妈妈是老师。我还有一个哥哥和一个弟弟。哥哥今年二十五岁，已经结婚了。他的妻子很漂亮，也很善良。弟弟今年十五岁，还在上中学。我们家还有一个姐姐，她嫁给了一个很好的丈夫。他们有两个可爱的孩子，一个男孩和一个女孩。男人和女人在我们家都很平等，大家互相尊重。每个周末，我们全家人都会聚在一起吃饭。奶奶会做很多好吃的菜，有羊肉、牛肉，还有各种蔬菜。我特别喜欢喝牛奶。吃完饭，我们一起聊天，非常开心。这就是我温暖的大家庭！",
        "translation": "Xin chào mọi người! Tôi họ Lý, tên là Lý Minh. Hôm nay tôi giới thiệu với mọi người về gia đình của tôi. Nhà tôi có sáu người. Ông bà của tôi đều đã nghỉ hưu. Bố tôi là bác sĩ, mẹ tôi là giáo viên. Tôi còn có một anh trai và một em trai. Anh trai năm nay 25 tuổi, đã kết hôn. Vợ của anh ấy rất đẹp, cũng rất hiền lành. Em trai năm nay 15 tuổi, vẫn đang học trung học. Nhà chúng tôi còn có một chị gái, chị ấy lấy một người chồng rất tốt. Họ có hai đứa con đáng yêu, một bé trai và một bé gái. Nam giới và nữ giới trong gia đình chúng tôi đều rất bình đẳng, mọi người tôn trọng lẫn nhau. Mỗi cuối tuần, cả gia đình chúng tôi đều tụ họp lại cùng ăn cơm. Bà sẽ làm nhiều món ngon, có thịt cừu, thịt bò, còn có đủ loại rau. Tôi đặc biệt thích uống sữa. Ăn xong cơm, chúng tôi cùng trò chuyện, rất vui. Đây là đại gia đình ấm áp của tôi!"
    },
    {
        "topic": "在菜市场",
        "description": "Ở chợ",
        "text": "今天早上我陪妈妈去菜市场买菜。菜市场离家不远，从我家走过去只要五分钟。市场里有很多摊位，卖各种各样的东西。我们先去水果摊。老板很热情，欢迎我们来看看。妈妈问：西瓜多少钱一公斤？老板说：三元一公斤，很甜的。妈妈又问：能不能便宜一点儿？老板笑着说：好吧，给您便宜五毛钱。我们买了一个大西瓜。然后我们去买肉。妈妈买了一些羊肉和牛肉。她说今天要做羊肉汤和牛肉面。我们还买了一些蔬菜和牛奶。付钱的时候，老板娘问：一共多少元？妈妈数了数，说：一共八十五元。您贵姓？老板娘说：我姓王。以后常来啊！妈妈说谢谢，然后我们就回家了。路上妈妈告诉我，买东西要货比三家，这样才能买到又好又便宜的东西。",
        "translation": "Sáng nay tôi đi cùng mẹ đến chợ mua rau. Chợ cách nhà không xa, từ nhà tôi đi qua chỉ mất 5 phút. Trong chợ có nhiều quầy hàng, bán đủ loại thứ. Chúng tôi trước tiên đến quầy trái cây. Chủ rất nhiệt tình, chào đón chúng tôi đến xem. Mẹ hỏi: dưa hấu bao nhiêu tiền một kg? Chủ nói: 3 tệ một kg, rất ngọt. Mẹ lại hỏi: có thể rẻ hơn một chút không? Chủ cười nói: được thôi, giảm cho chị 5 mao. Chúng tôi mua một quả dưa hấu lớn. Sau đó chúng tôi đi mua thịt. Mẹ mua một ít thịt cừu và thịt bò. Mẹ nói hôm nay sẽ nấu canh thịt cừu và mì thịt bò. Chúng tôi còn mua một ít rau và sữa. Khi trả tiền, bà chủ hỏi: tổng cộng bao nhiêu tệ? Mẹ đếm, nói: tổng cộng 85 tệ. Chị quý họ gì? Bà chủ nói: tôi họ Vương. Sau này thường đến nhé! Mẹ nói cảm ơn, sau đó chúng tôi về nhà. Trên đường mẹ nói với tôi, mua đồ phải so sánh nhiều chỗ, như vậy mới mua được đồ vừa tốt vừa rẻ."
    },
    {
        "topic": "问路",
        "description": "Hỏi đường",
        "text": "昨天我要去机场接朋友，但是我不知道怎么走。我看见一位先生，就走过去问他。我说：您好，请问机场怎么走？他很友好地回答：从这里往右边走，然后坐地铁二号线就可以到。我问：大概要多长时间？他说：可能要四十分钟左右吧。您是第一次去机场吗？我说是的。他说：那我送您去地铁站吧，正在顺路。我说太感谢了！路上我们聊了很多。我问他为什么对这里这么熟悉。他说他在附近工作已经十年了。我们还聊到了天气。他说：今天是晴天，但是明天可能会下雨或者下雪，天气预报说会变阴天。到了地铁站，他告诉我在哪里买票，然后说：希望您的朋友旅途愉快！我说谢谢，再见！真是一位热心的好人！",
        "translation": "Hôm qua tôi phải đi sân bay đón bạn, nhưng tôi không biết đi thế nào. Tôi thấy một ông, liền đi qua hỏi ông ấy. Tôi nói: Xin chào, cho hỏi đi sân bay thế nào? Ông ấy rất thân thiện trả lời: Từ đây đi bên phải, sau đó đi tàu điện ngầm tuyến 2 là có thể đến. Tôi hỏi: khoảng mất bao lâu? Ông ấy nói: có thể khoảng 40 phút. Đây là lần đầu anh đi sân bay à? Tôi nói đúng vậy. Ông ấy nói: vậy tôi đưa anh đến ga tàu điện ngầm, đang đúng đường. Tôi nói cảm ơn quá! Trên đường chúng tôi nói chuyện nhiều. Tôi hỏi ông tại sao lại quen đây thế. Ông nói ông làm việc gần đây đã mười năm rồi. Chúng tôi còn nói về thời tiết. Ông nói: hôm nay trời nắng, nhưng ngày mai có thể sẽ mưa hoặc tuyết, dự báo thời tiết nói sẽ chuyển âm u. Đến ga tàu điện ngầm, ông ấy nói cho tôi mua vé ở đâu, sau đó nói: hi vọng bạn của anh có chuyến đi vui vẻ! Tôi nói cảm ơn, tạm biệt! Thật là một người tốt bụng nhiệt tình!"
    },
    {
        "topic": "买礼物",
        "description": "Mua quà",
        "text": "下个星期三是我妈妈的生日，我想给她买一份礼物。我不知道买什么好，就打电话问姐姐。姐姐说妈妈最近总是说她的手表坏了，不如买一块新手表吧。我觉得这是个好主意。周末我去了商场。我看了很多手表，有各种颜色的。有红色的、蓝色的、黑色的、白色的。我想妈妈可能喜欢白色或者粉红色的。售货员问我：您要买什么样的手表？我说：我想买一块白色的，价格不要太贵。她给我推荐了几款。我选了一块很漂亮的，价格是八百元。虽然有点儿贵，但是质量很好。我希望妈妈会喜欢。生日那天，我把礼物送给妈妈。妈妈很高兴，说：谢谢你，孩子！这正是我想要的。为什么你这么了解妈妈呢？我笑着说：因为我爱您啊！看到妈妈开心的样子，我也很开心。",
        "translation": "Tuần sau thứ Tư là sinh nhật mẹ tôi, tôi muốn mua một món quà cho mẹ. Tôi không biết mua gì, liền gọi điện hỏi chị gái. Chị nói mẹ gần đây luôn nói đồng hồ của mẹ hỏng rồi, không bằng mua một chiếc đồng hồ mới. Tôi thấy đây là ý kiến hay. Cuối tuần tôi đi trung tâm thương mại. Tôi xem nhiều đồng hồ, có nhiều màu sắc. Có đỏ, xanh dương, đen, trắng. Tôi nghĩ mẹ có thể thích trắng hoặc hồng. Nhân viên bán hàng hỏi tôi: Anh muốn mua đồng hồ như thế nào? Tôi nói: Tôi muốn mua chiếc màu trắng, giá không quá đắt. Cô ấy giới thiệu cho tôi vài mẫu. Tôi chọn một chiếc rất đẹp, giá 800 tệ. Mặc dù hơi đắt, nhưng chất lượng rất tốt. Tôi hi vọng mẹ sẽ thích. Ngày sinh nhật, tôi tặng quà cho mẹ. Mẹ rất vui, nói: Cảm ơn con! Đây chính là điều mẹ muốn. Tại sao con hiểu mẹ thế? Tôi cười nói: Vì con yêu mẹ! Nhìn mẹ vui, tôi cũng rất vui."
    },
    {
        "topic": "周末活动",
        "description": "Hoạt động cuối tuần",
        "text": "这个周末的天气真好，是晴天。我和朋友们决定去公园玩。我们早上八点在公园门口集合。大家都很准时，一个都没有迟到。进了公园，我们先去划船。湖面上已经有很多船了。我们租了一条船，在湖上划了一个小时。从船上可以看到很美的风景。中午我们在公园的草地上野餐。大家都带了食物。我带了三明治和水果，还有几瓶牛奶。朋友小张带了西瓜，又大又甜。我们一边吃一边聊天，非常开心。下午我们去游泳池游泳。虽然水有点儿凉，但是游泳很舒服。我们在水里玩了很久。游完泳，我们都累了。我们坐在树荫下休息。这时候天气开始变阴了，可能要下雨了。我们赶紧收拾东西准备回家。虽然有点儿累，但是今天玩得真开心！我们约好下次还要一起出来玩。",
        "translation": "Cuối tuần này thời tiết thật tốt, trời nắng. Tôi và bạn bè quyết định đi công viên chơi. Chúng tôi 8 giờ sáng tập trung ở cổng công viên. Mọi người đều rất đúng giờ, không ai muộn. Vào công viên, chúng tôi trước tiên đi chèo thuyền. Trên mặt hồ đã có nhiều thuyền. Chúng tôi thuê một chiếc thuyền, chèo trên hồ một tiếng. Từ thuyền có thể nhìn thấy phong cảnh rất đẹp. Trưa chúng tôi dã ngoại trên bãi cỏ công viên. Mọi người đều mang đồ ăn. Tôi mang sandwich và trái cây, còn có vài chai sữa. Bạn Tiểu Trương mang dưa hấu, to và ngọt. Chúng tôi vừa ăn vừa trò chuyện, rất vui. Chiều chúng tôi đi hồ bơi bơi lội. Mặc dù nước hơi lạnh, nhưng bơi rất thoải mái. Chúng tôi chơi trong nước rất lâu. Bơi xong, chúng tôi đều mệt. Chúng tôi ngồi dưới bóng cây nghỉ. Lúc này thời tiết bắt đầu chuyển âm, có thể sắp mưa. Chúng tôi vội thu dọn đồ chuẩn bị về nhà. Mặc dù hơi mệt, nhưng hôm nay chơi thật vui! Chúng tôi hẹn lần sau còn cùng ra ngoài chơi."
    }
]

# Load existing data
with open('www/data/simplified/reading_hsk2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Add new passages
for passage in ADDITIONAL_PASSAGES:
    text = passage['text']
    pinyin_text = text_to_pinyin(text)
    translation = passage['translation']
    
    dialog = {
        "topic": passage['topic'],
        "description": passage['description'],
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

print(f"✓ Đã thêm {len(ADDITIONAL_PASSAGES)} đoạn văn mới")
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
    if len(missing) <= 20:
        print(', '.join(sorted(missing)))
else:
    print("\n✓ Đã sử dụng đầy đủ tất cả từ vựng HSK2!")
