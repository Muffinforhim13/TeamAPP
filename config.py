import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Настройки бота
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

# Настройки базы данных
DATABASE_PATH = 'teammates_bot.db'

# Настройки пагинации
PROFILES_PER_SESSION = 50

# Импорт игровых конфигураций
from games import GAMES_CONFIG, SUPPORTED_GAMES

# Основные поддерживаемые игры (с детальными конфигурациями)
MAIN_GAMES = SUPPORTED_GAMES

# Дополнительные популярные игры
ADDITIONAL_GAMES = [
    'Apex Legends', 'Overwatch 2', 'Rocket League', 'PUBG',
    'Fortnite', 'Rainbow Six Siege', 'World of Warcraft', 'Destiny 2',
    'Call of Duty', 'Minecraft', 'Among Us', 'Fall Guys',
    'FIFA', 'Battlefield', 'Hearthstone', 'Teamfight Tactics'
]

# Все игры
POPULAR_GAMES = MAIN_GAMES + ADDITIONAL_GAMES

# Возрастные группы
AGE_GROUPS = ['16-20', '21-25', '26-30', '31-35', '36+']

# Уровни игры
SKILL_LEVELS = ['Новичок', 'Любитель', 'Опытный', 'Профи']

# Предпочтения времени игры
PLAY_TIMES = ['Утром', 'Днем', 'Вечером', 'Ночью', 'Выходные', 'Гибкий график']

# Сообщения
MESSAGES = {
    'welcome': """
🎮 Добро пожаловать в TeammatesFinder!

Этот бот поможет тебе найти тиммейтов для твоих любимых игр!
Листай профили игроков и находи идеальных напарников! 

Для начала нужно создать свой профиль /create_profile

Команды:
/start - начать заново
/create_profile - создать профиль
/edit_profile - редактировать профиль
/my_profile - мой профиль
/matches - мои мэтчи
/help - помощь
""",
    
    'no_profile': """
❗ У тебя пока нет профиля!

Создай профиль командой /create_profile чтобы начать поиск тиммейтов.
""",
    
    'no_more_players': """
🎉 Ты просмотрел всех доступных игроков!

Можешь:
• Посмотреть свои мэтчи /matches
• Отредактировать профиль /edit_profile
• Начать поиск заново /start
""",
    
    'player_liked': "❤️ Игрок добавлен в понравившиеся!",
    'player_disliked': "❌ Игрок пропущен",
    'match_found': "🎉 У вас взаимный лайк! Теперь вы можете общаться!",
    'profile_created': "✅ Профиль создан! Теперь можешь искать тиммейтов!",
    'profile_updated': "✅ Профиль обновлен!"
}
