#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to add examples and grammar patterns to vocabulary JSON files
"""

import json
import os

# Sample examples database - you can expand this
EXAMPLES_DB = {
    # HSK1 Common words
    "爱": {
        "examples": [
            {"hanzi": "我爱你。", "pinyin": "Wǒ ài nǐ.", "meaning_vi": "Tôi yêu bạn."},
            {"hanzi": "我爱中国。", "pinyin": "Wǒ ài Zhōngguó.", "meaning_vi": "Tôi yêu Trung Quốc."},
            {"hanzi": "他爱学习。", "pinyin": "Tā ài xuéxí.", "meaning_vi": "Anh ấy thích học tập."}
        ],
        "grammar": "动词 (Động từ) - Biểu thị tình cảm yêu thích",
        "usage": "爱 + 名词/动词"
    },
    "吃": {
        "examples": [
            {"hanzi": "我吃饭。", "pinyin": "Wǒ chī fàn.", "meaning_vi": "Tôi ăn cơm."},
            {"hanzi": "你吃什么？", "pinyin": "Nǐ chī shénme?", "meaning_vi": "Bạn ăn gì?"},
            {"hanzi": "他不吃肉。", "pinyin": "Tā bù chī ròu.", "meaning_vi": "Anh ấy không ăn thịt."}
        ],
        "grammar": "动词 (Động từ) - Hành động ăn uống",
        "usage": "吃 + 食物"
    },
    "喝": {
        "examples": [
            {"hanzi": "我喝水。", "pinyin": "Wǒ hē shuǐ.", "meaning_vi": "Tôi uống nước."},
            {"hanzi": "他喝咖啡。", "pinyin": "Tā hē kāfēi.", "meaning_vi": "Anh ấy uống cà phê."},
            {"hanzi": "你喝茶吗？", "pinyin": "Nǐ hē chá ma?", "meaning_vi": "Bạn uống trà không?"}
        ],
        "grammar": "动词 (Động từ) - Hành động uống",
        "usage": "喝 + 饮料"
    },
    "是": {
        "examples": [
            {"hanzi": "我是学生。", "pinyin": "Wǒ shì xuéshēng.", "meaning_vi": "Tôi là sinh viên."},
            {"hanzi": "他是老师。", "pinyin": "Tā shì lǎoshī.", "meaning_vi": "Anh ấy là giáo viên."},
            {"hanzi": "这是书。", "pinyin": "Zhè shì shū.", "meaning_vi": "Đây là sách."}
        ],
        "grammar": "系动词 (Động từ \"là\") - Cấu trúc A是B",
        "usage": "主语 + 是 + 名词"
    },
    "有": {
        "examples": [
            {"hanzi": "我有书。", "pinyin": "Wǒ yǒu shū.", "meaning_vi": "Tôi có sách."},
            {"hanzi": "他有三个孩子。", "pinyin": "Tā yǒu sān gè háizi.", "meaning_vi": "Anh ấy có ba đứa con."},
            {"hanzi": "你有时间吗？", "pinyin": "Nǐ yǒu shíjiān ma?", "meaning_vi": "Bạn có thời gian không?"}
        ],
        "grammar": "动词 (Động từ) - Biểu thị sở hữu hoặc tồn tại",
        "usage": "主语 + 有 + 宾语"
    },
    "在": {
        "examples": [
            {"hanzi": "我在家。", "pinyin": "Wǒ zài jiā.", "meaning_vi": "Tôi ở nhà."},
            {"hanzi": "他在北京工作。", "pinyin": "Tā zài Běijīng gōngzuò.", "meaning_vi": "Anh ấy làm việc ở Bắc Kinh."},
            {"hanzi": "书在桌子上。", "pinyin": "Shū zài zhuōzi shàng.", "meaning_vi": "Sách ở trên bàn."}
        ],
        "grammar": "动词/介词 - Biểu thị vị trí hoặc đang làm gì",
        "usage": "在 + 地点 hoặc 在 + 动词"
    },
    "去": {
        "examples": [
            {"hanzi": "我去学校。", "pinyin": "Wǒ qù xuéxiào.", "meaning_vi": "Tôi đi học."},
            {"hanzi": "他去中国。", "pinyin": "Tā qù Zhōngguó.", "meaning_vi": "Anh ấy đi Trung Quốc."},
            {"hanzi": "你去哪儿？", "pinyin": "Nǐ qù nǎr?", "meaning_vi": "Bạn đi đâu?"}
        ],
        "grammar": "动词 (Động từ) - Hành động đi đến",
        "usage": "去 + 地点"
    },
    "来": {
        "examples": [
            {"hanzi": "我来了。", "pinyin": "Wǒ lái le.", "meaning_vi": "Tôi đến rồi."},
            {"hanzi": "他来中国。", "pinyin": "Tā lái Zhōngguó.", "meaning_vi": "Anh ấy đến Trung Quốc."},
            {"hanzi": "你来吗？", "pinyin": "Nǐ lái ma?", "meaning_vi": "Bạn đến không?"}
        ],
        "grammar": "动词 (Động từ) - Hành động đến",
        "usage": "来 + 地点 hoặc 来 + 动词"
    },
    "看": {
        "examples": [
            {"hanzi": "我看书。", "pinyin": "Wǒ kàn shū.", "meaning_vi": "Tôi đọc sách."},
            {"hanzi": "看电视", "pinyin": "kàn diànshì", "meaning_vi": "xem TV"},
            {"hanzi": "我看看。", "pinyin": "Wǒ kànkan.", "meaning_vi": "Để tôi xem."}
        ],
        "grammar": "动词 (Động từ) - Nhìn, xem, đọc",
        "usage": "看 + 宾语"
    },
    "听": {
        "examples": [
            {"hanzi": "我听音乐。", "pinyin": "Wǒ tīng yīnyuè.", "meaning_vi": "Tôi nghe nhạc."},
            {"hanzi": "听老师说", "pinyin": "tīng lǎoshī shuō", "meaning_vi": "nghe thầy nói"},
            {"hanzi": "你听我说。", "pinyin": "Nǐ tīng wǒ shuō.", "meaning_vi": "Bạn nghe tôi nói."}
        ],
        "grammar": "动词 (Động từ) - Nghe",
        "usage": "听 + 宾语"
    },
    "说": {
        "examples": [
            {"hanzi": "我说中文。", "pinyin": "Wǒ shuō Zhōngwén.", "meaning_vi": "Tôi nói tiếng Trung."},
            {"hanzi": "他说得很好。", "pinyin": "Tā shuō de hěn hǎo.", "meaning_vi": "Anh ấy nói rất tốt."},
            {"hanzi": "你说什么？", "pinyin": "Nǐ shuō shénme?", "meaning_vi": "Bạn nói gì?"}
        ],
        "grammar": "动词 (Động từ) - Nói",
        "usage": "说 + 语言/内容"
    },
    "读": {
        "examples": [
            {"hanzi": "我读书。", "pinyin": "Wǒ dú shū.", "meaning_vi": "Tôi đọc sách."},
            {"hanzi": "他读大学。", "pinyin": "Tā dú dàxué.", "meaning_vi": "Anh ấy học đại học."},
            {"hanzi": "读一读", "pinyin": "dú yī dú", "meaning_vi": "đọc thử"}
        ],
        "grammar": "动词 (Động từ) - Đọc, học",
        "usage": "读 + 宾语"
    },
    "写": {
        "examples": [
            {"hanzi": "我写字。", "pinyin": "Wǒ xiě zì.", "meaning_vi": "Tôi viết chữ."},
            {"hanzi": "写作业", "pinyin": "xiě zuòyè", "meaning_vi": "làm bài tập"},
            {"hanzi": "他写了一本书。", "pinyin": "Tā xiě le yì běn shū.", "meaning_vi": "Anh ấy đã viết một cuốn sách."}
        ],
        "grammar": "动词 (Động từ) - Viết",
        "usage": "写 + 宾语"
    },
    "学习": {
        "examples": [
            {"hanzi": "我学习中文。", "pinyin": "Wǒ xuéxí Zhōngwén.", "meaning_vi": "Tôi học tiếng Trung."},
            {"hanzi": "他很爱学习。", "pinyin": "Tā hěn ài xuéxí.", "meaning_vi": "Anh ấy rất thích học."},
            {"hanzi": "学习汉语很有意思。", "pinyin": "Xuéxí Hànyǔ hěn yǒuyìsi.", "meaning_vi": "Học tiếng Hán rất thú vị."}
        ],
        "grammar": "动词 (Động từ) - Học tập",
        "usage": "学习 + 科目/内容"
    },
    "工作": {
        "examples": [
            {"hanzi": "我在北京工作。", "pinyin": "Wǒ zài Běijīng gōngzuò.", "meaning_vi": "Tôi làm việc ở Bắc Kinh."},
            {"hanzi": "他的工作很忙。", "pinyin": "Tā de gōngzuò hěn máng.", "meaning_vi": "Công việc của anh ấy rất bận."},
            {"hanzi": "找工作", "pinyin": "zhǎo gōngzuò", "meaning_vi": "tìm việc"}
        ],
        "grammar": "动词/名词 - Làm việc / Công việc",
        "usage": "在 + 地点 + 工作 hoặc N的工作"
    },
    "买": {
        "examples": [
            {"hanzi": "我买书。", "pinyin": "Wǒ mǎi shū.", "meaning_vi": "Tôi mua sách."},
            {"hanzi": "他买了一件衣服。", "pinyin": "Tā mǎi le yí jiàn yīfu.", "meaning_vi": "Anh ấy đã mua một bộ quần áo."},
            {"hanzi": "在哪儿买？", "pinyin": "Zài nǎr mǎi?", "meaning_vi": "Mua ở đâu?"}
        ],
        "grammar": "动词 (Động từ) - Mua",
        "usage": "买 + 商品"
    },
    "想": {
        "examples": [
            {"hanzi": "我想学中文。", "pinyin": "Wǒ xiǎng xué Zhōngwén.", "meaning_vi": "Tôi muốn học tiếng Trung."},
            {"hanzi": "他想去中国。", "pinyin": "Tā xiǎng qù Zhōngguó.", "meaning_vi": "Anh ấy muốn đi Trung Quốc."},
            {"hanzi": "你想吃什么？", "pinyin": "Nǐ xiǎng chī shénme?", "meaning_vi": "Bạn muốn ăn gì?"}
        ],
        "grammar": "助动词 (Trợ động từ) - Muốn, nghĩ",
        "usage": "想 + 动词"
    },
    "会": {
        "examples": [
            {"hanzi": "我会说中文。", "pinyin": "Wǒ huì shuō Zhōngwén.", "meaning_vi": "Tôi biết nói tiếng Trung."},
            {"hanzi": "他会开车。", "pinyin": "Tā huì kāichē.", "meaning_vi": "Anh ấy biết lái xe."},
            {"hanzi": "你会不会？", "pinyin": "Nǐ huì bu huì?", "meaning_vi": "Bạn có biết không?"}
        ],
        "grammar": "助动词 (Trợ động từ) - Biết (khả năng học được)",
        "usage": "会 + 动词"
    },
    "能": {
        "examples": [
            {"hanzi": "我能帮你。", "pinyin": "Wǒ néng bāng nǐ.", "meaning_vi": "Tôi có thể giúp bạn."},
            {"hanzi": "这里不能抽烟。", "pinyin": "Zhèlǐ bù néng chōuyān.", "meaning_vi": "Ở đây không được hút thuốc."},
            {"hanzi": "你能来吗？", "pinyin": "Nǐ néng lái ma?", "meaning_vi": "Bạn có thể đến không?"}
        ],
        "grammar": "助动词 (Trợ động từ) - Có thể, được phép",
        "usage": "能 + 动词"
    },
    "可以": {
        "examples": [
            {"hanzi": "我可以进来吗？", "pinyin": "Wǒ kěyǐ jìnlái ma?", "meaning_vi": "Tôi có thể vào không?"},
            {"hanzi": "你可以用我的电脑。", "pinyin": "Nǐ kěyǐ yòng wǒ de diànnǎo.", "meaning_vi": "Bạn có thể dùng máy tính của tôi."},
            {"hanzi": "可以帮我吗？", "pinyin": "Kěyǐ bāng wǒ ma?", "meaning_vi": "Có thể giúp tôi không?"}
        ],
        "grammar": "助动词 (Trợ động từ) - Có thể, cho phép",
        "usage": "可以 + 动词"
    }
}

def add_examples_to_entries(entries):
    """Add examples and grammar info to vocabulary entries"""
    updated_entries = []
    
    for entry in entries:
        hanzi = entry.get("hanzi", "")
        
        # Create updated entry with original data
        updated_entry = entry.copy()
        
        # Add examples if available
        if hanzi in EXAMPLES_DB:
            updated_entry["examples"] = EXAMPLES_DB[hanzi]["examples"]
            updated_entry["grammar"] = EXAMPLES_DB[hanzi]["grammar"]
            updated_entry["usage"] = EXAMPLES_DB[hanzi]["usage"]
        else:
            # Add empty arrays for words without examples
            updated_entry["examples"] = []
            updated_entry["grammar"] = ""
            updated_entry["usage"] = ""
        
        updated_entries.append(updated_entry)
    
    return updated_entries

def process_json_file(input_path, output_path=None):
    """Process a JSON file and add examples"""
    if output_path is None:
        output_path = input_path
    
    try:
        # Read original file
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Add examples to entries
        if "entries" in data:
            data["entries"] = add_examples_to_entries(data["entries"])
        
        # Write updated file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Processed: {input_path}")
        return True
    
    except Exception as e:
        print(f"✗ Error processing {input_path}: {e}")
        return False

def main():
    """Main function to process all vocabulary files"""
    base_path = os.path.join("www", "data")
    
    # Simplified Chinese files
    simplified_files = [
        "hsk1.json", "hsk2.json", "hsk3.json",
        "hsk4.json", "hsk5.json", "hsk6.json"
    ]
    
    # Traditional Chinese files
    traditional_files = [
        "tocfl_a1.json", "tocfl_a2.json", "tocfl_b1.json",
        "tocfl_b2.json", "tocfl_c1.json", "tocfl_c2.json"
    ]
    
    print("Adding examples to vocabulary files...\n")
    
    # Process simplified files
    print("Processing Simplified Chinese files:")
    for filename in simplified_files:
        file_path = os.path.join(base_path, "simplified", filename)
        if os.path.exists(file_path):
            process_json_file(file_path)
        else:
            print(f"⚠ File not found: {file_path}")
    
    print("\nProcessing Traditional Chinese files:")
    # Process traditional files
    for filename in traditional_files:
        file_path = os.path.join(base_path, "traditional", filename)
        if os.path.exists(file_path):
            process_json_file(file_path)
        else:
            print(f"⚠ File not found: {file_path}")
    
    print("\n✓ Done! All files have been processed.")
    print("\nNote: You can expand the EXAMPLES_DB dictionary to add more examples.")

if __name__ == "__main__":
    main()
