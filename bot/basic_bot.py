#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Базовый Telegram Bot для TeammatesFinder
Максимально простая версия без сложных зависимостей
"""

import os
import sys
import time
import requests
import json
from dotenv import load_dotenv

# Загружаем .env
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBAPP_URL = os.getenv('WEBAPP_URL', 'http://localhost:5000')

if not BOT_TOKEN or BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
    print("❌ Ошибка: BOT_TOKEN не найден в .env файле")
    sys.exit(1)

class SimpleTelegramBot:
    def __init__(self, token):
        self.token = token
        self.api_url = f"https://api.telegram.org/bot{token}"
        self.offset = 0
    
    def send_message(self, chat_id, text, reply_markup=None):
        """Отправка сообщения"""
        url = f"{self.api_url}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'HTML'
        }
        
        if reply_markup:
            data['reply_markup'] = json.dumps(reply_markup)
        
        try:
            response = requests.post(url, data=data)
            return response.json()
        except Exception as e:
            print(f"Ошибка отправки сообщения: {e}")
            return None
    
    def get_updates(self):
        """Получение обновлений"""
        url = f"{self.api_url}/getUpdates"
        data = {'offset': self.offset, 'timeout': 30}
        
        try:
            response = requests.post(url, data=data)
            return response.json()
        except Exception as e:
            print(f"Ошибка получения обновлений: {e}")
            return None
    
    def handle_message(self, message):
        """Обработка сообщения"""
        chat_id = message['chat']['id']
        text = message.get('text', '')
        user = message.get('from', {})
        first_name = user.get('first_name', 'Игрок')
        
        # Обработка команд
        if text == '/start':
            welcome_text = f"""
🎮 <b>Добро пожаловать в TeammatesFinder!</b>

Привет, {first_name}! 

Этот бот поможет тебе найти тиммейтов для игр!

🌐 <b>Веб-приложение:</b>
<a href="{WEBAPP_URL}">Открыть TeammatesFinder</a>

<b>Поддерживаемые игры:</b>
🔴 Dota 2
🔫 Counter-Strike 2  
⚡ Valorant
⚔️ Mobile Legends
⚡ League of Legends

<b>Команды:</b>
/start - это сообщение
/app - ссылка на приложение
/help - помощь
"""
            
            keyboard = {
                "inline_keyboard": [
                    [{"text": "🎮 Открыть TeammatesFinder", "url": WEBAPP_URL}]
                ]
            }
            
            self.send_message(chat_id, welcome_text, keyboard)
            
        elif text == '/app':
            app_text = f"""
🚀 <b>TeammatesFinder</b>

Открой веб-приложение для поиска тиммейтов:
<a href="{WEBAPP_URL}">Нажми здесь</a>

Или скопируй ссылку: {WEBAPP_URL}
"""
            
            keyboard = {
                "inline_keyboard": [
                    [{"text": "🎮 Открыть приложение", "url": WEBAPP_URL}]
                ]
            }
            
            self.send_message(chat_id, app_text, keyboard)
            
        elif text == '/help':
            help_text = f"""
❓ <b>Помощь по TeammatesFinder</b>

<b>Как пользоваться:</b>
1. Открой веб-приложение: <a href="{WEBAPP_URL}">TeammatesFinder</a>
2. Создай свой игровой профиль
3. Просматривай профили других игроков
4. Лайкай тех, с кем хочешь играть
5. При взаимном лайке получите контакты!

<b>Команды:</b>
/start - главное меню
/app - ссылка на приложение
/help - эта справка

<b>Веб-приложение:</b> {WEBAPP_URL}
"""
            
            keyboard = {
                "inline_keyboard": [
                    [{"text": "🎮 Открыть приложение", "url": WEBAPP_URL}]
                ]
            }
            
            self.send_message(chat_id, help_text, keyboard)
            
        else:
            # Неизвестная команда
            unknown_text = f"""
❓ Неизвестная команда: {text}

<b>Доступные команды:</b>
/start - главное меню
/app - открыть приложение
/help - справка

Или просто открой веб-приложение:
<a href="{WEBAPP_URL}">TeammatesFinder</a>
"""
            
            keyboard = {
                "inline_keyboard": [
                    [{"text": "🎮 Открыть TeammatesFinder", "url": WEBAPP_URL}]
                ]
            }
            
            self.send_message(chat_id, unknown_text, keyboard)
    
    def run(self):
        """Запуск бота"""
        print("=> TeammatesFinder Bot запускается...")
        print(f"=> Веб-приложение: {WEBAPP_URL}")
        print("=> Бот готов к работе!")
        print("=> Отправьте /start боту в Telegram")
        print("=> Для остановки нажмите Ctrl+C")
        
        try:
            while True:
                updates = self.get_updates()
                
                if updates and updates.get('ok'):
                    for update in updates['result']:
                        self.offset = update['update_id'] + 1
                        
                        if 'message' in update:
                            self.handle_message(update['message'])
                
                time.sleep(1)  # Пауза между запросами
                
        except KeyboardInterrupt:
            print("\n=> Остановка бота...")
        except Exception as e:
            print(f"❌ Ошибка работы бота: {e}")

def main():
    bot = SimpleTelegramBot(BOT_TOKEN)
    bot.run()

if __name__ == '__main__':
    main()
