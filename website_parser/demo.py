#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Демонстрация возможностей веб-парсера
"""

from website_parser import WebsiteParser
from colorama import Fore, Style, init
import time

# Инициализация colorama
init()

def demo_basic_parsing():
    """Демонстрация базового парсинга"""
    print(f"{Fore.CYAN}{'='*60}")
    print("🕷️  ДЕМОНСТРАЦИЯ ВЕБ-ПАРСЕРА")
    print(f"{'='*60}{Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}1. Создание экземпляра парсера...{Style.RESET_ALL}")
    parser = WebsiteParser()
    print(f"{Fore.GREEN}✅ Парсер создан успешно{Style.RESET_ALL}")
    
    # Тестовый URL
    test_url = "https://httpbin.org/html"
    
    print(f"\n{Fore.YELLOW}2. Получение информации о странице...{Style.RESET_ALL}")
    print(f"URL: {test_url}")
    
    page_info = parser.get_page_info(test_url)
    
    if page_info:
        print(f"{Fore.GREEN}✅ Страница успешно проанализирована:{Style.RESET_ALL}")
        print(f"   📄 Заголовок: {page_info.get('title', 'Не найден')}")
        print(f"   📝 H1 заголовков: {page_info.get('h1_count', 0)}")
        print(f"   📝 H2 заголовков: {page_info.get('h2_count', 0)}")
        print(f"   🔗 Ссылок: {page_info.get('link_count', 0)}")
        print(f"   🖼️  Изображений: {page_info.get('image_count', 0)}")
    else:
        print(f"{Fore.RED}❌ Не удалось получить информацию о странице{Style.RESET_ALL}")
        return
    
    time.sleep(1)
    
    print(f"\n{Fore.YELLOW}3. Извлечение контента с помощью селекторов...{Style.RESET_ALL}")
    
    # Определяем селекторы
    selectors = {
        'title': 'title',
        'main_heading': 'h1',
        'content': 'p',
        'meta_description': 'meta[name="description"]'
    }
    
    print("Используемые селекторы:")
    for key, selector in selectors.items():
        print(f"   {key}: {selector}")
    
    # Парсим данные
    data = parser.parse_single_page(test_url, selectors)
    
    if data:
        print(f"\n{Fore.GREEN}✅ Данные успешно извлечены:{Style.RESET_ALL}")
        
        for key, value in data.items():
            if key == 'url':
                continue
                
            if isinstance(value, list):
                if value:
                    print(f"   {key}: {len(value)} элементов")
                    print(f"      └─ Первый: {str(value[0])[:50]}...")
                else:
                    print(f"   {key}: Пустой список")
            elif value:
                print(f"   {key}: {str(value)[:50]}...")
            else:
                print(f"   {key}: Не найдено")
    
    time.sleep(1)
    
    print(f"\n{Fore.YELLOW}4. Сохранение данных в CSV...{Style.RESET_ALL}")
    
    if data:
        filename = "demo_output.csv"
        saved_file = parser.save_to_csv([data], filename)
        print(f"{Fore.GREEN}✅ Данные сохранены в файл: {saved_file}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}❌ Нет данных для сохранения{Style.RESET_ALL}")

def demo_multiple_pages():
    """Демонстрация парсинга нескольких страниц"""
    print(f"\n{Fore.CYAN}{'='*60}")
    print("📊 ДЕМОНСТРАЦИЯ МАССОВОГО ПАРСИНГА")
    print(f"{'='*60}{Style.RESET_ALL}")
    
    parser = WebsiteParser()
    
    # Список тестовых URL
    urls = [
        "https://httpbin.org/html",
        "https://example.com"
    ]
    
    print(f"\n{Fore.YELLOW}Парсинг {len(urls)} страниц...{Style.RESET_ALL}")
    
    # Базовые селекторы
    selectors = {
        'title': 'title',
        'h1': 'h1',
        'description': 'meta[name="description"]'
    }
    
    # Парсим все страницы
    all_data = parser.parse_multiple_pages(urls, selectors)
    
    if all_data:
        print(f"\n{Fore.GREEN}✅ Обработано {len(all_data)} из {len(urls)} страниц{Style.RESET_ALL}")
        
        # Сохраняем данные
        filename = "demo_multiple.csv"
        parser.save_to_csv(all_data, filename)
        print(f"{Fore.GREEN}✅ Данные сохранены в {filename}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}❌ Не удалось извлечь данные{Style.RESET_ALL}")

def demo_custom_selectors():
    """Демонстрация пользовательских селекторов"""
    print(f"\n{Fore.CYAN}{'='*60}")
    print("🎯 ДЕМОНСТРАЦИЯ ПОЛЬЗОВАТЕЛЬСКИХ СЕЛЕКТОРОВ")
    print(f"{'='*60}{Style.RESET_ALL}")
    
    parser = WebsiteParser()
    
    # Примеры селекторов для разных типов сайтов
    selector_examples = {
        "Новостной сайт": {
            'title': 'h1, .title, .headline',
            'content': '.content, .article-body, p',
            'author': '.author, .byline',
            'date': '.date, .published, time'
        },
        "Интернет-магазин": {
            'name': 'h1, .product-title',
            'price': '.price, .cost',
            'description': '.description, .product-desc',
            'rating': '.rating, .stars'
        },
        "Блог": {
            'title': 'h1, .post-title',
            'content': '.post-content, .entry-content',
            'author': '.author, .post-author',
            'tags': '.tags a, .categories a'
        }
    }
    
    print(f"\n{Fore.YELLOW}Примеры селекторов для разных типов сайтов:{Style.RESET_ALL}")
    
    for site_type, selectors in selector_examples.items():
        print(f"\n{Fore.CYAN}📋 {site_type}:{Style.RESET_ALL}")
        for field, selector in selectors.items():
            print(f"   {field}: {selector}")

def main():
    """Главная функция демонстрации"""
    try:
        # Базовая демонстрация
        demo_basic_parsing()
        
        # Демонстрация массового парсинга
        demo_multiple_pages()
        
        # Демонстрация селекторов
        demo_custom_selectors()
        
        print(f"\n{Fore.MAGENTA}{'='*60}")
        print("🎉 ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
        print(f"{'='*60}{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}📚 Для дальнейшего изучения:{Style.RESET_ALL}")
        print("   • Запустите examples.py для интерактивных примеров")
        print("   • Запустите run_parser.py для быстрого парсинга")
        print("   • Изучите README.md для подробной документации")
        print("   • Настройте config.json под свои нужды")
        
        print(f"\n{Fore.GREEN}✨ Удачного парсинга! ✨{Style.RESET_ALL}")
        
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}👋 Демонстрация прервана пользователем{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Ошибка во время демонстрации: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()