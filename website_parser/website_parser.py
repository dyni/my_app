#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Веб-парсер для извлечения контента с сайтов и сохранения в CSV формат
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import json
import logging
import time
import os
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Optional, Any
import colorama
from colorama import Fore, Style

# Инициализация colorama для цветного вывода
colorama.init()

class WebsiteParser:
    """Класс для парсинга веб-сайтов и сохранения данных в CSV"""
    
    def __init__(self, config_file: str = "config.json"):
        """
        Инициализация парсера
        
        Args:
            config_file (str): Путь к файлу конфигурации
        """
        self.config = self._load_config(config_file)
        self.session = requests.Session()
        self.setup_logging()
        self.setup_session()
        
    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """Загрузка конфигурации из файла"""
        default_config = {
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            },
            "timeout": 10,
            "delay": 1,
            "max_retries": 3,
            "output_file": "parsed_data.csv",
            "log_level": "INFO"
        }
        
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception as e:
                print(f"{Fore.YELLOW}Предупреждение: Не удалось загрузить конфигурацию: {e}{Style.RESET_ALL}")
        
        return default_config
    
    def setup_logging(self):
        """Настройка логирования"""
        log_level = getattr(logging, self.config.get("log_level", "INFO"))
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('parser.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_session(self):
        """Настройка HTTP сессии"""
        self.session.headers.update(self.config.get("headers", {}))
        
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Получение и парсинг HTML страницы
        
        Args:
            url (str): URL страницы для парсинга
            
        Returns:
            Optional[BeautifulSoup]: Объект BeautifulSoup или None при ошибке
        """
        retries = 0
        max_retries = self.config.get("max_retries", 3)
        
        while retries < max_retries:
            try:
                self.logger.info(f"Получение страницы: {url}")
                response = self.session.get(
                    url, 
                    timeout=self.config.get("timeout", 10)
                )
                response.raise_for_status()
                
                # Определение кодировки
                if response.encoding == 'ISO-8859-1':
                    response.encoding = response.apparent_encoding
                
                soup = BeautifulSoup(response.content, 'html.parser')
                self.logger.info(f"Страница успешно получена: {url}")
                return soup
                
            except requests.exceptions.RequestException as e:
                retries += 1
                self.logger.warning(f"Ошибка при получении {url} (попытка {retries}/{max_retries}): {e}")
                if retries < max_retries:
                    time.sleep(self.config.get("delay", 1) * retries)
                else:
                    self.logger.error(f"Не удалось получить страницу после {max_retries} попыток: {url}")
        
        return None
    
    def extract_data(self, soup: BeautifulSoup, selectors: Dict[str, str]) -> Dict[str, Any]:
        """
        Извлечение данных из HTML по CSS селекторам
        
        Args:
            soup (BeautifulSoup): Объект BeautifulSoup
            selectors (Dict[str, str]): Словарь с CSS селекторами
            
        Returns:
            Dict[str, Any]: Извлеченные данные
        """
        data = {}
        
        for field_name, selector in selectors.items():
            try:
                elements = soup.select(selector)
                
                if len(elements) == 1:
                    # Один элемент - возвращаем текст
                    data[field_name] = elements[0].get_text(strip=True)
                elif len(elements) > 1:
                    # Несколько элементов - возвращаем список
                    data[field_name] = [elem.get_text(strip=True) for elem in elements]
                else:
                    # Элемент не найден
                    data[field_name] = None
                    
            except Exception as e:
                self.logger.warning(f"Ошибка при извлечении данных для селектора '{selector}': {e}")
                data[field_name] = None
        
        return data
    
    def extract_links(self, soup: BeautifulSoup, base_url: str, link_selector: str = "a") -> List[str]:
        """
        Извлечение ссылок со страницы
        
        Args:
            soup (BeautifulSoup): Объект BeautifulSoup
            base_url (str): Базовый URL для относительных ссылок
            link_selector (str): CSS селектор для ссылок
            
        Returns:
            List[str]: Список абсолютных URL
        """
        links = []
        
        try:
            link_elements = soup.select(link_selector)
            
            for link in link_elements:
                href = link.get('href')
                if href:
                    absolute_url = urljoin(base_url, href)
                    links.append(absolute_url)
                    
        except Exception as e:
            self.logger.warning(f"Ошибка при извлечении ссылок: {e}")
        
        return links
    
    def parse_single_page(self, url: str, selectors: Dict[str, str]) -> Optional[Dict[str, Any]]:
        """
        Парсинг одной страницы
        
        Args:
            url (str): URL страницы
            selectors (Dict[str, str]): CSS селекторы для извлечения данных
            
        Returns:
            Optional[Dict[str, Any]]: Извлеченные данные или None
        """
        soup = self.fetch_page(url)
        if not soup:
            return None
        
        data = self.extract_data(soup, selectors)
        data['url'] = url  # Добавляем URL в данные
        
        return data
    
    def parse_multiple_pages(self, urls: List[str], selectors: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Парсинг нескольких страниц
        
        Args:
            urls (List[str]): Список URL для парсинга
            selectors (Dict[str, str]): CSS селекторы для извлечения данных
            
        Returns:
            List[Dict[str, Any]]: Список извлеченных данных
        """
        all_data = []
        total_urls = len(urls)
        
        print(f"{Fore.CYAN}Начинаю парсинг {total_urls} страниц...{Style.RESET_ALL}")
        
        for i, url in enumerate(urls, 1):
            print(f"{Fore.BLUE}Обрабатываю {i}/{total_urls}: {url}{Style.RESET_ALL}")
            
            data = self.parse_single_page(url, selectors)
            if data:
                all_data.append(data)
                print(f"{Fore.GREEN}✓ Успешно обработано{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}✗ Ошибка при обработке{Style.RESET_ALL}")
            
            # Задержка между запросами
            if i < total_urls:
                time.sleep(self.config.get("delay", 1))
        
        print(f"{Fore.CYAN}Парсинг завершен. Обработано {len(all_data)} из {total_urls} страниц.{Style.RESET_ALL}")
        return all_data
    
    def save_to_csv(self, data: List[Dict[str, Any]], filename: Optional[str] = None) -> str:
        """
        Сохранение данных в CSV файл
        
        Args:
            data (List[Dict[str, Any]]): Данные для сохранения
            filename (Optional[str]): Имя файла (по умолчанию из конфига)
            
        Returns:
            str: Путь к сохраненному файлу
        """
        if not data:
            raise ValueError("Нет данных для сохранения")
        
        if filename is None:
            filename = self.config.get("output_file", "parsed_data.csv")
        
        try:
            # Создаем DataFrame из данных
            df = pd.DataFrame(data)
            
            # Сохраняем в CSV с правильной кодировкой
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            
            self.logger.info(f"Данные сохранены в файл: {filename}")
            print(f"{Fore.GREEN}✓ Данные успешно сохранены в {filename}{Style.RESET_ALL}")
            
            return filename
            
        except Exception as e:
            self.logger.error(f"Ошибка при сохранении данных: {e}")
            raise
    
    def get_page_info(self, url: str) -> Dict[str, Any]:
        """
        Получение базовой информации о странице
        
        Args:
            url (str): URL страницы
            
        Returns:
            Dict[str, Any]: Информация о странице
        """
        soup = self.fetch_page(url)
        if not soup:
            return {}
        
        info = {
            'url': url,
            'title': soup.title.string if soup.title else None,
            'description': None,
            'keywords': None,
            'h1_count': len(soup.find_all('h1')),
            'h2_count': len(soup.find_all('h2')),
            'link_count': len(soup.find_all('a')),
            'image_count': len(soup.find_all('img'))
        }
        
        # Мета-описание
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            info['description'] = meta_desc.get('content')
        
        # Ключевые слова
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        if meta_keywords:
            info['keywords'] = meta_keywords.get('content')
        
        return info


def main():
    """Пример использования парсера"""
    
    # Создаем экземпляр парсера
    parser = WebsiteParser()
    
    print(f"{Fore.CYAN}=== Веб-парсер для извлечения контента ==={Style.RESET_ALL}")
    print()
    
    # Пример 1: Парсинг одной страницы
    print(f"{Fore.YELLOW}Пример 1: Получение информации о странице{Style.RESET_ALL}")
    url = "https://httpbin.org/html"
    
    try:
        page_info = parser.get_page_info(url)
        if page_info:
            print(f"Заголовок: {page_info.get('title')}")
            print(f"Количество H1: {page_info.get('h1_count')}")
            print(f"Количество ссылок: {page_info.get('link_count')}")
    except Exception as e:
        print(f"{Fore.RED}Ошибка: {e}{Style.RESET_ALL}")
    
    print()
    
    # Пример 2: Парсинг с пользовательскими селекторами
    print(f"{Fore.YELLOW}Пример 2: Парсинг с пользовательскими селекторами{Style.RESET_ALL}")
    
    # Определяем селекторы для извлечения данных
    selectors = {
        'title': 'title',
        'heading': 'h1',
        'paragraphs': 'p'
    }
    
    try:
        data = parser.parse_single_page(url, selectors)
        if data:
            # Сохраняем в CSV
            csv_file = parser.save_to_csv([data], "example_output.csv")
            print(f"Данные сохранены в: {csv_file}")
    except Exception as e:
        print(f"{Fore.RED}Ошибка: {e}{Style.RESET_ALL}")


if __name__ == "__main__":
    main()