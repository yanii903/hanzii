import json
from pypinyin import pinyin, Style

def load_vocab(level):
    """Load vocabulary from HSK level file"""
    with open(f'www/data/simplified/{level}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['entries']

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

# Đoạn văn HSK2 - sử dụng từ vựng HSK1 + HSK2
READING_PASSAGES_HSK2 = [
    {
        "topic": "新同学",
        "description": "Bạn học mới",
        "text": "今天我们班来了一位新同学。他叫张华，今年十八岁。他以前在另外一个学校学习，现在搬到我们这个城市了。张华很高，也很帅。他穿着一件白色的衬衫和黑色的裤子。老师让他站在教室前面介绍自己。他用中文说话说得很流利。他告诉我们，他喜欢运动，尤其喜欢打篮球和踢足球。他还说他会弹吉他，唱歌也唱得很好。下课以后，我走过去跟他聊天。我问他觉得我们学校怎么样。他笑着说，这里的环境很好，同学们都很友好。我们很快就成为了好朋友。中午休息的时候，我带他去食堂吃午饭。我们一边吃一边聊天，聊了很多有趣的事情。张华真是一个有意思的人！",
        "translation": "Hôm nay lớp chúng tôi có một bạn học mới. Bạn ấy tên là Trương Hoa, năm nay 18 tuổi. Trước đây bạn ấy học ở một trường khác, bây giờ chuyển đến thành phố của chúng tôi. Trương Hoa rất cao, cũng rất đẹp trai. Bạn ấy mặc một chiếc áo sơ mi trắng và quần đen. Giáo viên để bạn ấy đứng ở phía trước lớp tự giới thiệu. Bạn ấy nói tiếng Trung rất lưu loát. Bạn ấy nói với chúng tôi rằng bạn ấy thích thể thao, đặc biệt thích chơi bóng rổ và đá bóng. Bạn ấy còn nói bạn ấy biết chơi guitar, hát cũng rất hay. Sau khi tan học, tôi đi lại trò chuyện với bạn ấy. Tôi hỏi bạn ấy thấy trường chúng tôi thế nào. Bạn ấy cười nói, môi trường ở đây rất tốt, các bạn đều rất thân thiện. Chúng tôi rất nhanh trở thành bạn tốt. Giờ nghỉ trưa, tôi dẫn bạn ấy đi nhà ăn ăn trưa. Chúng tôi vừa ăn vừa trò chuyện, nói về nhiều chuyện thú vị. Trương Hoa thật là một người thú vị!"
    },
    {
        "topic": "在超市",
        "description": "Ở siêu thị",
        "text": "昨天下午，我和妹妹一起去超市买东西。超市离我家不远，走路只要十分钟。我们进去以后，先拿了一个购物车。超市里的东西真多啊！有新鲜的水果和蔬菜，有各种各样的零食，还有生活用品。妹妹看见她最爱吃的巧克力，马上放进购物车里。我告诉她不要买太多甜食，对牙齿不好。我们买了一些苹果、香蕉、橙子，还有一些蔬菜。然后我们去了日用品区，买了洗发水、牙膏和毛巾。妹妹还想买一个新的杯子，因为她的旧杯子坏了。我们挑了一个粉红色的杯子，很漂亮。最后我们去收银台付钱。服务员问我们要不要袋子，我说不用，我们自己带了环保袋。一共花了一百二十块钱。回家的路上，我们提着东西，觉得有点儿累，但是很开心。",
        "translation": "Chiều hôm qua, tôi và em gái cùng đi siêu thị mua đồ. Siêu thị cách nhà tôi không xa, đi bộ chỉ mất 10 phút. Sau khi chúng tôi vào, đầu tiên lấy một xe đẩy hàng. Đồ trong siêu thị thật nhiều! Có hoa quả và rau tươi, có đủ loại đồ ăn vặt, còn có đồ dùng sinh hoạt. Em gái thấy socola mà em ấy thích nhất, lập tức bỏ vào xe đẩy. Tôi nói với em ấy đừng mua quá nhiều đồ ngọt, không tốt cho răng. Chúng tôi mua một ít táo, chuối, cam, còn có một ít rau. Sau đó chúng tôi đến khu đồ dùng hàng ngày, mua dầu gội, kem đánh răng và khăn. Em gái còn muốn mua một cái cốc mới, vì cái cốc cũ của em ấy hỏng rồi. Chúng tôi chọn một cái cốc màu hồng, rất đẹp. Cuối cùng chúng tôi đến quầy thu ngân trả tiền. Nhân viên hỏi chúng tôi có cần túi không, tôi nói không cần, chúng tôi tự mang túi môi trường. Tổng cộng tốn 120 tệ. Trên đường về nhà, chúng tôi xách đồ, thấy hơi mệt, nhưng rất vui."
    },
    {
        "topic": "去医院看病",
        "description": "Đi bệnh viện khám bệnh",
        "text": "上个星期，我感冒了。开始的时候只是有点儿不舒服，后来越来越严重。我发烧了，头也很疼，嗓子也疼。妈妈说我应该去医院看医生。我们早上八点就到了医院。医院里人很多，我们等了一个小时才轮到我。医生问我哪儿不舒服，我告诉他我的情况。医生给我检查了一下，说我感冒了，需要休息。他给我开了一些药，让我按时吃药，多喝水，好好休息。医生还说，如果三天以后还不好，要再来医院。我们在医院的药房拿了药，然后就回家了。回到家，我马上吃了药，然后躺在床上休息。妈妈给我做了一些清淡的饭菜。我吃完饭就睡觉了。第二天，我觉得好多了。第三天，我的病基本上好了。我很高兴，可以继续上学了。",
        "translation": "Tuần trước, tôi bị cảm. Ban đầu chỉ hơi khó chịu, sau đó càng ngày càng nghiêm trọng. Tôi sốt, đầu cũng rất đau, cổ họng cũng đau. Mẹ nói tôi nên đi bệnh viện khám bác sĩ. Chúng tôi 8 giờ sáng đã đến bệnh viện. Trong bệnh viện người rất đông, chúng tôi đợi một tiếng mới đến lượt tôi. Bác sĩ hỏi tôi đâu khó chịu, tôi nói cho bác sĩ tình hình của tôi. Bác sĩ khám cho tôi một chút, nói tôi bị cảm, cần nghỉ ngơi. Bác sĩ kê cho tôi một ít thuốc, bảo tôi uống thuốc đúng giờ, uống nhiều nước, nghỉ ngơi tốt. Bác sĩ còn nói, nếu ba ngày sau vẫn không khỏi, phải đến bệnh viện lại. Chúng tôi lấy thuốc ở phòng thuốc của bệnh viện, sau đó về nhà. Về đến nhà, tôi lập tức uống thuốc, sau đó nằm trên giường nghỉ. Mẹ nấu cho tôi một ít cơm nhạt. Tôi ăn xong cơm liền ngủ. Ngày thứ hai, tôi thấy khỏe hơn nhiều. Ngày thứ ba, bệnh của tôi cơ bản đã khỏi. Tôi rất vui, có thể tiếp tục đi học."
    },
    {
        "topic": "周末去爬山",
        "description": "Cuối tuần đi leo núi",
        "text": "这个周末天气特别好，阳光明媚，我决定和几个朋友一起去爬山。我们早上六点就起床了，准备好水和食物，然后坐公共汽车去山脚下。山不是很高，但是风景很美。我们开始往上爬。刚开始的时候觉得很容易，但是爬到一半的时候，我们都累了。大家都出汗了，需要休息一下。我们坐在大树下面，喝水、吃东西、聊天。休息了十五分钟以后，我们继续往上爬。虽然累，但是我们都很开心。终于，我们爬到了山顶！站在山顶上，我们可以看到整个城市。风吹过来，非常凉快舒服。我们在山顶拍了很多照片。下午两点，我们开始下山。下山比上山容易多了。回到家已经是晚上五点了。虽然很累，但是今天过得真充实！",
        "translation": "Cuối tuần này thời tiết đặc biệt tốt, nắng đẹp, tôi quyết định cùng mấy người bạn đi leo núi. Chúng tôi 6 giờ sáng đã dậy, chuẩn bị nước và thức ăn, sau đó đi xe buýt đến chân núi. Núi không cao lắm, nhưng phong cảnh rất đẹp. Chúng tôi bắt đầu leo lên. Ban đầu thấy rất dễ, nhưng leo đến nửa chừng, chúng tôi đều mệt. Mọi người đều đổ mồ hôi, cần nghỉ một chút. Chúng tôi ngồi dưới cây lớn, uống nước, ăn đồ, trò chuyện. Nghỉ 15 phút sau, chúng tôi tiếp tục leo lên. Mặc dù mệt, nhưng chúng tôi đều rất vui. Cuối cùng, chúng tôi leo đến đỉnh núi! Đứng trên đỉnh núi, chúng tôi có thể nhìn thấy cả thành phố. Gió thổi qua, rất mát mẻ thoải mái. Chúng tôi chụp rất nhiều ảnh ở đỉnh núi. Chiều 2 giờ, chúng tôi bắt đầu xuống núi. Xuống núi dễ hơn leo núi nhiều. Về đến nhà đã 5 giờ tối. Mặc dù rất mệt, nhưng hôm nay thật là trọn vẹn!"
    },
    {
        "topic": "我的房间",
        "description": "Phòng của tôi",
        "text": "我的房间不大，但是很温馨。房间里有一张床、一张桌子、一把椅子和一个衣柜。床在房间的左边，旁边有一个小桌子，上面放着台灯和闹钟。每天早上，闹钟会叫我起床。我的书桌在窗户旁边，这样学习的时候光线比较好。桌子上面有我的电脑、一些书和笔记本。墙上贴着一张世界地图，还有几张我和朋友的照片。衣柜在门的后面，里面放着我的衣服和鞋子。我每个星期都会整理一次房间，把东西收拾干净。窗台上有几盆花，是我自己种的。每天我都会给它们浇水。房间的墙是浅蓝色的，地板是木头的，看起来很舒服。晚上，我会打开台灯，坐在书桌前看书或者做作业。累了就躺在床上听音乐。这就是我的小天地，我非常喜欢它！",
        "translation": "Phòng của tôi không lớn, nhưng rất ấm cúng. Trong phòng có một cái giường, một cái bàn, một cái ghế và một tủ quần áo. Giường ở bên trái phòng, bên cạnh có một cái bàn nhỏ, trên đó đặt đèn bàn và đồng hồ báo thức. Mỗi sáng, đồng hồ báo thức sẽ gọi tôi dậy. Bàn học của tôi ở cạnh cửa sổ, như vậy khi học ánh sáng khá tốt. Trên bàn có máy tính của tôi, một số sách và vở. Tường dán một tấm bản đồ thế giới, còn có mấy tấm ảnh tôi và bạn bè. Tủ quần áo ở phía sau cửa, bên trong đặt quần áo và giày của tôi. Mỗi tuần tôi đều dọn dẹp phòng một lần, thu xếp đồ đạc sạch sẽ. Trên bệ cửa sổ có mấy chậu hoa, là tôi tự trồng. Mỗi ngày tôi đều tưới nước cho chúng. Tường phòng màu xanh nhạt, sàn là gỗ, nhìn rất thoải mái. Buổi tối, tôi sẽ bật đèn bàn, ngồi trước bàn học đọc sách hoặc làm bài tập. Mệt thì nằm trên giường nghe nhạc. Đây là thiên đường nhỏ của tôi, tôi rất thích nó!"
    },
    {
        "topic": "坐地铁",
        "description": "Đi tàu điện ngầm",
        "text": "我每天上班都坐地铁。地铁站离我家很近，出门走五分钟就到了。早上七点半，地铁站里已经有很多人了。大家都在等地铁。我先去自动售票机买票。现在很多人都用手机支付，很方便。买好票以后，我通过闸机进入站台。站台上的屏幕显示下一趟地铁还有三分钟到达。我站在黄线后面等待。很快，地铁来了。车门打开，先让里面的乘客下车，然后我们才上去。车厢里人很多，我只能站着。我抓住扶手，以免摔倒。地铁开动了，速度很快。每到一站，广播会报站名。我要坐八站才到公司。车上有的人在看手机，有的人在睡觉，还有的人在看报纸。大约二十分钟后，我到了目的地。下车的时候要小心，注意脚下。走出地铁站，我就到公司了。坐地铁真的很快很方便！",
        "translation": "Tôi mỗi ngày đi làm đều đi tàu điện ngầm. Ga tàu điện ngầm cách nhà tôi rất gần, ra khỏi nhà đi 5 phút là đến. Sáng 7 giờ rưỡi, trong ga tàu điện ngầm đã có rất nhiều người. Mọi người đều đang đợi tàu điện ngầm. Tôi trước tiên đến máy bán vé tự động mua vé. Bây giờ nhiều người đều dùng điện thoại thanh toán, rất tiện. Mua xong vé, tôi đi qua cổng soát vé vào sân ga. Màn hình trên sân ga hiển thị chuyến tàu điện ngầm tiếp theo còn 3 phút nữa đến. Tôi đứng sau vạch vàng chờ. Rất nhanh, tàu điện ngầm đến. Cửa tàu mở, để hành khách bên trong xuống trước, sau đó chúng tôi mới lên. Trong toa tàu người rất đông, tôi chỉ có thể đứng. Tôi nắm tay vịn, để tránh té ngã. Tàu điện ngầm chạy, tốc độ rất nhanh. Mỗi đến một ga, loa phát thanh sẽ báo tên ga. Tôi phải đi 8 ga mới đến công ty. Trên xe có người xem điện thoại, có người ngủ, còn có người đọc báo. Khoảng 20 phút sau, tôi đến nơi. Khi xuống xe phải cẩn thận, chú ý chân. Đi ra khỏi ga tàu điện ngầm, tôi đến công ty. Đi tàu điện ngầm thật sự rất nhanh rất tiện!"
    },
    {
        "topic": "学做菜",
        "description": "Học nấu ăn",
        "text": "最近我想学做菜。以前我总是吃外卖或者去饭馆吃饭，既不健康也很贵。所以我决定自己学做饭。上个周末，我去超市买了很多食材：蔬菜、肉、鸡蛋、米、油、盐等等。回家以后，我在网上找了一个简单的菜谱。我决定先做西红柿炒鸡蛋。我把西红柿洗干净，切成小块。然后打了两个鸡蛋，放点儿盐。先把鸡蛋炒好，然后放西红柿。虽然第一次做，但是味道还不错！我很高兴。晚上，我又做了米饭和一个青菜汤。虽然做得不太好看，但是自己做的饭吃起来特别香。现在我每天都自己做饭。妈妈说我进步很快，做的菜越来越好吃了。我还学会了做很多菜：炒土豆丝、红烧肉、糖醋鱼等等。做菜不仅能省钱，还很有意思。我喜欢做菜！",
        "translation": "Gần đây tôi muốn học nấu ăn. Trước đây tôi luôn ăn đồ giao hay đi nhà hàng ăn, vừa không lành mạnh lại rất đắt. Vì vậy tôi quyết định tự học nấu cơm. Cuối tuần trước, tôi đi siêu thị mua rất nhiều nguyên liệu: rau, thịt, trứng, gạo, dầu, muối v.v. Về nhà sau, tôi tìm một công thức đơn giản trên mạng. Tôi quyết định làm cà chua xào trứng trước. Tôi rửa sạch cà chua, cắt thành miếng nhỏ. Sau đó đập hai quả trứng, cho một chút muối. Trước tiên xào trứng, sau đó cho cà chua vào. Mặc dù là lần đầu làm, nhưng hương vị cũng không tệ! Tôi rất vui. Buổi tối, tôi lại nấu cơm và một canh rau xanh. Mặc dù làm không đẹp lắm, nhưng cơm tự làm ăn đặc biệt thơm. Bây giờ tôi mỗi ngày đều tự nấu cơm. Mẹ nói tôi tiến bộ rất nhanh, món làm càng ngày càng ngon. Tôi còn học được nhiều món: xào khoai tây sợi, thịt kho đỏ, cá sốt chua ngọt v.v. Nấu ăn không chỉ tiết kiệm tiền, còn rất thú vị. Tôi thích nấu ăn!"
    },
    {
        "topic": "考试",
        "description": "Thi cử",
        "text": "下个星期我们要期中考试了。我有点儿紧张，因为这次考试很重要。这几天我一直在认真复习。我每天早上六点就起床，开始看书。白天在学校上课的时候，我也认真听讲，做好笔记。晚上回家以后，我会把今天学的内容再复习一遍。遇到不懂的问题，我会问老师或者同学。我的朋友小李也在努力准备考试。我们经常一起学习，互相帮助。有时候我们会去图书馆，那里很安静，适合学习。妈妈很关心我，每天都给我做营养的饭菜。她还告诉我不要太紧张，只要努力就好。考试的前一天晚上，我把所有的复习资料都看了一遍，然后早点儿睡觉，保证第二天精神好。考试的时候，我要仔细审题，认真答题。我相信只要好好准备，一定能考出好成绩！",
        "translation": "Tuần sau chúng tôi sẽ thi giữa kỳ. Tôi hơi lo, vì kỳ thi này rất quan trọng. Mấy ngày này tôi luôn ôn tập chăm chỉ. Tôi mỗi sáng 6 giờ đã dậy, bắt đầu xem sách. Ban ngày ở trường khi học, tôi cũng chăm chú nghe giảng, ghi chú tốt. Buổi tối về nhà sau, tôi sẽ ôn lại một lần nội dung hôm nay học. Gặp vấn đề không hiểu, tôi sẽ hỏi thầy cô hoặc bạn học. Bạn tôi Tiểu Lý cũng đang cố gắng chuẩn bị thi. Chúng tôi thường cùng học, giúp đỡ lẫn nhau. Có lúc chúng tôi sẽ đi thư viện, đó rất yên tĩnh, thích hợp để học. Mẹ rất quan tâm tôi, mỗi ngày đều nấu cơm dinh dưỡng cho tôi. Mẹ còn nói với tôi đừng quá lo lắng, chỉ cần cố gắng là được. Buổi tối trước ngày thi, tôi xem hết tất cả tài liệu ôn tập một lần, sau đó ngủ sớm, đảm bảo ngày hôm sau tinh thần tốt. Khi thi, tôi phải xem đề cẩn thận, trả lời nghiêm túc. Tôi tin chỉ cần chuẩn bị tốt, nhất định có thể thi được điểm tốt!"
    },
    {
        "topic": "生日聚会",
        "description": "Tiệc sinh nhật",
        "text": "昨天是我的生日，我邀请了一些好朋友来家里开生日聚会。下午三点，朋友们陆续到了。他们都带来了礼物，有书、有巧克力、还有一个漂亮的相框。我很感动，谢谢大家。我们先在客厅聊天。大家聊得很开心，说了很多有趣的事情。然后我们一起玩游戏、唱歌、跳舞。房间里充满了欢笑声。到了晚上六点，妈妈端出了一个大蛋糕。蛋糕上插着十九根蜡烛，因为我今年十九岁了。朋友们围着我，一起唱生日快乐歌。我闭上眼睛，许了一个愿望，然后吹灭了蜡烛。大家一起鼓掌。我们切蛋糕，每个人都分到了一块。蛋糕很甜，很好吃。晚饭时间，妈妈准备了很多好吃的菜。我们一边吃一边聊，度过了一个愉快的夜晚。朋友们离开的时候，都说今天玩得很高兴。这是我最难忘的生日！",
        "translation": "Hôm qua là sinh nhật của tôi, tôi mời một số bạn tốt đến nhà tổ chức tiệc sinh nhật. Chiều 3 giờ, các bạn lần lượt đến. Họ đều mang quà đến, có sách, có socola, còn có một khung ảnh đẹp. Tôi rất cảm động, cảm ơn mọi người. Chúng tôi trước tiên trò chuyện ở phòng khách. Mọi người trò chuyện rất vui, nói nhiều chuyện thú vị. Sau đó chúng tôi cùng chơi game, hát, nhảy. Phòng tràn ngập tiếng cười. Đến 6 giờ tối, mẹ mang ra một cái bánh lớn. Trên bánh cắm 19 cây nến, vì năm nay tôi 19 tuổi. Bạn bè vây quanh tôi, cùng hát bài chúc mừng sinh nhật. Tôi nhắm mắt, ước một điều ước, sau đó thổi tắt nến. Mọi người cùng vỗ tay. Chúng tôi cắt bánh, mỗi người đều nhận được một miếng. Bánh rất ngọt, rất ngon. Giờ ăn tối, mẹ chuẩn bị rất nhiều món ngon. Chúng tôi vừa ăn vừa trò chuyện, trải qua một buổi tối vui vẻ. Khi bạn bè rời đi, đều nói hôm nay chơi rất vui. Đây là sinh nhật khó quên nhất của tôi!"
    },
    {
        "topic": "运动会",
        "description": "Hội thao",
        "text": "上个月，我们学校举办了一年一度的运动会。全校的学生都参加了。运动会有很多项目：跑步、跳远、跳高、接力赛等等。我报名参加了一百米跑步和接力赛。比赛前几天，我每天都去操场练习跑步。老师说要想跑得快，需要多练习。运动会那天，天气很好。操场上人山人海，非常热闹。我先参加了一百米跑步。站在起跑线上，我的心跳得很快。裁判员吹响口哨，我就像箭一样冲了出去。虽然我很努力，但是只得了第三名。下午是接力赛。我和三个同学一组。我们互相鼓励，一定要加油！比赛开始了，我们跑得很快，最后得了第一名！大家都很高兴，拥抱在一起。这次运动会让我明白了团队合作的重要性。虽然很累，但是我觉得很值得！",
        "translation": "Tháng trước, trường chúng tôi tổ chức hội thao hàng năm. Toàn bộ học sinh trường đều tham gia. Hội thao có nhiều môn: chạy, nhảy xa, nhảy cao, chạy tiếp sức v.v. Tôi đăng ký tham gia chạy 100 mét và chạy tiếp sức. Trước ngày thi đấu vài ngày, tôi mỗi ngày đều đến sân tập chạy. Thầy nói muốn chạy nhanh, cần luyện tập nhiều. Ngày hội thao, thời tiết rất tốt. Sân vận động người núi người biển, rất náo nhiệt. Tôi trước tiên tham gia chạy 100 mét. Đứng ở vạch xuất phát, tim tôi đập rất nhanh. Trọng tài thổi còi, tôi như mũi tên lao ra. Mặc dù tôi rất cố gắng, nhưng chỉ được giải ba. Chiều là chạy tiếp sức. Tôi và ba bạn học một nhóm. Chúng tôi động viên lẫn nhau, nhất định phải cố lên! Cuộc thi bắt đầu, chúng tôi chạy rất nhanh, cuối cùng được giải nhất! Mọi người đều rất vui, ôm nhau. Hội thao lần này khiến tôi hiểu được tầm quan trọng của hợp tác đội nhóm. Mặc dù rất mệt, nhưng tôi thấy rất đáng!"
    },
    {
        "topic": "第一次打工",
        "description": "Lần đầu làm thêm",
        "text": "暑假的时候，我找了一份兼职工作。这是我第一次打工，所以很兴奋也有点儿紧张。我在一家咖啡店工作。每天早上九点上班，下午五点下班。第一天上班，店长给我介绍了工作内容。我需要学习怎么做咖啡、怎么接待客人、怎么收钱等等。开始的时候，我觉得很难。做咖啡的步骤很多，我总是记不住。有时候客人很多，我会手忙脚乱。但是店长和同事们都很好，他们耐心地教我。慢慢地，我越来越熟练了。我学会了做各种咖啡，也学会了怎么跟客人交流。有些老客人还记得我，会跟我聊天。工作虽然辛苦，但是我学到了很多东西。我明白了赚钱不容易，也更加理解父母了。暑假结束的时候，我拿到了第一份工资。我用这些钱给爸爸妈妈买了礼物。他们很高兴，说我长大了。",
        "translation": "Mùa hè, tôi tìm được một công việc bán thời gian. Đây là lần đầu tiên tôi làm thêm, nên rất phấn khích cũng hơi lo. Tôi làm việc ở một quán cà phê. Mỗi ngày 9 giờ sáng đi làm, 5 giờ chiều tan làm. Ngày đầu đi làm, quản lý giới thiệu cho tôi nội dung công việc. Tôi cần học cách pha cà phê, cách tiếp khách, cách thu tiền v.v. Ban đầu, tôi thấy rất khó. Các bước pha cà phê rất nhiều, tôi luôn nhớ không được. Có lúc khách rất đông, tôi sẽ tay chân lúng túng. Nhưng quản lý và đồng nghiệp đều rất tốt, họ kiên nhẫn dạy tôi. Dần dần, tôi càng ngày càng thành thạo. Tôi học được cách pha nhiều loại cà phê, cũng học được cách giao tiếp với khách. Một số khách quen còn nhớ tôi, sẽ trò chuyện với tôi. Công việc tuy vất vả, nhưng tôi học được nhiều thứ. Tôi hiểu kiếm tiền không dễ, cũng hiểu bố mẹ hơn. Kết thúc mùa hè, tôi nhận được tiền lương đầu tiên. Tôi dùng số tiền này mua quà cho bố mẹ. Họ rất vui, nói tôi đã lớn."
    },
    {
        "topic": "搬家",
        "description": "Chuyển nhà",
        "text": "上个月，我们家搬家了。以前的房子比较旧，而且离爸爸的公司太远。新家在市中心，交通很方便。搬家前一个星期，我们就开始收拾东西。妈妈把所有的衣服、书、碗筷等都装进箱子里。我帮忙整理自己房间的东西。我发现了很多以前的照片和玩具，看着它们，想起了很多美好的回忆。搬家那天，搬家公司来了。工人们很专业，小心地把家具搬上车。我们坐车跟在后面。到了新家，我很兴奋。新房子比旧房子大多了，而且很明亮。我有了自己独立的房间！墙是我最喜欢的绿色。我开始布置房间，把书放在书架上，把海报贴在墙上。妈妈在厨房忙着整理锅碗瓢盆。虽然累，但是大家都很开心。邻居们也很友好，来帮我们搬东西。新环境让我很期待，我想我会喜欢这里的！",
        "translation": "Tháng trước, gia đình chúng tôi chuyển nhà. Nhà trước khá cũ, và cách công ty của bố quá xa. Nhà mới ở trung tâm thành phố, giao thông rất tiện. Trước khi chuyển nhà một tuần, chúng tôi đã bắt đầu thu dọn đồ. Mẹ bỏ tất cả quần áo, sách, bát đũa v.v. vào hộp. Tôi giúp thu dọn đồ trong phòng mình. Tôi phát hiện nhiều ảnh và đồ chơi trước đây, nhìn chúng, nhớ lại nhiều kỷ niệm đẹp. Ngày chuyển nhà, công ty chuyển nhà đến. Công nhân rất chuyên nghiệp, cẩn thận chuyển đồ nội thất lên xe. Chúng tôi đi xe theo phía sau. Đến nhà mới, tôi rất phấn khích. Nhà mới lớn hơn nhà cũ nhiều, và rất sáng sủa. Tôi có phòng riêng độc lập! Tường là màu xanh lá tôi thích nhất. Tôi bắt đầu bố trí phòng, đặt sách lên giá, dán poster lên tường. Mẹ ở nhà bếp bận thu xếp nồi chảo bát đĩa. Mặc dù mệt, nhưng mọi người đều rất vui. Hàng xóm cũng rất thân thiện, đến giúp chúng tôi chuyển đồ. Môi trường mới khiến tôi rất mong đợi, tôi nghĩ tôi sẽ thích nơi đây!"
    },
    {
        "topic": "学骑自行车",
        "description": "Học đi xe đạp",
        "text": "小时候，我一直想学骑自行车，但是害怕摔倒。去年暑假，爸爸鼓励我，说一定要学会。他给我买了一辆漂亮的自行车。第一天练习，我很紧张。爸爸在旁边扶着车，我骑得摇摇晃晃的。刚开始的时候，我根本控制不了方向，总是往左右倾斜。爸爸告诉我要保持平衡，眼睛看前方，不要看脚下。我按照他说的做，慢慢地感觉好一点了。但是当爸爸松手的时候，我就摔倒了。膝盖擦破了，很疼。我想放弃，但是爸爸说：失败是成功之母，要坚持！我又爬起来继续练习。经过一个星期的努力，我终于学会了！我可以自己骑着自行车在小区里转来转去。现在我每天都骑自行车上学，既锻炼身体，又环保。学骑自行车让我明白：只要不怕困难，坚持不懈，就一定能成功！",
        "translation": "Hồi nhỏ, tôi luôn muốn học đi xe đạp, nhưng sợ ngã. Mùa hè năm ngoái, bố động viên tôi, nói nhất định phải học được. Bố mua cho tôi một chiếc xe đạp đẹp. Ngày đầu luyện tập, tôi rất lo. Bố ở bên cạnh nâng xe, tôi đạp lảo đảo. Lúc mới bắt đầu, tôi hoàn toàn không kiểm soát được hướng, luôn nghiêng trái phải. Bố nói với tôi phải giữ thăng bằng, mắt nhìn phía trước, không nhìn chân. Tôi làm theo như bố nói, dần dần cảm thấy tốt hơn một chút. Nhưng khi bố buông tay, tôi liền ngã. Đầu gối trầy, rất đau. Tôi muốn bỏ cuộc, nhưng bố nói: thất bại là mẹ thành công, phải kiên trì! Tôi lại đứng dậy tiếp tục luyện tập. Sau một tuần cố gắng, cuối cùng tôi học được! Tôi có thể tự mình đạp xe đạp đi lại trong khu. Bây giờ tôi mỗi ngày đều đạp xe đạp đi học, vừa rèn luyện thân thể, lại thân thiện môi trường. Học đi xe đạp khiến tôi hiểu: chỉ cần không sợ khó khăn, kiên trì không ngừng, nhất định sẽ thành công!"
    }
]

def generate_reading_data_hsk2():
    """Generate complete reading data for HSK2"""
    
    # Load vocabulary to check coverage
    vocab_entries = load_vocab('hsk2')
    all_words = set([entry['hanzi'] for entry in vocab_entries])
    
    print(f"Tổng số từ HSK2: {len(all_words)}")
    
    dialogs = []
    
    # Convert passages to full format
    for passage in READING_PASSAGES_HSK2:
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
        dialogs.append(dialog)
    
    # Check coverage
    used_words = set()
    for dialog in dialogs:
        text = dialog['lines'][0]['text']
        for word in all_words:
            if word in text:
                used_words.add(word)
    
    missing_words = all_words - used_words
    coverage = len(used_words) / len(all_words) * 100
    
    print(f"\nĐộ phủ từ vựng HSK2: {coverage:.2f}%")
    print(f"Số từ đã sử dụng: {len(used_words)}/{len(all_words)}")
    
    if missing_words:
        print(f"\nCòn thiếu {len(missing_words)} từ")
        if len(missing_words) <= 20:
            print("Từ còn thiếu:", ', '.join(sorted(missing_words)))
    
    # Calculate passage lengths
    lengths = [len(d['lines'][0]['text']) for d in dialogs]
    print(f"\nSố đoạn văn: {len(dialogs)}")
    print(f"Độ dài trung bình: {sum(lengths)//len(lengths)} ký tự")
    print(f"Độ dài: từ {min(lengths)} đến {max(lengths)} ký tự")
    
    # Save to file
    output = {"dialogs": dialogs}
    with open('www/data/simplified/reading_hsk2.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Đã lưu vào www/data/simplified/reading_hsk2.json")

if __name__ == '__main__':
    generate_reading_data_hsk2()
