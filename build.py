import requests
import csv
import os
import re
import html
from config import SHEET_CSV_URL, get_drive_id


def make_cat_id(name: str) -> str:
    """Генерирует стабильный slug-based ID для категории (без hash-рандомизации)."""
    slug = re.sub(r'[^\w]', '-', name.lower().strip())
    slug = re.sub(r'-+', '-', slug).strip('-')
    return f"cat-{slug}"


def build():
    try:
        response = requests.get(SHEET_CSV_URL, timeout=30)
        response.encoding = 'utf-8'
        # Используем первый ряд (хедер), очищая каждое название от пробелов и невидимых символов BOM (Byte Order Mark)
        reader = csv.DictReader(response.text.splitlines())
        reader.fieldnames = [field.strip().replace('\ufeff', '') for field in reader.fieldnames]
        items = list(reader)
    except Exception as e:
        print(f"Ошибка при загрузке таблицы: {e}")
        return

    # Группируем по категориям
    categories: dict[str, list] = {}
    for item in items:
        if not item.get('name'):  # если имени нет (вероятно пустая строка в конце списка), пропускаем строку
            continue
        cat = item.get('category', 'Разное')
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(item)

    nav_html = ""
    sections_food_html = ""
    sections_bar_html = ""

    for cat_name, cat_items in categories.items():
        # Определяем вкладку по первому товару в категории
        raw_tab = cat_items[0].get('tab', 'Кухня').strip().lower()
        is_bar = (raw_tab == 'бар')

        cat_id = make_cat_id(cat_name)
        tab_key = "bar" if is_bar else "food"
        display_style = 'style="display: none;"' if is_bar else 'style="display: inline-block;"'

        nav_html += f'<a href="#{cat_id}" class="nav-item" data-tab="{tab_key}" {display_style}>{cat_name}</a>'

        section_html = f'<h2 id="{cat_id}" class="category-title">{cat_name}</h2>\n<div class="menu-grid">'

        for item in cat_items:
            price_val = item.get('price', '').strip()
            price_html = f'<div class="product-price">{price_val} ₽</div>' if price_val else ''

            img_url = item.get('img', '').strip()
            img_id = get_drive_id(img_url)

            data_name   = html.escape(item.get('name', ''),               quote=True)
            data_price  = html.escape(price_val,                           quote=True)
            data_weight = html.escape(item.get('weight', '').strip(),      quote=True)
            data_desc   = html.escape(item.get('desc', '').strip(),        quote=True)

            if img_id:
                t_path = f"assets/img/thumbs/{img_id}.webp"
                f_path = f"assets/img/full/{img_id}.webp"
                img_tag    = f'<img src="{t_path}" class="product-img" loading="lazy">'
                card_class = "product-card"
            else:
                t_path = ""
                f_path = ""
                img_tag    = ""
                card_class = "product-card no-image"

            section_html += f'''
            <div class="{card_class}" onclick="openModal(this)"
                 data-name="{data_name}" data-price="{data_price}"
                 data-weight="{data_weight}" data-desc="{data_desc}"
                 data-img-thumb="{t_path}" data-img-full="{f_path}">
                {img_tag}
                <div class="product-info">
                    <div class="product-title">{item['name']}</div>
                    {price_html}
                </div>
            </div>'''

        section_html += '</div>\n'

        if is_bar:
            sections_bar_html += section_html
        else:
            sections_food_html += section_html

    # Запись в шаблон
    if not os.path.exists('template.html'):
        print("Ошибка: template.html не найден")
        return

    with open('template.html', 'r', encoding='utf-8') as f:
        template = f.read()

    final_html = template.replace('{nav_items}', nav_html)
    final_html = final_html.replace('{sections_food}', sections_food_html)
    final_html = final_html.replace('{sections_bar}', sections_bar_html)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(final_html)


if __name__ == "__main__":
    build()
