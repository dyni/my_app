#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Примеры использования веб-парсера
"""

from website_parser import WebsiteParser
import json
import os
from colorama import Fore, Style


def example_parse_news_site():
    """Пример парсинга новостного сайта"""
    print(f"{Fore.CYAN}=== Пример парсинга новостного сайта ==={Style.RESET_ALL}")
    
    parser = WebsiteParser()
    
    # Селекторы для новостного сайта
    news_selectors = {
        'title': 'h1, .title, .headline',
        'content': '.content, .article-body, p',
        'author': '.author, .byline',
        'date': '.date, .published, time'
    }
    
    # Пример URL (можно заменить на реальный)
    urls = [
        "https://httpbin.org/html",  # Тестовый URL
        # Добавьте реальные URL новостей здесь
    ]
    
    try:
        data = parser.parse_multiple_pages(urls, news_selectors)
        if data:
            filename = "news_data.csv"
            parser.save_to_csv(data, filename)
            print(f"{Fore.GREEN}Новостные данные сохранены в {filename}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}Нет данных для сохранения{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Ошибка: {e}{Style.RESET_ALL}")


def example_parse_product_catalog():
    """Пример парсинга каталога товаров"""
    print(f"{Fore.CYAN}=== Пример парсинга каталога товаров ==={Style.RESET_ALL}")
    
    parser = WebsiteParser()
    
    # Селекторы для товаров
    product_selectors = {
        'name': 'h1, .product-title, .item-name',
        'price': '.price, .cost, .amount',
        'description': '.description, .product-desc',
        'rating': '.rating, .stars',
        'availability': '.stock, .availability'
    }
    
    # Пример URL каталога
    catalog_url = "https://httpbin.org/html"
    
    try:
        # Сначала получаем страницу каталога
        soup = parser.fetch_page(catalog_url)
        if soup:
            # Извлекаем ссылки на товары (пример селектора)
            product_links = parser.extract_links(soup, catalog_url, ".product-link a")
            
            if product_links:
                print(f"Найдено {len(product_links)} товаров")
                data = parser.parse_multiple_pages(product_links, product_selectors)
                
                if data:
                    filename = "products_data.csv"
                    parser.save_to_csv(data, filename)
                    print(f"{Fore.GREEN}Данные о товарах сохранены в {filename}{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}Ссылки на товары не найдены{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Ошибка: {e}{Style.RESET_ALL}")


def example_custom_parsing():
    """Пример пользовательского парсинга"""
    print(f"{Fore.CYAN}=== Пример пользовательского парсинга ==={Style.RESET_ALL}")
    
    # URL для парсинга
    url = input("Введите URL для парсинга: ").strip()
    if not url:
        url = "https://httpbin.org/html"  # URL по умолчанию
    
    parser = WebsiteParser()
    
    # Получаем базовую информацию о странице
    print(f"\n{Fore.YELLOW}Анализ страницы...{Style.RESET_ALL}")
    page_info = parser.get_page_info(url)
    
    if page_info:
        print(f"Заголовок: {page_info.get('title', 'Не найден')}")
        print(f"Описание: {page_info.get('description', 'Не найдено')}")
        print(f"Количество H1: {page_info.get('h1_count', 0)}")
        print(f"Количество H2: {page_info.get('h2_count', 0)}")
        print(f"Количество ссылок: {page_info.get('link_count', 0)}")
        print(f"Количество изображений: {page_info.get('image_count', 0)}")
    
    # Пользовательские селекторы
    print(f"\n{Fore.YELLOW}Настройка селекторов для извлечения данных:{Style.RESET_ALL}")
    print("Введите CSS селекторы (оставьте пустым для пропуска):")
    
    selectors = {}
    
    # Основные селекторы
    selector_options = [
        ("title", "Заголовок (например: h1, .title)"),
        ("content", "Контент (например: .content, p)"),
        ("author", "Автор (например: .author, .byline)"),
        ("date", "Дата (например: .date, time)"),
        ("price", "Цена (например: .price, .cost)"),
        ("description", "Описание (например: .description)")
    ]
    
    for key, description in selector_options:
        selector = input(f"{description}: ").strip()
        if selector:
            selectors[key] = selector
    
    if selectors:
        try:
            print(f"\n{Fore.YELLOW}Парсинг данных...{Style.RESET_ALL}")
            data = parser.parse_single_page(url, selectors)
            
            if data:
                filename = "custom_data.csv"
                parser.save_to_csv([data], filename)
                print(f"{Fore.GREEN}Данные сохранены в {filename}{Style.RESET_ALL}")
                
                # Показываем извлеченные данные
                print(f"\n{Fore.CYAN}Извлеченные данные:{Style.RESET_ALL}")
                for key, value in data.items():
                    if isinstance(value, list):
                        print(f"{key}: {len(value)} элементов")
                        if value:
                            print(f"  Первый: {value[0][:100]}...")
                    else:
                        print(f"{key}: {str(value)[:100]}...")
            else:
                print(f"{Fore.RED}Не удалось извлечь данные{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Ошибка при парсинге: {e}{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}Селекторы не заданы{Style.RESET_ALL}")


def example_batch_parsing():
    """Пример массового парсинга из списка URL"""
    print(f"{Fore.CYAN}=== Пример массового парсинга ==={Style.RESET_ALL}")
    
    # Создаем файл со списком URL, если его нет
    urls_file = "urls.txt"
    if not os.path.exists(urls_file):
        sample_urls = [
            "https://httpbin.org/html",
            "https://httpbin.org/json",
            # Добавьте свои URL здесь
        ]
        
        with open(urls_file, 'w', encoding='utf-8') as f:
            for url in sample_urls:
                f.write(f"{url}\n")
        
        print(f"Создан файл {urls_file} с примерами URL")
    
    # Читаем URL из файла
    try:
        with open(urls_file, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]
        
        if not urls:
            print(f"{Fore.YELLOW}Файл {urls_file} пуст{Style.RESET_ALL}")
            return
        
        print(f"Загружено {len(urls)} URL из {urls_file}")
        
        parser = WebsiteParser()
        
        # Используем базовые селекторы
        selectors = {
            'title': 'title',
            'h1': 'h1',
            'meta_description': 'meta[name="description"]'
        }
        
        # Парсим все URL
        data = parser.parse_multiple_pages(urls, selectors)
        
        if data:
            filename = "batch_data.csv"
            parser.save_to_csv(data, filename)
            print(f"{Fore.GREEN}Данные массового парсинга сохранены в {filename}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}Нет данных для сохранения{Style.RESET_ALL}")
            
    except Exception as e:
        print(f"{Fore.RED}Ошибка при массовом парсинге: {e}{Style.RESET_ALL}")


def main():
    """Главная функция с меню примеров"""
    print(f"{Fore.MAGENTA}{'='*50}")
    print("    ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ ВЕБ-ПАРСЕРА")
    print(f"{'='*50}{Style.RESET_ALL}")
    
    examples = [
        ("1", "Парсинг новостного сайта", example_parse_news_site),
        ("2", "Парсинг каталога товаров", example_parse_product_catalog),
        ("3", "Пользовательский парсинг", example_custom_parsing),
        ("4", "Массовый парсинг из файла", example_batch_parsing),
        ("0", "Выход", None)
    ]
    
    while True:
        print(f"\n{Fore.CYAN}Выберите пример:{Style.RESET_ALL}")
        for num, desc, _ in examples:
            print(f"  {num}. {desc}")
        
        choice = input(f"\n{Fore.YELLOW}Ваш выбор: {Style.RESET_ALL}").strip()
        
        if choice == "0":
            print(f"{Fore.GREEN}До свидания!{Style.RESET_ALL}")
            break
        
        # Найти и выполнить выбранный пример
        example_func = None
        for num, desc, func in examples:
            if num == choice:
                example_func = func
                break
        
        if example_func:
            print(f"\n{'-'*50}")
            try:
                example_func()
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Прервано пользователем{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}Ошибка: {e}{Style.RESET_ALL}")
            print(f"{'-'*50}")
        else:
            print(f"{Fore.RED}Неверный выбор. Попробуйте снова.{Style.RESET_ALL}")


if __name__ == "__main__":
    main()