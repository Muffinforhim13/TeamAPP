#!/bin/bash

# TeammatesFinder - Запуск для Linux/Mac

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для цветного вывода
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}💡 $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Заголовок
echo ""
echo "🎮 TeammatesFinder - Запуск для Linux/Mac"
echo "=========================================="
echo ""

# Проверяем Python
if ! command -v python3 &> /dev/null; then
    print_error "Python3 не найден! Установите Python 3.7+"
    exit 1
fi

print_status "Python найден: $(python3 --version)"

# Проверяем .env файл
if [ ! -f ".env" ]; then
    print_error "Не найден файл .env!"
    print_info "Создайте файл .env с содержимым:"
    echo "   BOT_TOKEN=ваш_токен_от_BotFather"
    exit 1
fi

print_status ".env файл найден"

# Устанавливаем зависимости
echo "📦 Устанавливаем зависимости..."
cd backend
if ! pip3 install -r requirements.txt; then
    print_error "Ошибка установки зависимостей!"
    exit 1
fi
cd ..

print_status "Зависимости установлены"

# Создаем временные файлы для логов
mkdir -p logs
BACKEND_LOG="logs/backend.log"
BOT_LOG="logs/bot.log"

echo ""
echo "🚀 Запускаем сервисы..."
echo ""

# Запускаем Backend в фоне
cd backend
python3 app.py > "../$BACKEND_LOG" 2>&1 &
BACKEND_PID=$!
cd ..

# Ждем 3 секунды
sleep 3

# Проверяем что Backend запустился
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    print_error "Backend не запустился! Проверьте логи: $BACKEND_LOG"
    exit 1
fi

print_status "Backend запущен (PID: $BACKEND_PID)"

# Запускаем Bot в фоне
python3 bot/miniapp_bot.py > "$BOT_LOG" 2>&1 &
BOT_PID=$!

# Ждем 2 секунды
sleep 2

# Проверяем что Bot запустился
if ! kill -0 $BOT_PID 2>/dev/null; then
    print_error "Bot не запустился! Проверьте логи: $BOT_LOG"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

print_status "Bot запущен (PID: $BOT_PID)"

echo ""
print_status "Все сервисы запущены успешно!"
echo ""
echo "📱 Инструкции:"
echo "1. Найдите своего бота в Telegram"
echo "2. Отправьте /start"
echo "3. Нажмите кнопку для открытия Mini App"
echo ""
echo "🌐 Backend API: http://localhost:5000"
echo "🤖 Telegram Bot: Работает"
echo ""
echo "📊 Логи:"
echo "   Backend: $BACKEND_LOG"
echo "   Bot: $BOT_LOG"
echo ""
print_info "Для остановки нажмите Ctrl+C"

# Функция остановки при Ctrl+C
cleanup() {
    echo ""
    print_warning "Останавливаем сервисы..."
    
    if kill -0 $BACKEND_PID 2>/dev/null; then
        kill $BACKEND_PID
        print_status "Backend остановлен"
    fi
    
    if kill -0 $BOT_PID 2>/dev/null; then
        kill $BOT_PID
        print_status "Bot остановлен"
    fi
    
    echo "👋 Готово!"
    exit 0
}

# Устанавливаем обработчик Ctrl+C
trap cleanup SIGINT

# Ждем пока процессы работают
while true; do
    # Проверяем что процессы живы
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        print_error "Backend завершился! Проверьте логи: $BACKEND_LOG"
        break
    fi
    
    if ! kill -0 $BOT_PID 2>/dev/null; then
        print_error "Bot завершился! Проверьте логи: $BOT_LOG"
        break
    fi
    
    sleep 1
done

cleanup

