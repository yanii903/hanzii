import json
from opencc import OpenCC

# Khởi tạo converter
cc = OpenCC('s2t')

print("🔄 Đang tạo TOCFL C1 và C2 từ HSK6...\n")

# Đọc HSK6
with open('www/data/simplified/hsk6.json', 'r', encoding='utf-8') as f:
    hsk6_data = json.load(f)

total_entries = len(hsk6_data['entries'])
print(f"📖 HSK6 có {total_entries} từ vựng")

# Chia làm 3 phần: B2, C1, C2
split_b2 = total_entries // 3  # 1/3 đầu cho B2
split_c1 = (total_entries * 2) // 3  # 1/3 giữa cho C1, 1/3 cuối cho C2

print(f"   - TOCFL B2: {split_b2} từ (từ 0-{split_b2-1})")
print(f"   - TOCFL C1: {split_c1 - split_b2} từ (từ {split_b2}-{split_c1-1})")
print(f"   - TOCFL C2: {total_entries - split_c1} từ (từ {split_c1}-{total_entries-1})")

# Tạo B2 (1/3 đầu)
tocfl_b2 = {
    'level': 'TOCFL_B2',
    'entries': []
}

for entry in hsk6_data['entries'][:split_b2]:
    tocfl_b2['entries'].append({
        'hanzi': cc.convert(entry['hanzi']),
        'pinyin': entry['pinyin'],
        'meaning_vi': entry['meaning_vi'],
        'level': 'TOCFL B2'
    })

# Tạo C1 (1/3 giữa)
tocfl_c1 = {
    'level': 'TOCFL_C1',
    'entries': []
}

for entry in hsk6_data['entries'][split_b2:split_c1]:
    tocfl_c1['entries'].append({
        'hanzi': cc.convert(entry['hanzi']),
        'pinyin': entry['pinyin'],
        'meaning_vi': entry['meaning_vi'],
        'level': 'TOCFL C1'
    })

# Tạo C2 (1/3 cuối)
tocfl_c2 = {
    'level': 'TOCFL_C2',
    'entries': []
}

for entry in hsk6_data['entries'][split_c1:]:
    tocfl_c2['entries'].append({
        'hanzi': cc.convert(entry['hanzi']),
        'pinyin': entry['pinyin'],
        'meaning_vi': entry['meaning_vi'],
        'level': 'TOCFL C2'
    })

print("\n💾 Đang lưu file...\n")

# Lưu B2 (cập nhật lại)
with open('www/data/traditional/tocfl_b2.json', 'w', encoding='utf-8') as f:
    json.dump(tocfl_b2, f, ensure_ascii=False, indent=2)
print(f"✅ tocfl_b2.json: {len(tocfl_b2['entries'])} từ vựng")
for i, entry in enumerate(tocfl_b2['entries'][:3], 1):
    print(f"   {i}. {entry['hanzi']} ({entry['pinyin']}) - {entry['meaning_vi']}")

# Lưu C1
with open('www/data/traditional/tocfl_c1.json', 'w', encoding='utf-8') as f:
    json.dump(tocfl_c1, f, ensure_ascii=False, indent=2)
print(f"\n✅ tocfl_c1.json: {len(tocfl_c1['entries'])} từ vựng")
for i, entry in enumerate(tocfl_c1['entries'][:3], 1):
    print(f"   {i}. {entry['hanzi']} ({entry['pinyin']}) - {entry['meaning_vi']}")

# Lưu C2
with open('www/data/traditional/tocfl_c2.json', 'w', encoding='utf-8') as f:
    json.dump(tocfl_c2, f, ensure_ascii=False, indent=2)
print(f"\n✅ tocfl_c2.json: {len(tocfl_c2['entries'])} từ vựng")
for i, entry in enumerate(tocfl_c2['entries'][:3], 1):
    print(f"   {i}. {entry['hanzi']} ({entry['pinyin']}) - {entry['meaning_vi']}")

print("\n" + "="*50)
print("🎉 HOÀN THÀNH!")
print("="*50)
print("\n📊 TOCFL Phồn thể:")
print(f"  A1: 299 từ")
print(f"  A2: 295 từ")
print(f"  B1: 1,895 từ")
print(f"  B2: {len(tocfl_b2['entries'])} từ")
print(f"  C1: {len(tocfl_c1['entries'])} từ (MỚI)")
print(f"  C2: {len(tocfl_c2['entries'])} từ (MỚI)")
print(f"  TỔNG: {299 + 295 + 1895 + len(tocfl_b2['entries']) + len(tocfl_c1['entries']) + len(tocfl_c2['entries'])} từ")
