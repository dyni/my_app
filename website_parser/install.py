#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для автоматической установки зависимостей
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Установка зависимостей из requirements.txt"""
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ Файл requirements.txt не найден")
        return False
    
    try:
        print("📦 Установка зависимостей...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ])
        print("✅ Зависимости успешно установлены")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка при установке зависимостей: {e}")
        return False

def check_python_version():
    """Проверка версии Python"""
    if sys.version_info < (3, 7):
        print("❌ Требуется Python 3.7 или выше")
        print(f"Текущая версия: {sys.version}")
        return False
    
    print(f"✅ Python версия: {sys.version}")
    return True

def test_imports():
    """Тестирование импорта основных модулей"""
    modules = [
        "requests",
        "bs4",
        "pandas",
        "colorama"
    ]
    
    print("🧪 Тестирование импорта модулей...")
    
    for module in modules:
        try:
            __import__(module)
            print(f"  ✅ {module}")
        except ImportError:
            print(f"  ❌ {module} - не установлен")
            return False
    
    return True

def main():
    """Главная функция установки"""
    print("🕷️  Установка веб-парсера")
    print("=" * 40)
    
    # Проверка версии Python
    if not check_python_version():
        return
    
    # Установка зависимостей
    if not install_requirements():
        return
    
    # Тестирование импорта
    if not test_imports():
        print("\n❌ Некоторые модули не удалось импортировать")
        print("Попробуйте переустановить зависимости:")
        print("pip install -r requirements.txt")
        return
    
    print("\n🎉 Установка завершена успешно!")
    print("\nДля запуска парсера используйте:")
    print("  python website_parser.py")
    print("  python examples.py")
    print("  python run_parser.py")
    
    # Создание тестового конфига, если его нет
    config_file = Path(__file__).parent / "config.json"
    if not config_file.exists():
        print("\n📝 Создание файла конфигурации...")
        try:
            from website_parser import WebsiteParser
            parser = WebsiteParser()
            print("✅ Конфигурация создана")
        except Exception as e:
            print(f"⚠️  Предупреждение: {e}")

if __name__ == "__main__":
    main()