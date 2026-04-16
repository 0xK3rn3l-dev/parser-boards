def map_display_type(prop_type):
    """
    Правила:
    - Призматрон, Призмавижн → Призматрон
    - Скролл → Скроллер
    - LED - экран, Светодиодный экран, Экран → Видеоэкран
    - Обычная плоскость без признаков смены изображения → Статика
    """
    if not prop_type:
        return "Статика"
    
    prop_type_lower = prop_type.lower()
    
    if any(word in prop_type_lower for word in ['призматрон', 'призмавижн', 'призма']):
        return "Призматрон"
    elif 'скролл' in prop_type_lower:
        return "Скроллер"
    elif any(word in prop_type_lower for word in ['led', 'светодиод', 'экран']):
        return "Видеоэкран"
    else:
        return "Статика"
    


def map_construction_format(prop_type):
    """
    Правила:
    - Билборд → Билборды
    - Арка → Арки
    - Путепровод → Мосты
    - Брандмауэр → Брандмауэры
    - Ситиборд → Ситиборды
    - Световой короб → Сити-форматы или Нетиповые форматы (здесь используем Нетиповые форматы)
    - Юнипол, Мегаборд → Нетиповые форматы
    - Неизвестный формат → Нетиповые форматы
    """
    if not prop_type:
        return "Нетиповые форматы"
    
    prop_type_lower = prop_type.lower()
    
    mapping = {
        'билборд': 'Билборды',
        'арка': 'Арки',
        'путепровод': 'Мосты',
        'брандмауэр': 'Брандмауэры',
        'ситиборд': 'Ситиборды',
    }
    
    for key, value in mapping.items():
        if key in prop_type_lower:
            return value
    
    if 'световой короб' in prop_type_lower or 'световой' in prop_type_lower:
        return "Нетиповые форматы"
    elif any(word in prop_type_lower for word in ['юнипол', 'мегаборд']):
        return "Нетиповые форматы"
    
    return "Нетиповые форматы"