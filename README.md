# Boards.by Parser

Парсер данных рекламных конструкций с сайта [boards.by](https://boards.by). Извлекает информацию о билбордах, ситибордах и других рекламных поверхностях, преобразует в целевой формат JSON и Excel.

## Структура проекта

output/               -  Результаты парсинга
venv/                 -  Виртуальное окружение
API-data.json         -  Пример ответа API (для отладки)
boards_parser.py      -  Основной модуль парсинга
parse_constructor.py  -  Маппинг типов конструкций
formatting.py         -  Форматирование
extract_json.py       -  Сохранение в JSON
extract_exl.py        -  Сохранение в Excel
main.py               -  Точка входа
requirements.txt      -  Зависимости
dev.note.txt          -  Заметки разработчика


## Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd <project-directory>
```
2.  Создайте виртуальное окружение:
```bash
python -m venv venv
```
3. Активируйте виртуальное окружение:
Windows:
```bash
venv\Scripts\activate
```
Linux/MacOS:
```bash
source venv/bin/activate
```
4. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Запуск
```bash
python main.py boards_parser
```
После выполнения в папке output/ появятся файлы:

    result.json — данные в формате JSON

    result.xlsx — данные в формате Excel


## Логика работы

1. Загрузка данных

Парсер отправляет POST-запрос к API https://boards.by/local/ajax/map.php с необходимыми cookies и заголовками.

2. Обработка данных

Для каждого объекта извлекаются и преобразуются поля:
Исходное поле	              Целевое поле	        Примечание
ID	                        gid	                  Уникальный идентификатор
NAME	                      address	              Адрес (очищается от префиксов)
PROPERTY_SIDE_VALUE	        name	                Разделяется на отдельные стороны
PROPERTY_TYPE_VALUE	        construction_format	  Маппится по справочнику
PROPERTY_TYPE_VALUE	        display_type	        Маппится по справочнику
PROPERTY_LONGITUDE_VALUE	  lat	                  Внимание: в API перепутаны поля!
PROPERTY_LATITUDE_VALUE	    lon	                  Внимание: в API перепутаны поля!

3. Разделение сторон

Если конструкция имеет несколько сторон (например, "А,В"), создаётся отдельная запись для каждой стороны с одинаковым gid, но разным name.

4. Маппинг типов

construction_format:

    Билборд → Билборды

    Арка → Арки

    Путепровод → Мосты

    Брандмауэр → Брандмауэры

    Ситиборд → Ситиборды

    Остальное → Нетиповые форматы

display_type:

    Призматрон, Призмавижн → Призматрон

    Скролл → Скроллер

    LED, Светодиодный экран → Видеоэкран

    Остальное → Статика

5. Формат результата
```json

{
  "construction_sides": [
    {
      "gid": "10118",
      "address": "г.Молодечно, угол ул.Виленская - ул.Толстого (Центральная площадь)",
      "name": "В",
      "lon": 26.839621,
      "lat": 54.307023,
      "construction_format": "Билборды",
      "display_type": "Статика",
      "lighting": null,
      "size": null,
      "material": null
    }
  ]
}
```
Важные замечания
🚨 Ошибка в API boards.by

В ответе API перепутаны названия полей координат:

    PROPERTY_LONGITUDE_VALUE содержит широту (lat)

    PROPERTY_LATITUDE_VALUE содержит долготу (lon)

Парсер учитывает эту особенность и меняет поля местами.

📏 Размеры конструкций

Поле size заполняется только если размер найден в названии (NAME). В API размер отсутствует, для точных данных требуется парсинг страницы карточки.

💡 Освещение и материал

Поля lighting и material всегда null, так как отсутствуют в исходных данных.
Зависимости

    requests — HTTP-запросы к API

    bs4 (BeautifulSoup) — для возможного парсинга HTML (опционально)

    pandas — сохранение в Excel

    openpyxl — движок для записи Excel-файлов