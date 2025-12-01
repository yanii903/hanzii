import pandas as pd
import json

excel_file = 'FULL TỪ VỰNG HSK1- HSK6.xlsx'

# Danh sách các level cần chuyển đổi
levels = ['HSK1', 'HSK2', 'HSK3', 'HSK4', 'HSK5', 'HSK6']

for level in levels:
    print(f"\n{'='*50}")
    print(f"🔄 Đang chuyển đổi {level}...")
    print(f"{'='*50}")
    
    # Đọc sheet
    df = pd.read_excel(excel_file, sheet_name=level)
    
    # Tạo danh sách entries
    entries = []
    for _, row in df.iterrows():
        hanzi = str(row['Từ mới']).strip()
        pinyin = str(row['Phiên âm']).strip()
        meaning = str(row['Giải thích']).strip()
        
        if hanzi and hanzi != 'nan' and pinyin and pinyin != 'nan':
            entry = {
                "hanzi": hanzi,
                "pinyin": pinyin,
                "meaning_vi": meaning,
                "level": level.upper()
            }
            entries.append(entry)
    
    # Tạo JSON
    output = {
        "level": f"{level.upper()[:3]}_{level[-1]}",
        "entries": entries
    }
    
    # Lưu file
    filename = f'www/data/simplified/{level.lower()}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Đã chuyển đổi {len(entries)} từ vựng")
    print(f"📝 File: {filename}")
    print(f"\n🔍 Preview 3 từ đầu tiên:")
    for i, entry in enumerate(entries[:3], 1):
        print(f"  {i}. {entry['hanzi']} ({entry['pinyin']}) - {entry['meaning_vi']}")

print(f"\n{'='*50}")
print(f"🎉 HOÀN THÀNH TẤT CẢ!")
print(f"{'='*50}")
