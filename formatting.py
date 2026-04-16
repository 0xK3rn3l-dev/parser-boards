import re

def extract_size(name):
    """Извлечение размера из названия (например, 6x3, 12x3, 1.2x1.8)"""
    patterns = [
        r'(\d+(?:\.\d+)?)\s*[xх×]\s*(\d+(?:\.\d+)?)',
        r'(\d+(?:\.\d+)?)\s*[на]\s*(\d+(?:\.\d+)?)',
        r'(\d+(?:\.\d+)?)[xх×](\d+(?:\.\d+)?)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, name, re.IGNORECASE)
        if match:
            return f"{match.group(1)}x{match.group(2)}"
    return None


def extract_address(name):
    """Извлечение полного адреса из названия"""
    address = re.sub(r'^№\s*\d+\s*', '', name)
    address = re.sub(r'\s*\(?\d+(?:\.\d+)?\s*[xх×]\s*\d+(?:\.\d+)?\)?', '', address)
    return address.strip()


def split_sides(side_string):
    """
    Разделяет строку со сторонами на список отдельных сторон
    Примеры:
    "А" -> ["А"]
    "А,В" -> ["А", "В"]
    "А, В" -> ["А", "В"]
    """
    if not side_string:
        return [None]
    cleaned = side_string.replace('Сторона', '').strip()
    sides = [s.strip() for s in cleaned.split(',') if s.strip()]
    if not sides:
        return [side_string.strip()]
    return sides