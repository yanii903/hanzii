import json
import random
from opencc import OpenCC

def load_vocab(level):
    """Load vocabulary from HSK level file"""
    with open(f'www/data/simplified/{level}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['entries']

def get_word_info(entries):
    """Create a dictionary with word info"""
    word_dict = {}
    for entry in entries:
        word_dict[entry['hanzi']] = {
            'pinyin': entry.get('pinyin', ''),
            'meaning': entry.get('meaning_vi', '')
        }
    return word_dict

def check_word_usage(passages, all_words):
    """Track which words have been used"""
    used_words = set()
    for passage in passages:
        text = passage['lines'][0]['text']
        for word in all_words:
            if word in text:
                used_words.add(word)
    return used_words

# Định nghĩa các nhóm từ theo chủ đề để tạo đoạn văn tự nhiên
READING_PASSAGES_HSK1 = [
    {
        "topic": "我的一天",
        "description": "Một ngày của tôi",
        "text": "我叫小明，我是学生。我家有四个人，爸爸、妈妈、我和我的女儿。我很爱我的家。今天是星期一，我七点起床。我的妈妈做早饭，我吃米饭和苹果。我喝茶，不喝咖啡。八点我去学校。我的学校很大，也很漂亮。我在学校学习中文。我的老师是中国人，她很好。她叫李老师。十二点我和同学在学校吃饭。我们吃米饭和菜。下午我看书，也写汉字。我有很多中文书。四点下课。五点我回家。回家以后，我先做作业，然后吃晚饭。晚上我和爸爸妈妈一起看电视。我们看中国电影。十点我睡觉。我很高兴。我喜欢我的学校，也喜欢我的家。"
    },
    {
        "topic": "去商店买东西",
        "description": "Đi cửa hàng mua đồ",
        "text": "今天是星期六，我不去学校。上午九点，我和妈妈一起去商店买东西。商店很大，里面有很多东西。我看见水、茶、米饭、苹果、杯子、椅子、桌子，还有很多书。商店里的人也很多。水五块钱一瓶，茶六块钱，米饭八块钱。我很喜欢苹果，我问老板：这个苹果多少钱？老板说：三块钱一个，很好吃。我买了六个苹果。我还买了两杯茶和一个漂亮的杯子。妈妈买了米、菜和水果。老板说：一共二十五块钱。我给老板钱，我说谢谢。老板也说谢谢，再见。我们很高兴。下午我在家吃苹果，喝茶，看书。我喜欢星期六。"
    },
    {
        "topic": "我的朋友",
        "description": "Bạn của tôi",
        "text": "我有一个好朋友，他叫王明。他是中国人，是北京人。他今年二十岁。他也是学生，在我的学校学习。他很爱学习。他学习中文和英文，也学习数学。他的中文老师和英文老师都说他很好。我们常常在学校一起看书，一起写汉字。他有很多中文书，也有很多英文书。他很喜欢看书。星期六和星期天，我们不去学校。我们去看电影，也去商店买书。他很喜欢看中国电影。他也喜欢吃中国菜，喝中国茶。他说中国菜很好吃。他的家也在北京，他家有五个人：爸爸、妈妈、哥哥、他和他的女儿。他很爱他的家。我很喜欢我的朋友，他也很喜欢我。我们是好朋友。"
    },
    {
        "topic": "在饭店吃饭",
        "description": "Ăn cơm ở nhà hàng",
        "text": "今天中午，我和我的朋友王明一起去饭店吃饭。饭店很大，很漂亮，人也很多。我们坐下。一个服务员来了，她很漂亮，也很好。她问我们：你们吃什么？我说：我想吃米饭和菜。王明说：我吃面条。服务员又问：你们喝什么？我说：我喝茶，我很喜欢喝茶。王明说：我喝水，我不喝茶。服务员说：好的，请等一下。我和王明在饭店看书。我们等了十分钟。服务员来了，她说：你们的饭来了。我们开始吃饭。饭很好吃，菜也很好吃。我们吃得很高兴。吃完饭，我们给服务员钱。我们说谢谢服务员。服务员也说谢谢，再见。我们很高兴。"
    },
    {
        "topic": "我的家",
        "description": "Gia đình tôi",
        "text": "我家有五个人：爸爸、妈妈、哥哥、我和我的女儿。我们都很爱我们的家。我爸爸是医生，他在医院工作。他每天都很忙，但是他很爱他的工作。他说他喜欢做医生。我妈妈是老师，她在学校工作。她教中文。她的学生都很喜欢她。她说她很喜欢当老师。我哥哥是学生，他在北京的大学学习。他学习英文，也学习数学。他很爱学习，他的老师说他学得很好。我也是学生，我学习中文。我的女儿很小，她三岁。她很可爱，我们都很爱她。星期天，我们都在家。我们一起吃饭，一起看电视，一起看电影。我们很高兴。我很爱我的家。"
    },
    {
        "topic": "天气和日期",
        "description": "Thời tiết và ngày tháng",
        "text": "今天是五月十日，星期二。今天的天气很好，不冷也不热，很舒服。昨天下雨了，很冷。明天天气怎么样？我不知道。我每天早上都看天气预报。今年的天气很奇怪。有时候很热，有时候很冷。我不喜欢冷天气，我喜欠暖和的天气。我问我的朋友：你喜欢什么天气？他说：我喜欢下雨的天气。下雨的时候，我在家看书，喝茶，很舒服。我说：下雨天我不能出去，我不喜欢。他笑了。我们都有不同的喜好。今天不下雨，我很高兴。我要出去买东西，去看朋友，去饭馆吃饭。天气好的时候，做什么都很开心。"
    },
    {
        "topic": "打电话",
        "description": "Gọi điện thoại",
        "text": "喂，你好！我是小明。你是谁？你是王明吗？对，我是王明。你好，小明！你现在在哪里？我现在在家。你呢？我在学校。今天星期几？今天星期五。明天是星期六，你明天有时间吗？有时间，怎么了？明天我想去看电影，你能来吗？我能来。几点？下午两点，在电影院门口，好吗？好的，没问题。我们看完电影去饭馆吃饭，怎么样？好啊，我也想吃中国菜。那我们明天见。好，明天见。再见！再见！打完电话，我很高兴。我很喜欢和朋友一起看电影，一起吃饭。明天一定很有意思。"
    },
    {
        "topic": "我的宠物",
        "description": "Thú cưng của tôi",
        "text": "我家有两只宠物，一只狗和一只猫。我的狗叫大黄，我的猫叫小白。大黄很大，小白很小。它们都很可爱。大黄今年三岁，小白今年一岁。我很爱它们。每天早上，大黄会叫我起床。我起床以后，给它们吃早饭。大黄吃狗粮，小白吃猫粮。吃完早饭，大黄和小白在家玩。它们是好朋友。下午我从学校回家，它们在门口等我。我很高兴看到它们。晚上我做作业的时候，大黄在我的桌子下面睡觉，小白在我的椅子上睡觉。我写字，它们睡觉。我很喜欢这样。我的朋友来我家，都很喜欢大黄和小白。它们让我的生活很有意思。"
    },
    {
        "topic": "去旅行",
        "description": "Đi du lịch",
        "text": "下个月我想去中国旅行。我想坐飞机去北京。飞机很快，我很喜欢坐飞机。我也可以坐火车，但是火车很慢。我不喜欢坐出租车，太贵了。我想住在北京的饭店。饭店前面有很多商店，后面有公园。那个饭店很大，很漂亮。我在北京想吃很多中国菜，喝很多中国茶。我想去看长城，去看故宫。我的朋友说：北京很漂亮，你一定会喜欢。我问他：北京的天气怎么样？他说：现在不冷不热，很舒服。我很高兴。我现在每天学汉语，我想说话说得很好。我会买很多中国书和衣服带回家。我太想去中国了！"
    },
    {
        "topic": "学习和工作",
        "description": "Học tập và làm việc",
        "text": "我是学生，我哥哥工作了。我每天去学校学习，哥哥每天去公司工作。我学汉语、英语和数学。我的汉语老师姓李，她是中国人。李老师很好，我们都很喜欢她。她会说汉语和英语。她常常问我们：你们会说汉语吗？你们会写汉字吗？我说：我会说一些汉语，但是说得不太好。我会写一些汉字，但是写得也不太好。李老师说：没关系，你学得很认真，以后一定会说得很好。我很高兴。我哥哥的工作很忙。他每天早上七点半去公司，晚上六点半回家。他说：我很喜欢我的工作。虽然很忙，但是很有意思。我问他：你累不累？他说：有时候累，但是我很快乐。对不起，我要去工作了，我们晚上再说话。好的，再见！"
    },
    {
        "topic": "问路和地点",
        "description": "Hỏi đường và địa điểm",
        "text": "对不起，请问火车站在哪里？火车站离这里不太远。你看，你从这里往前走，前面有一个大商店。商店的前面是银行，后面是饭馆。你看见那个饭馆了吗？看见了，然后呢？你往左走，走十分钟就到了。火车站很大，很好找。谢谢你！不客气。你是哪里人？你的汉语说得很好。谢谢！我是学生，我在这里学汉语。我的老师是中国人，她教得很好。你叫什么名字？我叫小明。你呢？你叫什么？我姓王，叫王明。你也是学生吗？对，我也是学生。我在北京学英语。那我们是同学了。对，我们是同学。很高兴认识你！我也很高兴认识你！你现在去哪里？我去火车站接我的朋友。好，那你去吧。再见！再见！"
    },
    {
        "topic": "在家里",
        "description": "Ở nhà",
        "text": "今天星期日，我不去学校，我在家里。我的家不太大，但是很温暖。我的房间里有一张床，一张桌子，两把椅子，还有一个大书柜。书柜里有很多书，有中文书，有英文书。我的电脑在桌子上。我每天用电脑学习，看电影，听音乐。我的衣服在哪里？哦，在椅子上。我的猫在床上睡觉，我的狗在门口。今天零下五度，外面很冷。我不想出去，我想在家里看书，看电视。中午我妈妈做饭，我们一起吃饭。妈妈做的菜很好吃。吃完饭，我给我的朋友打电话。我问他：你在哪儿？他说：我在饭馆吃饭。我说：吃完饭来我家吧，我们一起看电影。他说：好的，一会儿见。我很高兴。"
    }
]

def generate_reading_data_hsk1():
    """Generate complete reading data for HSK1 with full vocabulary coverage"""
    
    # Load vocabulary
    vocab_entries = load_vocab('hsk1')
    word_dict = get_word_info(vocab_entries)
    all_words = set(word_dict.keys())
    
    print(f"Tổng số từ HSK1: {len(all_words)}")
    
    dialogs = []
    
    # Convert passages to full format
    for passage in READING_PASSAGES_HSK1:
        text = passage['text']
        
        # Generate pinyin (simplified - in real case you'd use a library)
        # For now, we'll mark it as TODO
        pinyin = "TODO: Add pinyin"
        translation = "TODO: Add translation"
        
        dialog = {
            "topic": passage['topic'],
            "description": passage['description'],
            "lines": [{
                "speaker": "",
                "text": text,
                "pinyin": pinyin,
                "translation": translation
            }]
        }
        dialogs.append(dialog)
    
    # Check coverage
    used_words = check_word_usage(dialogs, all_words)
    missing_words = all_words - used_words
    coverage = len(used_words) / len(all_words) * 100
    
    print(f"\nĐộ phủ từ vựng: {coverage:.2f}%")
    print(f"Số từ đã sử dụng: {len(used_words)}")
    print(f"Số từ còn thiếu: {len(missing_words)}")
    
    if missing_words:
        print(f"\n{len(missing_words)} từ còn thiếu:")
        missing_list = sorted(list(missing_words))
        for i in range(0, len(missing_list), 10):
            print('  ', ', '.join(missing_list[i:i+10]))
    
    # Calculate passage lengths
    lengths = [len(d['lines'][0]['text']) for d in dialogs]
    print(f"\nSố đoạn văn: {len(dialogs)}")
    print(f"Độ dài trung bình: {sum(lengths)/len(lengths):.0f} ký tự")
    print(f"Độ dài ngắn nhất: {min(lengths)} ký tự")
    print(f"Độ dài dài nhất: {max(lengths)} ký tự")
    
    # Save to file
    output = {"dialogs": dialogs}
    with open('www/data/simplified/reading_hsk1.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Đã lưu vào www/data/simplified/reading_hsk1.json")
    print(f"  (Lưu ý: Cần bổ sung pinyin và bản dịch tiếng Việt)")

if __name__ == '__main__':
    generate_reading_data_hsk1()
