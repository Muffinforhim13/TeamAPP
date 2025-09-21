#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TeammatesFinder - Финальная версия запуска
Использует установленную команду lt
"""

import subprocess
import sys
import os
import time
import signal
import re
import threading

class FinalLauncher:
    def __init__(self):
        self.backend_process = None
        self.tunnel_process = None
        self.bot_process = None
        self.tunnel_url = None
        self.is_running = False
        
    def start_backend(self):
        """Запуск Backend"""
        print("🚀 Запускаем Backend...")
        
        try:
            self.backend_process = subprocess.Popen([
                sys.executable, 'backend/app.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            time.sleep(3)
            
            if self.backend_process.poll() is None:
                print("✅ Backend запущен на http://localhost:5000")
                return True
            else:
                stdout, stderr = self.backend_process.communicate()
                print(f"❌ Ошибка Backend: {stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка Backend: {e}")
            return False
            
    def start_tunnel(self):
        """Запуск LocalTunnel"""
        print("🌐 Запускаем LocalTunnel...")
        
        try:
            # Используем команду lt которая у тебя работает
            self.tunnel_process = subprocess.Popen([
                'lt', '--port', '5000'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            print("⏳ Ожидаем URL туннеля...")
            
            # Читаем вывод туннеля
            def read_tunnel_output():
                while True:
                    line = self.tunnel_process.stdout.readline()
                    if line:
                        line = line.strip()
                        print(f"📝 Tunnel: {line}")
                        
                        # Ищем URL в разных форматах
                        url_patterns = [
                            r'https://[^\s]+\.loca\.lt',
                            r'your url is: (https://[^\s]+)',
                            r'https://[a-zA-Z0-9-]+\.loca\.lt'
                        ]
                        
                        for pattern in url_patterns:
                            match = re.search(pattern, line)
                            if match:
                                if 'your url is:' in line:
                                    self.tunnel_url = match.group(1)
                                else:
                                    self.tunnel_url = match.group(0)
                                print(f"✅ Туннель готов: {self.tunnel_url}")
                                return
                                
                    if self.tunnel_process.poll() is not None:
                        stderr = self.tunnel_process.stderr.read()
                        if stderr:
                            print(f"❌ Ошибка туннеля: {stderr}")
                        return
            
            # Запускаем чтение в отдельном потоке
            tunnel_thread = threading.Thread(target=read_tunnel_output, daemon=True)
            tunnel_thread.start()
            
            # Ждем URL максимум 20 секунд
            start_time = time.time()
            while time.time() - start_time < 20:
                if self.tunnel_url:
                    return True
                time.sleep(0.5)
            
            print("❌ Не удалось получить URL туннеля за 20 секунд")
            return False
            
        except Exception as e:
            print(f"❌ Ошибка туннеля: {e}")
            return False
            
    def update_env(self):
        """Обновить .env файл"""
        if not self.tunnel_url:
            return False
            
        try:
            env_lines = []
            if os.path.exists('.env'):
                with open('.env', 'r', encoding='utf-8') as f:
                    env_lines = f.readlines()
            
            # Обновляем WEBAPP_URL
            updated = False
            for i, line in enumerate(env_lines):
                if line.startswith('WEBAPP_URL='):
                    env_lines[i] = f'WEBAPP_URL={self.tunnel_url}\n'
                    updated = True
                    break
            
            if not updated:
                env_lines.append(f'WEBAPP_URL={self.tunnel_url}\n')
            
            with open('.env', 'w', encoding='utf-8') as f:
                f.writelines(env_lines)
            
            print(f"✅ .env обновлен: WEBAPP_URL={self.tunnel_url}")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка обновления .env: {e}")
            return False
            
    def start_bot(self):
        """Запуск бота"""
        print("🤖 Запускаем бота...")
        
        try:
            self.bot_process = subprocess.Popen([
                sys.executable, 'bot/basic_bot.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            time.sleep(2)
            
            if self.bot_process.poll() is None:
                print("✅ Бот запущен!")
                return True
            else:
                stdout, stderr = self.bot_process.communicate()
                print(f"❌ Ошибка бота: {stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка бота: {e}")
            return False
            
    def show_instructions(self):
        """Показать инструкции"""
        print(f"""
🎉 ВСЕ СЕРВИСЫ ЗАПУЩЕНЫ!

📋 ИНСТРУКЦИИ ПО НАСТРОЙКЕ MINI APP:

1️⃣ Скопируй URL туннеля:
   {self.tunnel_url}

2️⃣ Иди к @BotFather в Telegram

3️⃣ Отправь команду:
   /setmenubutton

4️⃣ Выбери своего бота из списка

5️⃣ Введи название кнопки:
   TeammatesFinder

6️⃣ Введи URL:
   {self.tunnel_url}

7️⃣ Найди своего бота в Telegram

8️⃣ Отправь команду:
   /start

9️⃣ Внизу экрана появится кнопка "TeammatesFinder"

🔟 Нажми на кнопку - Mini App откроется!

🌐 Локальный доступ: http://localhost:5000
🌍 Публичный URL: {self.tunnel_url}
🤖 Telegram Bot: Работает

⚠️  ВАЖНО: НЕ ЗАКРЫВАЙ это окно - все сервисы остановятся!

Для остановки нажми Ctrl+C
""")
            
    def stop_all(self):
        """Остановка всех процессов"""
        print("\n⏹️  Останавливаем сервисы...")
        
        processes = [
            (self.backend_process, "Backend"),
            (self.tunnel_process, "LocalTunnel"), 
            (self.bot_process, "Bot")
        ]
        
        for process, name in processes:
            if process:
                try:
                    process.terminate()
                    process.wait(timeout=3)
                    print(f"✅ {name} остановлен")
                except:
                    try:
                        process.kill()
                        print(f"🔨 {name} принудительно остановлен")
                    except:
                        pass
                    
    def signal_handler(self, signum, frame):
        """Обработчик Ctrl+C"""
        self.stop_all()
        sys.exit(0)
        
    def run(self):
        """Запуск всего"""
        print("""
🎮 TeammatesFinder - Финальный запуск
====================================
Backend + LocalTunnel + Telegram Bot
====================================
""")
        
        signal.signal(signal.SIGINT, self.signal_handler)
        
        # Проверяем .env
        if not os.path.exists('.env'):
            print("❌ Файл .env не найден!")
            print("💡 Создайте файл .env с BOT_TOKEN")
            return False
        
        print("🔍 Запускаем все компоненты...")
        
        # 1. Запускаем Backend
        if not self.start_backend():
            return False
            
        # 2. Запускаем туннель
        if not self.start_tunnel():
            print("❌ Не удалось запустить туннель")
            self.stop_all()
            return False
            
        # 3. Обновляем .env
        if not self.update_env():
            print("⚠️  Не удалось обновить .env, но продолжаем...")
            
        # 4. Запускаем бота
        if not self.start_bot():
            print("❌ Не удалось запустить бота")
            self.stop_all()
            return False
            
        # 5. Показываем инструкции
        self.show_instructions()
        
        self.is_running = True
        
        # Ждем команд пользователя
        try:
            while self.is_running:
                try:
                    user_input = input("\nНажми Enter для показа статуса или Ctrl+C для остановки: ")
                    if user_input.lower() in ['статус', 'status', 's']:
                        self.show_instructions()
                except EOFError:
                    break
                except KeyboardInterrupt:
                    break
                    
        except KeyboardInterrupt:
            pass
            
        self.stop_all()
        print("\n👋 TeammatesFinder остановлен!")
        print("Увидимся в следующий раз! 🎮")
        return True

def main():
    launcher = FinalLauncher()
    launcher.run()

if __name__ == '__main__':
    main()
