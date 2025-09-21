@echo off
chcp 65001 >nul
cls

echo.
echo 🎮 TeammatesFinder - Полный запуск
echo ===================================
echo.

REM Проверяем .env файл
if not exist ".env" (
    echo ❌ Не найден файл .env!
    echo 💡 Создайте файл .env с токеном бота
    pause
    exit /b 1
)

echo 🚀 Запускаем все сервисы...
echo.

REM Запускаем Backend в новом окне
echo 📡 Запускаем Backend API...
start "TeammatesFinder Backend" cmd /k "cd backend && python app.py"

REM Ждем 3 секунды
timeout /t 3 /nobreak >nul

REM Запускаем LocalTunnel в новом окне
echo 🌐 Запускаем LocalTunnel...
start "LocalTunnel" cmd /k "lt --port 5000"

REM Ждем 5 секунд для получения URL
timeout /t 5 /nobreak >nul

REM Запускаем Bot в новом окне
echo 🤖 Запускаем Telegram Bot...
start "TeammatesFinder Bot" cmd /k "python bot/basic_bot.py"

echo.
echo ✅ Все сервисы запущены в отдельных окнах!
echo.
echo 📱 Инструкции:
echo 1. Скопируйте HTTPS URL из окна LocalTunnel
echo 2. Обновите файл .env: WEBAPP_URL=ваш_https_url
echo 3. Укажите этот URL в @BotFather через /setmenubutton
echo 4. Найдите бота в Telegram и отправьте /start
echo 5. Нажмите кнопку TeammatesFinder внизу экрана
echo.
echo 🌐 Backend: http://localhost:5000
echo 🤖 Bot: Работает в отдельном окне
echo 🌍 Tunnel: Смотрите окно LocalTunnel
echo.
echo Для остановки закройте все окна
echo.
pause
