import json
from opencc import OpenCC

# Khởi tạo converter Giản thể -> Phồn thể
cc = OpenCC('s2t')  # Simplified to Traditional

# Phân cấp HSK sang TOCFL (tương đương)
# HSK1-2 ~ TOCFL A1
# HSK3 ~ TOCFL A2
# HSK4-5 ~ TOCFL B1
# HSK6 ~ TOCFL B2
mapping = {
    'hsk1': 'tocfl_a1',
    'hsk2': 'tocfl_a1',
    'hsk3': 'tocfl_a2',
    'hsk4': 'tocfl_b1',
    'hsk5': 'tocfl_b1',
    'hsk6': 'tocfl_b2'
}

# Dictionary để gộp các entries theo TOCFL level
tocfl_data = {
    'tocfl_a1': {'level': 'TOCFL_A1', 'entries': []},
    'tocfl_a2': {'level': 'TOCFL_A2', 'entries': []},
    'tocfl_b1': {'level': 'TOCFL_B1', 'entries': []},
    'tocfl_b2': {'level': 'TOCFL_B2', 'entries': []}
}

print("🔄 Đang chuyển đổi Giản thể sang Phồn thể...\n")

# Đọc từng file HSK và chuyển đổi
for hsk_level, tocfl_level in mapping.items():
    hsk_file = f'www/data/simplified/{hsk_level}.json'
    
    print(f"📖 Đọc {hsk_file}...")
    
    with open(hsk_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Chuyển đổi từng entry sang Phồn thể
    for entry in data['entries']:
        traditional_entry = {
            'hanzi': cc.convert(entry['hanzi']),  # Chuyển sang Phồn thể
            'pinyin': entry['pinyin'],
            'meaning_vi': entry['meaning_vi'],
            'level': tocfl_level.upper().replace('_', ' ')
        }
        tocfl_data[tocfl_level]['entries'].append(traditional_entry)
    
    print(f"  ✅ Chuyển đổi {len(data['entries'])} từ sang {tocfl_level}")

print("\n💾 Đang lưu file TOCFL...\n")

# Lưu từng file TOCFL
for tocfl_level, data in tocfl_data.items():
    output_file = f'www/data/traditional/{tocfl_level}.json'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ {output_file}: {len(data['entries'])} từ vựng")
    
    # Preview 3 từ đầu
    print(f"   🔍 Preview:")
    for i, entry in enumerate(data['entries'][:3], 1):
        print(f"      {i}. {entry['hanzi']} ({entry['pinyin']}) - {entry['meaning_vi']}")
    print()

print("="*50)
print("🎉 HOÀN THÀNH CHUYỂN ĐỔI!")
print("="*50)
print("\n📊 Tổng kết:")
print(f"  TOCFL A1: {len(tocfl_data['tocfl_a1']['entries'])} từ (HSK1 + HSK2)")
print(f"  TOCFL A2: {len(tocfl_data['tocfl_a2']['entries'])} từ (HSK3)")
print(f"  TOCFL B1: {len(tocfl_data['tocfl_b1']['entries'])} từ (HSK4 + HSK5)")
print(f"  TOCFL B2: {len(tocfl_data['tocfl_b2']['entries'])} từ (HSK6)")
print(f"  TỔNG: {sum(len(d['entries']) for d in tocfl_data.values())} từ")
