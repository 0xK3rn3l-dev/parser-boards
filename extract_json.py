import json
import os


def save_to_json(data, filename="result.json", output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
    
    print(f"[+] Данные сохранены в {filepath}")
    return filepath