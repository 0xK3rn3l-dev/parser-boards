import os
import pandas as pd


def save_to_excel(data, filename="result.xlsx", output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    
    # Если data это словарь с ключом construction_sides
    if isinstance(data, dict) and "construction_sides" in data:
        df = pd.DataFrame(data["construction_sides"])
    else:
        df = pd.DataFrame(data)
    
    df.to_excel(filepath, index=False, engine='openpyxl')
    print(f"[+] Данные сохранены в {filepath}")
    return filepath