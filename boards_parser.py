import logging
from parse_constructor import map_display_type, map_construction_format
from formatting import extract_size, extract_address, split_sides  
from config import cookies, headers, data
from extract_json import save_to_json
from extract_exl import save_to_excel
import requests

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('parse_logs.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def parse_boards_data():
    logger.info("Начало парсинга данных")
    
    try:
        response = requests.post('https://boards.by/local/ajax/map.php', 
                                cookies=cookies, 
                                headers=headers, 
                                data=data)
        response.raise_for_status()
        logger.info(f"HTTP запрос успешен, статус: {response.status_code}")
        
        res = response.json()
        total_objects = len([k for k, v in res.items() if isinstance(v, dict) and 'ID' in v])
        logger.info(f"Получено объектов: {total_objects}")
        
        construction_sides = []
        error_count = 0
        processed_count = 0

        for gid, obj in res.items():
            if not isinstance(obj, dict) or 'ID' not in obj:
                continue
            
            try:
                lat = float(obj.get('PROPERTY_LONGITUDE_VALUE', 0)) if obj.get('PROPERTY_LONGITUDE_VALUE') else 0
                lon = float(obj.get('PROPERTY_LATITUDE_VALUE', 0)) if obj.get('PROPERTY_LATITUDE_VALUE') else 0
                prop_type = obj.get('PROPERTY_TYPE_VALUE', '')
                display_type = map_display_type(prop_type)
                construction_format = map_construction_format(prop_type)
                size = extract_size(obj.get('NAME', ''))
                address = extract_address(obj.get('NAME', ''))
                side_string = obj.get('PROPERTY_SIDE_VALUE', '')
                sides = split_sides(side_string)
                
                for side in sides:
                    name = side if side else gid
                
                    side_data = {
                        "gid": gid,
                        "address": address,
                        "name": name,
                        "lon": lon,
                        "lat": lat,
                        "construction_format": construction_format,
                        "display_type": display_type,
                        "lighting": None,
                        "size": size,
                        "material": None
                    }
                    construction_sides.append(side_data)
                
                processed_count += 1
                if processed_count % 100 == 0:
                    logger.info(f"Обработано {processed_count} объектов, создано сторон: {len(construction_sides)}")
                    
            except (ValueError, TypeError, KeyError) as e:
                error_count += 1
                logger.warning(f"Ошибка обработки объекта {gid} (тип: {prop_type if 'prop_type' in locals() else 'unknown'}): {e}")
                continue

        result = {"construction_sides": construction_sides}
        
        logger.info(f"Итоги: обработано {processed_count} объектов, ошибок: {error_count}, создано сторон: {len(construction_sides)}")
        
        try:
            save_to_json(result, "result.json")
            save_to_excel(result, "result.xlsx")
            logger.info("Файлы успешно сохранены: result.json, result.xlsx")
        except Exception as e:
            logger.error(f"Ошибка сохранения файлов: {e}", exc_info=True)
        
        return result
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка HTTP запроса: {e}", exc_info=True)
        return {"construction_sides": [], "error": str(e)}
    except ValueError as e:
        logger.error(f"Ошибка парсинга JSON: {e}", exc_info=True)
        return {"construction_sides": [], "error": str(e)}
    except Exception as e:
        logger.error(f"Непредвиденная ошибка: {e}", exc_info=True)
        return {"construction_sides": [], "error": str(e)}