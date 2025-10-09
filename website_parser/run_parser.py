#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простой скрипт для быстрого запуска парсера
"""

import sys
import os
from website_parser import WebsiteParser
from colorama import Fore, Style, init

# Инициализация colorama
init()

def quick_parse():
    """Быстрый парсинг одной страницы"""
    print(f"{Fore.CYAN}🕷️  Быстрый парсер веб-страниц{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Для выхода нажмите Ctrl+C{Style.RESET_ALL}")
    print()
    
    try:
        # Получаем URL от пользователя
        url = input(f"{Fore.GREEN}Введите URL для парсинга: {Style.RESET_ALL}").strip()
        
        if not url:
            print(f"{Fore.RED}URL не может быть пустым{Style.RESET_ALL}")
            return
        
        # Добавляем http:// если не указан протокол
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        print(f"\n{Fore.YELLOW}Анализ страницы...{Style.RESET_ALL}")
        
        # Создаем парсер
        parser = WebsiteParser()
        
        # Получаем базовую информацию
        page_info = parser.get_page_info(url)
        
        if not page_info:
            print(f"{Fore.RED}Не удалось получить страницу. Проверьте URL и подключение к интернету.{Style.RESET_ALL}")
            return
        
        # Показываем информацию о странице
        print(f"\n{Fore.CYAN}📄 Информация о странице:{Style.RESET_ALL}")
        print(f"Заголовок: {page_info.get('title', 'Не найден')}")
        print(f"Описание: {page_info.get('description', 'Не найдено')[:100]}...")
        print(f"H1 заголовков: {page_info.get('h1_count', 0)}")
        print(f"H2 заголовков: {page_info.get('h2_count', 0)}")
        print(f"Ссылок: {page_info.get('link_count', 0)}")
        print(f"Изображений: {page_info.get('image_count', 0)}")
        
        # Предлагаем варианты парсинга
        print(f"\n{Fore.CYAN}📊 Выберите тип данных для извлечения:{Style.RESET_ALL}")
        print("1. Основная информация (заголовки, параграфы)")
        print("2. Новостная статья (заголовок, контент, автор, дата)")
        print("3. Товар в магазине (название, цена, описание)")
        print("4. Пользовательские селекторы")
        
        choice = input(f"\n{Fore.GREEN}Ваш выбор (1-4): {Style.RESET_ALL}").strip()
        
        # Определяем селекторы на основе выбора
        selectors = {}
        filename = "parsed_data.csv"
        
        if choice == "1":
            selectors = {
                'title': 'title',
                'h1': 'h1',
                'h2': 'h2',
                'paragraphs': 'p',
                'meta_description': 'meta[name="description"]'
            }
            filename = "basic_info.csv"
            
        elif choice == "2":
            selectors = {
                'title': 'h1, .title, .headline, .article-title',
                'content': '.content, .article-body, .post-content, .entry-content, p',
                'author': '.author, .byline, .writer, .post-author',
                'date': '.date, .published, .timestamp, time, .post-date',
                'tags': '.tags a, .categories a, .tag'
            }
            filename = "news_article.csv"
            
        elif choice == "3":
            selectors = {
                'name': 'h1, .product-title, .item-name, .product-name',
                'price': '.price, .cost, .amount, .product-price',
                'description': '.description, .product-desc, .details, .product-description',
                'rating': '.rating, .stars, .score, .product-rating',
                'availability': '.stock, .availability, .in-stock'
            }
            filename = "product_info.csv"
            
        elif choice == "4":
            print(f"\n{Fore.YELLOW}Введите CSS селекторы (Enter для пропуска):{Style.RESET_ALL}")
            
            selector_fields = [
                ("title", "Заголовок"),
                ("content", "Основной контент"),
                ("author", "Автор"),
                ("date", "Дата"),
                ("price", "Цена"),
                ("description", "Описание")
            ]
            
            for field, description in selector_fields:
                selector = input(f"{description} (CSS селектор): ").strip()
                if selector:
                    selectors[field] = selector
            
            filename = "custom_data.csv"
            
        else:
            print(f"{Fore.RED}Неверный выбор{Style.RESET_ALL}")
            return
        
        if not selectors:
            print(f"{Fore.YELLOW}Селекторы не заданы{Style.RESET_ALL}")
            return
        
        # Парсим данные
        print(f"\n{Fore.YELLOW}🔍 Извлечение данных...{Style.RESET_ALL}")
        data = parser.parse_single_page(url, selectors)
        
        if data:
            # Сохраняем в CSV
            saved_file = parser.save_to_csv([data], filename)
            
            # Показываем результаты
            print(f"\n{Fore.GREEN}✅ Данные успешно извлечены и сохранены в {saved_file}{Style.RESET_ALL}")
            
            print(f"\n{Fore.CYAN}📋 Извлеченные данные:{Style.RESET_ALL}")
            for key, value in data.items():
                if key == 'url':
                    continue
                    
                if isinstance(value, list):
                    if value:
                        print(f"{key}: {len(value)} элементов")
                        print(f"  └─ Первый: {str(value[0])[:80]}...")
                    else:
                        print(f"{key}: Пустой список")
                elif value:
                    print(f"{key}: {str(value)[:80]}...")
                else:
                    print(f"{key}: Не найдено")
            
            print(f"\n{Fore.CYAN}💾 Файл сохранен: {os.path.abspath(saved_file)}{Style.RESET_ALL}")
            
        else:
            print(f"{Fore.RED}❌ Не удалось извлечь данные. Проверьте селекторы.{Style.RESET_ALL}")
            
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}👋 Работа прервана пользователем{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Ошибка: {e}{Style.RESET_ALL}")


def main():
    """Главная функция"""
    if len(sys.argv) > 1:
        # Если передан URL как аргумент
        url = sys.argv[1]
        print(f"{Fore.CYAN}Парсинг URL: {url}{Style.RESET_ALL}")
        
        parser = WebsiteParser()
        
        # Базовые селекторы
        selectors = {
            'title': 'title',
            'h1': 'h1',
            'paragraphs': 'p'
        }
        
        data = parser.parse_single_page(url, selectors)
        if data:
            filename = "quick_parse.csv"
            parser.save_to_csv([data], filename)
            print(f"{Fore.GREEN}Данные сохранены в {filename}{Style.RESET_ALL}")
    else:
        # Интерактивный режим
        quick_parse()


if __name__ == "__main__":
    main()