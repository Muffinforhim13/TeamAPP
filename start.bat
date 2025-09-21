@echo off
chcp 65001 >nul
cls

echo.
echo 🎮 TeammatesFinder - Запуск для Windows
echo =======================================
echo.

REM Проверяем Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не найден! Установите Python 3.7+
    pause
    exit /b 1
)

REM Проверяем .env файл
if not exist ".env" (
    echo ❌ Не найден файл .env!
    echo 💡 Создайте файл .env с содержимым:
    echo    BOT_TOKEN=ваш_токен_от_BotFather
    pause
    exit /b 1
)

echo 📦 Устанавливаем зависимости...
cd backend
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Ошибка установки зависимостей!
    pause
    exit /b 1
)
cd ..

echo.
echo 🚀 Запускаем сервисы...
echo.

REM Запускаем Backend в новом окне
start "TeammatesFinder Backend" cmd /k "cd backend && python app.py"

REM Ждем 3 секунды
timeout /t 3 /nobreak >nul

REM Запускаем Bot в новом окне  
start "TeammatesFinder Bot" cmd /k "python bot/miniapp_bot.py"

echo ✅ Сервисы запущены в отдельных окнах!
echo.
echo 📱 Инструкции:
echo 1. Найдите своего бота в Telegram
echo 2. Отправьте /start
echo 3. Нажмите кнопку для открытия Mini App
echo.
echo 🌐 Backend API: http://localhost:5000
echo 🤖 Telegram Bot: Работает в отдельном окне
echo.
echo Для остановки закройте окна Backend и Bot
echo.
pause

