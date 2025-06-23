from pathlib import Path
from clear_data import read_excel
from make_folder import OUT_DIR, IN_DIR

def process_all_excels():
    excel_files = list(IN_DIR.glob("*.xlsx"))

    for file_path in excel_files:
        print(f"📄 처리 중: {file_path.name}")
        level1, level2, level3 = read_excel(file_path)

        if not level1.empty:
            out_name = file_path.stem
            
            level1.to_csv(OUT_DIR / f"{out_name}_1급 질병 발병 횟수_level1.csv", encoding="utf-8-sig")
            level2.to_csv(OUT_DIR / f"{out_name}_2급 질병 발병 횟수_level2.csv", encoding="utf-8-sig")
            level3.to_csv(OUT_DIR / f"{out_name}_3급 질병 발병 횟수_level3.csv", encoding="utf-8-sig")
        else:
            print(f"⚠️{file_path.name} -> 처리 실패 또는 빈 데이터")
            

if __name__ == "__main__":
    process_all_excels()