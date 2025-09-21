# Утилиты для работы с игровыми конфигурациями

from games import GAMES_CONFIG, get_game_config, get_game_ranks, get_game_roles
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def create_games_keyboard(selected_games=None, callback_prefix="game"):
    """Создать клавиатуру для выбора игр"""
    if selected_games is None:
        selected_games = []
    
    keyboard = []
    
    # Основные игры с эмодзи
    for game_name, config in GAMES_CONFIG.items():
        emoji = "✅ " if game_name in selected_games else ""
        display_name = f"{emoji}{config['emoji']} {game_name}"
        keyboard.append([InlineKeyboardButton(
            display_name, 
            callback_data=f"{callback_prefix}_{game_name}"
        )])
    
    # Кнопка завершения
    keyboard.append([InlineKeyboardButton("✅ Готово", callback_data=f"{callback_prefix}_done")])
    
    return InlineKeyboardMarkup(keyboard)

def create_ranks_keyboard(game_name, callback_prefix="rank"):
    """Создать клавиатуру для выбора ранга в игре"""
    config = get_game_config(game_name)
    if not config:
        return None
    
    ranks = config.get('ranks', [])
    keyboard = []
    
    for rank in ranks:
        keyboard.append([InlineKeyboardButton(
            rank, 
            callback_data=f"{callback_prefix}_{game_name}_{rank}"
        )])
    
    return InlineKeyboardMarkup(keyboard)

def create_roles_keyboard(game_name, callback_prefix="role"):
    """Создать клавиатуру для выбора роли в игре"""
    config = get_game_config(game_name)
    if not config:
        return None
    
    roles = config.get('roles', [])
    keyboard = []
    
    for role in roles:
        keyboard.append([InlineKeyboardButton(
            role, 
            callback_data=f"{callback_prefix}_{game_name}_{role}"
        )])
    
    return InlineKeyboardMarkup(keyboard)

def format_player_profile_text(profile_data, include_contacts=False):
    """Форматировать текст профиля игрока"""
    import json
    
    (user_id, display_name, age_group, bio, avatar_url, preferred_games, 
     skill_levels, play_times, discord_tag, steam_profile, other_contacts, 
     looking_for, language, is_active, created_at, updated_at) = profile_data
    
    # Парсим JSON данные
    games_list = json.loads(preferred_games) if preferred_games else []
    skills_dict = json.loads(skill_levels) if skill_levels else {}
    times_list = json.loads(play_times) if play_times else []
    
    # Форматируем игры с эмодзи
    games_text = []
    for game in games_list:
        config = get_game_config(game)
        emoji = config['emoji'] if config else '🎮'
        skill = skills_dict.get(game, 'Не указан')
        games_text.append(f"{emoji} {game} ({skill})")
    
    profile_text = f"""
🎮 <b>{display_name}</b>
👥 Возраст: {age_group} | 🎯 Ищет: {looking_for}

📝 <b>О себе:</b>
{bio}

🎮 <b>Игры и уровень:</b>
{chr(10).join(games_text) if games_text else 'Не указаны'}

🕐 <b>Играет:</b> {', '.join(times_list) if times_list else 'Не указано'}
"""
    
    # Добавляем контакты если нужно
    if include_contacts:
        profile_text += f"""
📞 <b>Контакты:</b>
Discord: {discord_tag or 'Не указан'}
Steam: {steam_profile or 'Не указан'}
"""
    
    return profile_text

def get_game_specific_questions(game_name):
    """Получить специфические вопросы для игры"""
    config = get_game_config(game_name)
    if not config:
        return []
    
    questions = []
    
    # Вопрос о ранге
    if 'ranks' in config:
        questions.append({
            'type': 'rank',
            'question': f"Какой у тебя ранг в {config['display_name']}?",
            'options': config['ranks']
        })
    
    # Вопрос о роли
    if 'roles' in config:
        questions.append({
            'type': 'role', 
            'question': f"Какую роль предпочитаешь в {config['display_name']}?",
            'options': config['roles']
        })
    
    # Вопрос о сервере
    if 'servers' in config:
        questions.append({
            'type': 'server',
            'question': f"На каком сервере играешь в {config['display_name']}?", 
            'options': config['servers']
        })
    
    return questions

def get_matching_score(user_profile, target_profile):
    """Вычислить совместимость двух профилей (0-100)"""
    import json
    
    score = 0
    max_score = 0
    
    # Парсим данные профилей
    user_games = json.loads(user_profile[5]) if user_profile[5] else []
    target_games = json.loads(target_profile[5]) if target_profile[5] else []
    
    user_times = json.loads(user_profile[7]) if user_profile[7] else []
    target_times = json.loads(target_profile[7]) if target_profile[7] else []
    
    # Совпадение игр (40% веса)
    common_games = set(user_games) & set(target_games)
    if user_games and target_games:
        game_score = len(common_games) / max(len(user_games), len(target_games)) * 40
        score += game_score
    max_score += 40
    
    # Совпадение времени игры (30% веса)
    common_times = set(user_times) & set(target_times)
    if user_times and target_times:
        time_score = len(common_times) / max(len(user_times), len(target_times)) * 30
        score += time_score
    max_score += 30
    
    # Совпадение возрастной группы (20% веса)
    if user_profile[2] == target_profile[2]:  # age_group
        score += 20
    max_score += 20
    
    # Совпадение цели поиска (10% веса)
    if user_profile[11] == target_profile[11]:  # looking_for
        score += 10
    max_score += 10
    
    return int(score / max_score * 100) if max_score > 0 else 0

def suggest_profile_improvements(profile_data):
    """Предложить улучшения для профиля"""
    import json
    
    suggestions = []
    
    (user_id, display_name, age_group, bio, avatar_url, preferred_games, 
     skill_levels, play_times, discord_tag, steam_profile, other_contacts, 
     looking_for, language, is_active, created_at, updated_at) = profile_data
    
    # Проверяем заполненность профиля
    if not bio or len(bio) < 20:
        suggestions.append("📝 Добавь более подробное описание о себе")
    
    if not preferred_games or len(json.loads(preferred_games)) < 2:
        suggestions.append("🎮 Добавь больше игр в свой профиль")
    
    if not discord_tag and not steam_profile:
        suggestions.append("📞 Добавь контакты для связи (Discord/Steam)")
    
    if not play_times or len(json.loads(play_times)) < 2:
        suggestions.append("🕐 Укажи больше времени когда играешь")
    
    # Игро-специфичные советы
    games_list = json.loads(preferred_games) if preferred_games else []
    for game in games_list:
        config = get_game_config(game)
        if config and 'profile_tips' in config:
            suggestions.extend([f"💡 {tip}" for tip in config['profile_tips'][:2]])
    
    return suggestions[:5]  # Максимум 5 советов

