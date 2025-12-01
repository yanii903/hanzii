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

# Đoạn văn bổ sung cho TOCFL A1 (Giản thể trước, sẽ convert sang Phồn thể)
ADDITIONAL_PASSAGES = [
    {
        "topic": "我的家人",
        "description": "Gia đình tôi",
        "text": "大家好！我来介绍一下我的家人。我家有七口人：爷爷、奶奶、爸爸、妈妈、哥哥、妹妹和我。我爸爸的妻子是我妈妈，她是一位老师。我妈妈的丈夫是我爸爸，他是医生。我还有一个姐姐，她已经结婚了，她的丈夫很好。我的弟弟今年十岁，他喜欢踢足球和打篮球，非常喜欢运动。妹妹很可爱，她喜欢唱歌和跳舞。周末的时候，我们一家人会一起准备晚饭。爸爸做鱼，妈妈炒菜，我帮助他们洗菜。我们做了很多菜：红色的西红柿炒鸡蛋、黑色的木耳、还有羊肉。大家都觉得非常好吃。吃完饭，我们一起看电视，聊聊最近的事情。这就是我的家人，我很爱他们！",
        "translation": "Xin chào mọi người! Tôi giới thiệu về gia đình tôi. Nhà tôi có bảy người: ông, bà, bố, mẹ, anh trai, em gái và tôi. Vợ của bố tôi là mẹ tôi, mẹ là giáo viên. Chồng của mẹ tôi là bố tôi, ông là bác sĩ. Tôi còn có một chị gái, chị đã kết hôn, chồng của chị rất tốt. Em trai tôi năm nay mười tuổi, em thích đá bóng và chơi bóng rổ, rất thích thể thao. Em gái rất đáng yêu, em thích hát và nhảy. Cuối tuần, cả nhà chúng tôi sẽ cùng chuẩn bị bữa tối. Bố nấu cá, mẹ xào rau, tôi giúp họ rửa rau. Chúng tôi làm nhiều món: cà chua đỏ xào trứng, mộc nhĩ đen, còn có thịt cừu. Mọi người đều thấy rất ngon. Ăn xong cơm, chúng tôi cùng xem tivi, nói chuyện về những chuyện gần đây. Đây là gia đình tôi, tôi rất yêu họ!"
    },
    {
        "topic": "上學的一天",
        "description": "Một ngày đi học",
        "text": "今天早上我六點起床，穿上新衣服去上學。我坐公共汽車去學校，路上用了半個小時。到了學校，我先去教室。第一節課是中文課，老師教我們寫漢字。老師問我們懂不懂，我們都說懂了。第二節課是數學課，老師告訴我們怎麼做題。我覺得數學有點兒難，但是很有意思。下課以後，我和同學一起打籃球。我們在操場上跑步，玩得很開心。中午我在學校吃午飯，吃了魚、雞蛋和蔬菜。下午有兩節課，一節是英語課，一節是音樂課。音樂課上我們唱歌，老師說我唱得很好。放學以後，我坐公共汽車回家。回到家，我先洗手，然後做作業。晚上我和家人一起吃晚飯，然後準備明天的考試。",
        "translation": "Sáng nay tôi dậy lúc 6 giờ, mặc quần áo mới đi học. Tôi đi xe buýt đến trường, trên đường mất nửa tiếng. Đến trường, tôi trước tiên đến lớp học. Tiết đầu tiên là tiết tiếng Trung, thầy dạy chúng tôi viết chữ Hán. Thầy hỏi chúng tôi có hiểu không, chúng tôi đều nói hiểu rồi. Tiết thứ hai là tiết toán, thầy nói cho chúng tôi cách làm bài. Tôi thấy toán hơi khó, nhưng rất thú vị. Sau khi tan học, tôi và bạn học cùng chơi bóng rổ. Chúng tôi chạy bộ ở sân trường, chơi rất vui. Trưa tôi ăn trưa ở trường, ăn cá, trứng và rau. Chiều có hai tiết, một tiết tiếng Anh, một tiết âm nhạc. Tiết âm nhạc chúng tôi hát, thầy nói tôi hát rất hay. Sau khi tan học, tôi đi xe buýt về nhà. Về đến nhà, tôi trước tiên rửa tay, sau đó làm bài tập. Tối tôi cùng gia đình ăn tối, sau đó chuẩn bị cho kỳ thi ngày mai."
    },
    {
        "topic": "去超市買東西",
        "description": "Đi siêu thị mua đồ",
        "text": "昨天下午，我和媽媽去超市買東西。超市離我家很近，從家裏走過去只要十分鐘。進去以後，我們先去蔬菜區。那裏賣很多新鮮的蔬菜。媽媽買了一些西瓜、雞蛋、牛奶和羊肉。西瓜三元一公斤，很便宜。我問媽媽為什麼要買這麼多，媽媽回答說因為明天是我的生日，要準備生日晚會。我們還買了魚，媽媽說魚對身體很好。在水果區，我看見紅色的蘋果，黑色的葡萄，還有很多顏色的水果。我選了我最喜歡的香蕉。付錢的時候，一共花了一百二十元。服務員問我們需不需要袋子，媽媽說不用，我們自己帶了。走出超市，我幫助媽媽提東西。路上我們看見賣西瓜的人，他正在大聲喊：新鮮西瓜，又甜又便宜！",
        "translation": "Chiều hôm qua, tôi và mẹ đi siêu thị mua đồ. Siêu thị cách nhà tôi rất gần, từ nhà đi qua chỉ mất mười phút. Vào bên trong, chúng tôi trước tiên đi khu rau. Ở đó bán rất nhiều rau tươi. Mẹ mua một ít dưa hấu, trứng, sữa và thịt cừu. Dưa hấu ba tệ một kg, rất rẻ. Tôi hỏi mẹ tại sao mua nhiều thế, mẹ trả lời vì ngày mai là sinh nhật của tôi, phải chuẩn bị tiệc sinh nhật. Chúng tôi còn mua cá, mẹ nói cá tốt cho cơ thể. Ở khu trái cây, tôi thấy táo đỏ, nho đen, còn có nhiều màu sắc trái cây. Tôi chọn chuối tôi thích nhất. Khi trả tiền, tổng cộng tốn một trăm hai mươi tệ. Nhân viên hỏi chúng tôi có cần túi không, mẹ nói không cần, chúng tôi tự mang. Đi ra khỏi siêu thị, tôi giúp mẹ xách đồ. Trên đường chúng tôi thấy người bán dưa hấu, anh ta đang hét to: dưa hấu tươi, vừa ngọt vừa rẻ!"
    },
    {
        "topic": "問路",
        "description": "Hỏi đường",
        "text": "上個星期，我要去機場接朋友，但是不知道怎麼走。我看見一位先生，就過去問他。我說：您好，請問機場怎麼走？他很友好地告訴我：你從這裏往右邊走，然後在第一個路口向左轉，走大約一百米就能看見公共汽車站。坐五號線公共汽車就可以到機場。我問：大概要多長時間？他說：可能要一個小時左右吧。你也可以坐地鐵，比公共汽車快。我說太感謝您了！他笑著說：別客氣，希望你能順利接到朋友。我問他：機場旁邊有沒有商店？他說有，機場左邊有很多商店，賣各種東西，也有餐廳。我又問：買機票在哪裏？他說：在機場裏面，你一進去就能看見售票處。我們聊了一會兒，他還告訴我今天天氣很好，是晴天，但是明天可能會下雪，天氣會變陰。",
        "translation": "Tuần trước, tôi phải đi sân bay đón bạn, nhưng không biết đi thế nào. Tôi thấy một ông, liền đi qua hỏi ông. Tôi nói: Xin chào, cho hỏi đi sân bay thế nào? Ông rất thân thiện nói cho tôi: bạn từ đây đi bên phải, sau đó ở ngã tư đầu tiên rẽ trái, đi khoảng một trăm mét là thấy trạm xe buýt. Đi xe buýt tuyến 5 là có thể đến sân bay. Tôi hỏi: khoảng mất bao lâu? Ông nói: có thể khoảng một tiếng. Bạn cũng có thể đi tàu điện ngầm, nhanh hơn xe buýt. Tôi nói cảm ơn ông quá! Ông cười nói: đừng khách khí, hi vọng bạn có thể đón bạn thuận lợi. Tôi hỏi ông: bên cạnh sân bay có cửa hàng không? Ông nói có, bên trái sân bay có nhiều cửa hàng, bán đủ thứ, cũng có nhà hàng. Tôi lại hỏi: mua vé máy bay ở đâu? Ông nói: trong sân bay, bạn vừa vào là thấy quầy bán vé. Chúng tôi nói chuyện một lúc, ông còn nói cho tôi hôm nay thời tiết rất tốt, trời nắng, nhưng ngày mai có thể tuyết rơi, thời tiết sẽ chuyển âm."
    },
    {
        "topic": "週末活動",
        "description": "Hoạt động cuối tuần",
        "text": "這個週末，我和朋友們一起去公園玩。我們早上八點在公園門口休息區集合。我騎自行車去的，朋友小李坐公共汽車來的。公園裏人非常多，大家都在運動。有人在跑步，有人在打籃球，還有人在踢足球。我們先去游泳池游泳。水有點兒涼，但是游泳很舒服，對身體很好。游了一個小時以後，我們去旁邊的餐廳吃午飯。我點了魚和雞蛋，朋友們點了牛奶、羊肉和西瓜。飯菜的顏色很好看，紅色的西紅柿，黑色的木耳。下午我們去坐船。船票十元一次，不太貴。我們在湖上划船，看風景。湖邊有很多人在拍照，他們穿着各種顏色的新衣服。晚上我們一起去看電影。電影很有意思，我們都覺得很好看。看完電影已經很晚了，我們就各自回家了。",
        "translation": "Cuối tuần này, tôi và bạn bè cùng đi công viên chơi. Chúng tôi 8 giờ sáng tập trung ở khu nghỉ cổng công viên. Tôi đi xe đạp, bạn Tiểu Lý đi xe buýt đến. Trong công viên người rất đông, mọi người đều đang thể dục. Có người chạy bộ, có người chơi bóng rổ, còn có người đá bóng. Chúng tôi trước tiên đi hồ bơi bơi lội. Nước hơi lạnh, nhưng bơi rất thoải mái, tốt cho cơ thể. Bơi một tiếng sau, chúng tôi đi nhà hàng bên cạnh ăn trưa. Tôi gọi cá và trứng, bạn bè gọi sữa, thịt cừu và dưa hấu. Màu sắc món ăn rất đẹp, cà chua đỏ, mộc nhĩ đen. Chiều chúng tôi đi chèo thuyền. Vé thuyền mười tệ một lần, không đắt lắm. Chúng tôi chèo thuyền trên hồ, xem phong cảnh. Bên hồ có nhiều người đang chụp ảnh, họ mặc đủ loại quần áo màu sắc mới. Tối chúng tôi cùng đi xem phim. Phim rất thú vị, chúng tôi đều thấy rất hay. Xem xong phim đã rất muộn, chúng tôi mỗi người về nhà."
    },
    {
        "topic": "去醫院",
        "description": "Đi bệnh viện",
        "text": "去年冬天，我生病了。開始的時候我以為只是有點兒不舒服，所以沒有去醫院。但是過了兩天，我的眼睛很疼，身體也越來越不舒服。媽媽說我應該去看醫生。第二天早上，媽媽帶我去醫院。醫院離我家不遠，從家裏走路去只要十五分鐘，也可以騎自行車去。到了醫院，護士先問我哪裏不舒服，然後幫助我掛號。我們在休息室等了一個小時才輪到我。醫生很好，他告訴我不要緊張。他檢查了我的眼睛和身體，說我是因為太累了。他給我開了一些藥，讓我好好休息。他還說：這個藥一天吃三次，飯後吃。如果三天以後還不好，要再來醫院。媽媽問醫生：他需要住院嗎？醫生說不用，在家休息就可以了。我們付了錢，拿了藥就回家了。",
        "translation": "Mùa đông năm ngoái, tôi bị ốm. Ban đầu tôi tưởng chỉ hơi khó chịu, nên không đi bệnh viện. Nhưng qua hai ngày, mắt tôi rất đau, cơ thể cũng càng ngày càng khó chịu. Mẹ nói tôi nên đi khám bác sĩ. Sáng hôm sau, mẹ đưa tôi đi bệnh viện. Bệnh viện cách nhà tôi không xa, từ nhà đi bộ chỉ mất mười lăm phút, cũng có thể đi xe đạp. Đến bệnh viện, y tá trước tiên hỏi tôi đâu khó chịu, sau đó giúp tôi đăng ký. Chúng tôi đợi ở phòng nghỉ một tiếng mới đến lượt tôi. Bác sĩ rất tốt, ông nói cho tôi đừng lo lắng. Ông kiểm tra mắt và cơ thể của tôi, nói tôi là do quá mệt. Ông kê cho tôi một ít thuốc, bảo tôi nghỉ ngơi tốt. Ông còn nói: thuốc này một ngày uống ba lần, sau bữa ăn uống. Nếu ba ngày sau vẫn không khỏi, phải đến bệnh viện lại. Mẹ hỏi bác sĩ: con cần nằm viện không? Bác sĩ nói không cần, nghỉ ở nhà là được. Chúng tôi trả tiền, lấy thuốc rồi về nhà."
    },
    {
        "topic": "旅遊計劃",
        "description": "Kế hoạch du lịch",
        "text": "下個月是暑假，我和家人準備去旅遊。這是我們第一次一起旅遊，所以大家都很興奮。爸爸告訴我們，他已經買好了火車票和飛機票。我們要先坐火車去機場，然後坐飛機去目的地。媽媽問爸爸：飛機票多少錢一張？爸爸回答說：一千元左右，比較貴，但是很快。我們要去的地方很遠，坐飛機只要兩個小時，如果坐船要好幾天。媽媽正在準備行李，她買了新的衣服、帽子和手錶。弟弟問媽媽：我們什麼時候出發？媽媽說：下個月五號，你要準備好你的東西。我覺得這次旅遊一定會很有意思。我希望能看到很多新的地方，認識新的朋友。我也想買一些禮物送給我的朋友們。雖然要花不少錢，但是我們都覺得非常值得。旅遊可以讓我們休息，也可以學到很多新的事情。",
        "translation": "Tháng sau là kỳ nghỉ hè, tôi và gia đình chuẩn bị đi du lịch. Đây là lần đầu tiên chúng tôi cùng đi du lịch, nên mọi người đều rất phấn khích. Bố nói cho chúng tôi, ông đã mua vé tàu và vé máy bay. Chúng tôi trước tiên đi tàu hỏa đến sân bay, sau đó đi máy bay đến điểm đến. Mẹ hỏi bố: vé máy bay bao nhiêu tiền một vé? Bố trả lời: khoảng một nghìn tệ, khá đắt, nhưng rất nhanh. Nơi chúng tôi đi rất xa, đi máy bay chỉ mất hai tiếng, nếu đi thuyền phải mấy ngày. Mẹ đang chuẩn bị hành lý, mẹ mua quần áo mới, mũ và đồng hồ. Em trai hỏi mẹ: chúng ta khi nào khởi hành? Mẹ nói: tháng sau ngày 5, con phải chuẩn bị đồ của con. Tôi thấy chuyến du lịch này chắc chắn sẽ rất thú vị. Tôi hi vọng có thể xem nhiều nơi mới, quen bạn mới. Tôi cũng muốn mua một ít quà tặng cho bạn bè của tôi. Mặc dù phải tốn không ít tiền, nhưng chúng tôi đều thấy rất đáng. Du lịch có thể cho chúng tôi nghỉ ngơi, cũng có thể học được nhiều chuyện mới."
    },
    {
        "topic": "在餐廳",
        "description": "Ở nhà hàng",
        "text": "昨天晚上，我和朋友們去餐廳吃飯。這家餐廳很有名，賣各種各樣的菜。我們六點到的，餐廳已經有很多人了。服務員歡迎我們，讓我們坐在靠窗戶的位置。我覺得這個位置很好，因為可以看到外面的風景。服務員給我們菜單，問我們想喝什麼。我點了牛奶，朋友們點了果汁和茶。我們看菜單，上面有魚、雞蛋、羊肉、蔬菜等等。每個菜旁邊都寫着價錢，有的貴，有的便宜。服務員告訴我們，今天的特別菜是紅燒魚，非常好吃。我們決定點這個。我還點了西紅柿炒雞蛋，朋友點了羊肉。等菜的時候，我們聊天，談論最近的事情。服務員送來了菜，菜的顏色很漂亮，紅色、黑色、綠色都有。我們開始吃飯，大家都說菜很好吃。吃完飯，服務員問我們需不需要打包。我們說不用了，然後付了錢。",
        "translation": "Tối hôm qua, tôi và bạn bè đi nhà hàng ăn cơm. Nhà hàng này rất nổi tiếng, bán đủ loại món. Chúng tôi đến lúc 6 giờ, nhà hàng đã có rất nhiều người. Nhân viên chào đón chúng tôi, để chúng tôi ngồi ở vị trí gần cửa sổ. Tôi thấy vị trí này rất tốt, vì có thể nhìn phong cảnh bên ngoài. Nhân viên đưa thực đơn cho chúng tôi, hỏi chúng tôi muốn uống gì. Tôi gọi sữa, bạn bè gọi nước trái cây và trà. Chúng tôi xem thực đơn, trên đó có cá, trứng, thịt cừu, rau v.v. Bên cạnh mỗi món đều viết giá, có món đắt, có món rẻ. Nhân viên nói cho chúng tôi, món đặc biệt hôm nay là cá kho đỏ, rất ngon. Chúng tôi quyết định gọi món này. Tôi còn gọi cà chua xào trứng, bạn gọi thịt cừu. Khi đợi món, chúng tôi trò chuyện, bàn luận chuyện gần đây. Nhân viên mang món đến, màu sắc món ăn rất đẹp, đỏ, đen, xanh đều có. Chúng tôi bắt đầu ăn cơm, mọi người đều nói món rất ngon. Ăn xong cơm, nhân viên hỏi chúng tôi có cần đóng gói không. Chúng tôi nói không cần, sau đó trả tiền."
    }
]

# Load existing data
with open('www/data/traditional/reading_tocfl_a1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Convert and add new passages
for passage in ADDITIONAL_PASSAGES:
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

print(f"✓ Đã thêm {len(ADDITIONAL_PASSAGES)} đoạn văn mới")
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
    if len(missing) <= 30:
        print(', '.join(sorted(missing)))
else:
    print("\n✓ Đã sử dụng đầy đủ 100% từ vựng TOCFL A1!")

# Check average length
lengths = [len(d['lines'][0]['text']) for d in data['dialogs']]
print(f"\nĐộ dài trung bình: {sum(lengths)//len(lengths)} ký tự")
print(f"Độ dài: từ {min(lengths)} đến {max(lengths)} ký tự")
