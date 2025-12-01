import json
from pypinyin import pinyin, Style

# Định nghĩa bản dịch tiếng Việt cho từng đoạn văn
TRANSLATIONS = {
    "我的一天": "Tôi tên là Tiểu Minh, tôi là học sinh. Nhà tôi có bốn người, bố, mẹ, tôi và con gái tôi. Tôi rất yêu gia đình của mình. Hôm nay là thứ Hai, tôi dậy lúc 7 giờ. Mẹ tôi nấu bữa sáng, tôi ăn cơm và táo. Tôi uống trà, không uống cà phê. 8 giờ tôi đi học. Trường của tôi rất lớn, cũng rất đẹp. Tôi học tiếng Trung ở trường. Giáo viên của tôi là người Trung Quốc, cô ấy rất tốt. Cô ấy tên là cô Lý. 12 giờ tôi và bạn học ăn cơm ở trường. Chúng tôi ăn cơm và rau. Buổi chiều tôi đọc sách, cũng viết chữ Hán. Tôi có rất nhiều sách tiếng Trung. 4 giờ tan học. 5 giờ tôi về nhà. Về nhà sau, tôi làm bài tập trước, sau đó ăn tối. Buổi tối tôi cùng bố mẹ xem tivi. Chúng tôi xem phim Trung Quốc. 10 giờ tôi đi ngủ. Tôi rất vui. Tôi thích trường của mình, cũng thích gia đình của mình.",
    
    "去商店买东西": "Hôm nay là thứ Bảy, tôi không đi học. Buổi sáng 9 giờ, tôi cùng mẹ đi cửa hàng mua đồ. Cửa hàng rất lớn, bên trong có rất nhiều thứ. Tôi thấy nước, trà, cơm, táo, cốc, ghế, bàn, còn có rất nhiều sách. Người trong cửa hàng cũng rất đông. Nước 5 tệ một chai, trà 6 tệ, cơm 8 tệ. Tôi rất thích táo, tôi hỏi chủ: quả táo này bao nhiêu tiền? Chủ nói: 3 tệ một quả, rất ngon. Tôi đã mua 6 quả táo. Tôi còn mua 2 cốc trà và một cái cốc đẹp. Mẹ mua gạo, rau và trái cây. Chủ nói: tổng cộng 25 tệ. Tôi đưa tiền cho chủ, tôi nói cảm ơn. Chủ cũng nói cảm ơn, tạm biệt. Chúng tôi rất vui. Buổi chiều tôi ở nhà ăn táo, uống trà, đọc sách. Tôi thích thứ Bảy.",
    
    "我的朋友": "Tôi có một người bạn tốt, anh ấy tên là Vương Minh. Anh ấy là người Trung Quốc, là người Bắc Kinh. Năm nay anh ấy 20 tuổi. Anh ấy cũng là học sinh, học ở trường của tôi. Anh ấy rất yêu học tập. Anh ấy học tiếng Trung và tiếng Anh, cũng học toán. Giáo viên tiếng Trung và giáo viên tiếng Anh của anh ấy đều nói anh ấy rất tốt. Chúng tôi thường cùng đọc sách ở trường, cùng viết chữ Hán. Anh ấy có rất nhiều sách tiếng Trung, cũng có nhiều sách tiếng Anh. Anh ấy rất thích đọc sách. Thứ Bảy và Chủ Nhật, chúng tôi không đi học. Chúng tôi đi xem phim, cũng đi cửa hàng mua sách. Anh ấy rất thích xem phim Trung Quốc. Anh ấy cũng thích ăn món Trung Quốc, uống trà Trung Quốc. Anh ấy nói món Trung Quốc rất ngon. Gia đình anh ấy cũng ở Bắc Kinh, nhà anh ấy có năm người: bố, mẹ, anh trai, anh ấy và con gái của anh ấy. Anh ấy rất yêu gia đình mình. Tôi rất thích bạn của mình, anh ấy cũng rất thích tôi. Chúng tôi là bạn tốt.",
    
    "在饭店吃饭": "Hôm nay trưa, tôi và bạn tôi Vương Minh cùng đi nhà hàng ăn cơm. Nhà hàng rất lớn, rất đẹp, người cũng rất đông. Chúng tôi ngồi xuống. Một phục vụ đến, cô ấy rất đẹp, cũng rất tốt. Cô ấy hỏi chúng tôi: các anh ăn gì? Tôi nói: tôi muốn ăn cơm và rau. Vương Minh nói: tôi ăn mì. Phục vụ lại hỏi: các anh uống gì? Tôi nói: tôi uống trà, tôi rất thích uống trà. Vương Minh nói: tôi uống nước, tôi không uống trà. Phục vụ nói: được, xin vui lòng đợi một chút. Tôi và Vương Minh đọc sách trong nhà hàng. Chúng tôi đợi 10 phút. Phục vụ đến, cô ấy nói: cơm của các anh đến rồi. Chúng tôi bắt đầu ăn cơm. Cơm rất ngon, rau cũng rất ngon. Chúng tôi ăn rất vui. Ăn xong cơm, chúng tôi đưa tiền cho phục vụ. Chúng tôi nói cảm ơn phục vụ. Phục vụ cũng nói cảm ơn, tạm biệt. Chúng tôi rất vui.",
    
    "我的家": "Nhà tôi có năm người: bố, mẹ, anh trai, tôi và con gái tôi. Chúng tôi đều rất yêu gia đình của mình. Bố tôi là bác sĩ, ông làm việc ở bệnh viện. Ông mỗi ngày đều rất bận, nhưng ông rất yêu công việc của mình. Ông nói ông thích làm bác sĩ. Mẹ tôi là giáo viên, bà làm việc ở trường. Bà dạy tiếng Trung. Học sinh của bà đều rất thích bà. Bà nói bà rất thích làm giáo viên. Anh trai tôi là học sinh, anh ấy học ở đại học Bắc Kinh. Anh ấy học tiếng Anh, cũng học toán. Anh ấy rất yêu học tập, giáo viên của anh ấy nói anh ấy học rất tốt. Tôi cũng là học sinh, tôi học tiếng Trung. Con gái tôi còn nhỏ, nó 3 tuổi. Nó rất đáng yêu, chúng tôi đều rất yêu nó. Chủ Nhật, chúng tôi đều ở nhà. Chúng tôi cùng ăn cơm, cùng xem tivi, cùng xem phim. Chúng tôi rất vui. Tôi rất yêu gia đình của mình.",
    
    "天气和日期": "Hôm nay là ngày 10 tháng 5, thứ Ba. Thời tiết hôm nay rất tốt, không lạnh cũng không nóng, rất thoải mái. Hôm qua trời mưa, rất lạnh. Ngày mai thời tiết thế nào? Tôi không biết. Tôi mỗi sáng đều xem dự báo thời tiết. Thời tiết năm nay rất kỳ lạ. Có lúc rất nóng, có lúc rất lạnh. Tôi không thích thời tiết lạnh, tôi thích thời tiết ấm áp. Tôi hỏi bạn tôi: bạn thích thời tiết gì? Anh ấy nói: tôi thích thời tiết mưa. Khi trời mưa, tôi ở nhà đọc sách, uống trà, rất thoải mái. Tôi nói: ngày mưa tôi không thể ra ngoài, tôi không thích. Anh ấy cười. Chúng tôi đều có sở thích khác nhau. Hôm nay không mưa, tôi rất vui. Tôi muốn ra ngoài mua đồ, gặp bạn, đi nhà hàng ăn cơm. Khi thời tiết tốt, làm gì cũng vui.",
    
    "打电话": "Alo, xin chào! Tôi là Tiểu Minh. Bạn là ai? Bạn có phải Vương Minh không? Đúng, tôi là Vương Minh. Chào bạn, Tiểu Minh! Bây giờ bạn ở đâu? Bây giờ tôi ở nhà. Còn bạn? Tôi ở trường. Hôm nay thứ mấy? Hôm nay thứ Sáu. Ngày mai là thứ Bảy, ngày mai bạn có thời gian không? Có thời gian, sao vậy? Ngày mai tôi muốn đi xem phim, bạn có thể đến không? Tôi có thể đến. Mấy giờ? Chiều 2 giờ, ở cửa rạp chiếu phim, được không? Được, không vấn đề gì. Chúng ta xem xong phim đi nhà hàng ăn cơm, thế nào? Được, tôi cũng muốn ăn món Trung Quốc. Vậy chúng ta gặp nhau ngày mai. Được, gặp nhau ngày mai. Tạm biệt! Tạm biệt! Gọi xong điện thoại, tôi rất vui. Tôi rất thích cùng bạn bè xem phim, cùng ăn cơm. Ngày mai chắc chắn rất thú vị.",
    
    "我的宠物": "Nhà tôi có hai con thú cưng, một con chó và một con mèo. Con chó của tôi tên là Đại Hoàng, con mèo của tôi tên là Tiểu Bạch. Đại Hoàng rất to, Tiểu Bạch rất nhỏ. Chúng đều rất đáng yêu. Năm nay Đại Hoàng 3 tuổi, Tiểu Bạch 1 tuổi. Tôi rất yêu chúng. Mỗi sáng, Đại Hoàng sẽ gọi tôi dậy. Sau khi tôi dậy, cho chúng ăn sáng. Đại Hoàng ăn thức ăn cho chó, Tiểu Bạch ăn thức ăn cho mèo. Ăn xong sáng, Đại Hoàng và Tiểu Bạch chơi ở nhà. Chúng là bạn tốt. Chiều tôi từ trường về nhà, chúng đợi tôi ở cửa. Tôi rất vui khi nhìn thấy chúng. Tối khi tôi làm bài tập, Đại Hoàng ngủ dưới bàn của tôi, Tiểu Bạch ngủ trên ghế của tôi. Tôi viết chữ, chúng ngủ. Tôi rất thích như vậy. Bạn tôi đến nhà tôi, đều rất thích Đại Hoàng và Tiểu Bạch. Chúng làm cuộc sống của tôi rất thú vị.",
    
    "去旅行": "Tháng sau tôi muốn đi du lịch Trung Quốc. Tôi muốn đi máy bay đến Bắc Kinh. Máy bay rất nhanh, tôi rất thích đi máy bay. Tôi cũng có thể đi tàu hỏa, nhưng tàu hỏa rất chậm. Tôi không thích đi taxi, quá đắt. Tôi muốn ở khách sạn ở Bắc Kinh. Phía trước khách sạn có nhiều cửa hàng, phía sau có công viên. Khách sạn đó rất lớn, rất đẹp. Tôi ở Bắc Kinh muốn ăn nhiều món Trung Quốc, uống nhiều trà Trung Quốc. Tôi muốn đi xem Vạn Lý Trường Thành, đi xem Cố Cung. Bạn tôi nói: Bắc Kinh rất đẹp, bạn chắc chắn sẽ thích. Tôi hỏi anh ấy: thời tiết Bắc Kinh thế nào? Anh ấy nói: bây giờ không lạnh không nóng, rất thoải mái. Tôi rất vui. Bây giờ tôi mỗi ngày học tiếng Hán, tôi muốn nói chuyện nói rất tốt. Tôi sẽ mua nhiều sách Trung Quốc và quần áo mang về nhà. Tôi quá muốn đi Trung Quốc!",
    
    "学习和工作": "Tôi là học sinh, anh trai tôi đã đi làm. Tôi mỗi ngày đi học, anh trai mỗi ngày đi công ty làm việc. Tôi học tiếng Hán, tiếng Anh và toán. Giáo viên tiếng Hán của tôi họ Lý, cô ấy là người Trung Quốc. Cô Lý rất tốt, chúng tôi đều rất thích cô ấy. Cô ấy biết nói tiếng Hán và tiếng Anh. Cô ấy thường hỏi chúng tôi: các em biết nói tiếng Hán không? Các em biết viết chữ Hán không? Tôi nói: tôi biết nói một ít tiếng Hán, nhưng nói không tốt lắm. Tôi biết viết một ít chữ Hán, nhưng viết cũng không tốt lắm. Cô Lý nói: không sao, em học rất chăm chỉ, sau này chắc chắn sẽ nói rất tốt. Tôi rất vui. Công việc của anh trai tôi rất bận. Anh ấy mỗi sáng 7 giờ rưỡi đi công ty, tối 6 giờ rưỡi về nhà. Anh ấy nói: anh rất thích công việc của mình. Tuy rất bận, nhưng rất thú vị. Tôi hỏi anh ấy: anh có mệt không? Anh ấy nói: có lúc mệt, nhưng anh rất vui. Xin lỗi, anh phải đi làm, chúng ta tối nói chuyện tiếp. Được, tạm biệt!",
    
    "问路和地点": "Xin lỗi, cho hỏi ga tàu ở đâu? Ga tàu cách đây không xa lắm. Bạn xem, từ đây đi thẳng, phía trước có một cửa hàng lớn. Phía trước cửa hàng là ngân hàng, phía sau là nhà hàng. Bạn thấy nhà hàng đó chưa? Thấy rồi, sau đó thế nào? Bạn đi sang trái, đi 10 phút là đến. Ga tàu rất lớn, rất dễ tìm. Cảm ơn bạn! Không có gì. Bạn là người đâu? Tiếng Hán của bạn nói rất tốt. Cảm ơn! Tôi là học sinh, tôi học tiếng Hán ở đây. Giáo viên của tôi là người Trung Quốc, cô ấy dạy rất tốt. Bạn tên là gì? Tôi tên là Tiểu Minh. Còn bạn? Bạn tên là gì? Tôi họ Vương, tên là Vương Minh. Bạn cũng là học sinh à? Đúng, tôi cũng là học sinh. Tôi học tiếng Anh ở Bắc Kinh. Vậy chúng ta là bạn học rồi. Đúng, chúng ta là bạn học. Rất vui được gặp bạn! Tôi cũng rất vui được gặp bạn! Bây giờ bạn đi đâu? Tôi đi ga tàu đón bạn tôi. Được, vậy bạn đi nhé. Tạm biệt! Tạm biệt!",
    
    "在家里": "Hôm nay Chủ Nhật, tôi không đi học, tôi ở nhà. Nhà của tôi không quá lớn, nhưng rất ấm áp. Trong phòng của tôi có một cái giường, một cái bàn, hai cái ghế, còn có một tủ sách lớn. Trong tủ sách có nhiều sách, có sách tiếng Trung, có sách tiếng Anh. Máy tính của tôi ở trên bàn. Tôi mỗi ngày dùng máy tính học tập, xem phim, nghe nhạc. Quần áo của tôi ở đâu? Ồ, ở trên ghế. Con mèo của tôi ngủ trên giường, con chó của tôi ở cửa. Hôm nay âm 5 độ, bên ngoài rất lạnh. Tôi không muốn ra ngoài, tôi muốn ở nhà đọc sách, xem tivi. Trưa mẹ tôi nấu cơm, chúng tôi cùng ăn cơm. Món mẹ nấu rất ngon. Ăn xong cơm, tôi gọi điện cho bạn tôi. Tôi hỏi anh ấy: bạn ở đâu? Anh ấy nói: tôi đang ăn cơm ở nhà hàng. Tôi nói: ăn xong cơm đến nhà tôi nhé, chúng ta cùng xem phim. Anh ấy nói: được, một lát gặp nhau. Tôi rất vui."
}

def text_to_pinyin(text):
    """Convert Chinese text to pinyin with tone marks"""
    result = pinyin(text, style=Style.TONE, heteronym=False)
    # Join the pinyin syllables
    pinyin_text = ' '.join([item[0] for item in result])
    # Capitalize first letter and add proper punctuation spacing
    sentences = []
    current = []
    for item in result:
        syllable = item[0]
        current.append(syllable)
        # Check if this character is punctuation in original text
        if syllable in ['，', '。', '！', '？', '：', '；']:
            sentence = ' '.join(current[:-1])
            if sentence:
                # Capitalize first letter
                sentence = sentence[0].upper() + sentence[1:] if len(sentence) > 0 else sentence
                sentences.append(sentence + syllable)
            current = []
    
    # Handle remaining
    if current:
        sentence = ' '.join(current)
        sentence = sentence[0].upper() + sentence[1:] if len(sentence) > 0 else sentence
        sentences.append(sentence)
    
    return ' '.join(sentences)

def add_pinyin_and_translation():
    """Add pinyin and Vietnamese translation to all reading passages"""
    
    # Read the current file
    with open('www/data/simplified/reading_hsk1.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Update each dialog
    for dialog in data['dialogs']:
        topic = dialog['topic']
        text = dialog['lines'][0]['text']
        
        # Generate pinyin
        pinyin_text = text_to_pinyin(text)
        
        # Get translation
        translation = TRANSLATIONS.get(topic, "Translation not available")
        
        # Update the dialog
        dialog['lines'][0]['pinyin'] = pinyin_text
        dialog['lines'][0]['translation'] = translation
        
        print(f"✓ {topic}: Added pinyin and translation")
    
    # Save back to file
    with open('www/data/simplified/reading_hsk1.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Đã cập nhật pinyin và bản dịch cho {len(data['dialogs'])} đoạn văn")
    print(f"✓ File đã lưu: www/data/simplified/reading_hsk1.json")

if __name__ == '__main__':
    add_pinyin_and_translation()
