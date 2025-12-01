import pandas as pd

excel_file = 'FULL TỪ VỰNG HSK1- HSK6.xlsx'

# Kiểm tra cấu trúc
xl = pd.ExcelFile(excel_file)
print(f"📋 Danh sách sheet:")
for i, sheet in enumerate(xl.sheet_names, 1):
    print(f"  {i}. {sheet}")

print(f"\n" + "="*50)
print("📊 Đọc sheet đầu tiên để xem cấu trúc:")
print("="*50)

df = pd.read_excel(excel_file, sheet_name=0, nrows=10)
print(f"\nCác cột: {list(df.columns)}")
print(f"\n{df.to_string()}")
