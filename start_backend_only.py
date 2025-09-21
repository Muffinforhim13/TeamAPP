#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Запуск только Backend для локального тестирования
"""

import subprocess
import sys
import os
import time
import signal

class BackendLauncher:
    def __init__(self):
        self.backend_process = None
        self.bot_process = None
        
    def start_backend(self):
        """Запуск Backend"""
        print("🚀 Запускаем Backend...")
        
        try:
            self.backend_process = subprocess.Popen([
                sys.executable, 'backend/app.py'
            ])
            
            time.sleep(2)
            print("✅ Backend запущен на http://localhost:5000")
            return True
                
        except Exception as e:
            print(f"❌ Ошибка Backend: {e}")
            return False
            
    def start_bot(self):
        """Запуск бота для локального тестирования"""
        print("🤖 Запускаем бота (локальная версия)...")
        
        # Обновляем .env для localhost
        try:
            env_lines = []
            if os.path.exists('.env'):
                with open('.env', 'r') as f:
                    env_lines = f.readlines()
            
            # Устанавливаем localhost URL
            updated = False
            for i, line in enumerate(env_lines):
                if line.startswith('WEBAPP_URL='):
                    env_lines[i] = 'WEBAPP_URL=http://localhost:5000\\n'
                    updated = True
                    break
            
            if not updated:
                env_lines.append('WEBAPP_URL=http://localhost:5000\\n')
            
            with open('.env', 'w') as f:
                f.writelines(env_lines)
                
        except Exception as e:
            print(f"⚠️  Не удалось обновить .env: {e}")
        
        try:
            self.bot_process = subprocess.Popen([
                sys.executable, 'bot/basic_bot.py'
            ])
            
            time.sleep(1)
            print("✅ Бот запущен!")
            return True
                
        except Exception as e:
            print(f"❌ Ошибка бота: {e}")
            return False
            
    def stop_all(self):
        """Остановка процессов"""
        print("\\n⏹️  Останавливаем сервисы...")
        
        if self.backend_process:
            self.backend_process.terminate()
            print("✅ Backend остановлен")
            
        if self.bot_process:
            self.bot_process.terminate()
            print("✅ Бот остановлен")
            
    def signal_handler(self, signum, frame):
        """Обработчик Ctrl+C"""
        self.stop_all()
        sys.exit(0)
        
    def run(self):
        """Запуск"""
        print("""
🎮 TeammatesFinder - Локальный запуск
====================================
Backend + Bot (без туннеля)
====================================
""")
        
        signal.signal(signal.SIGINT, self.signal_handler)
        
        if not os.path.exists('.env'):
            print("❌ Файл .env не найден!")
            return False
        
        # Запускаем Backend
        if not self.start_backend():
            return False
            
        # Запускаем бота
        if not self.start_bot():
            self.stop_all()
            return False
            
        print(f"""
🎉 СЕРВИСЫ ЗАПУЩЕНЫ!

🌐 Веб-приложение: http://localhost:5000
🤖 Telegram Bot: Работает (localhost режим)

📱 Тестирование:
1. Открой http://localhost:5000 в браузере
2. Протестируй создание профиля и свайпы
3. Бот работает, но Mini App нужен HTTPS

💡 Для полноценного Mini App используй GitHub Pages:
   python deploy_github.py

Для остановки нажми Ctrl+C
""")
        
        # Ждем
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
            
        self.stop_all()
        print("👋 Готово!")

def main():
    launcher = BackendLauncher()
    launcher.run()

if __name__ == '__main__':
    main()
