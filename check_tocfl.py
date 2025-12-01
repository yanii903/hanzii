import pandas as pd

excel_file = 'FULL TỪ VỰNG HSK1- HSK6.xlsx'

# Kiểm tra xem có sheet TOCFL không
xl = pd.ExcelFile(excel_file)
print(f"📋 Danh sách tất cả các sheet:")
for i, sheet in enumerate(xl.sheet_names, 1):
    print(f"  {i}. {sheet}")
    
# Tìm các sheet có chứa TOCFL hoặc A1, A2, B1, B2
tocfl_sheets = [s for s in xl.sheet_names if 'TOCFL' in s.upper() or any(level in s.upper() for level in ['A1', 'A2', 'B1', 'B2'])]

if tocfl_sheets:
    print(f"\n✅ Tìm thấy {len(tocfl_sheets)} sheet TOCFL:")
    for sheet in tocfl_sheets:
        print(f"  - {sheet}")
else:
    print(f"\n❌ Không tìm thấy sheet TOCFL")
    print(f"\nVui lòng cho biết file Excel có dữ liệu TOCFL không?")
