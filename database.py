import sqlite3
import json
from datetime import datetime
from config import DATABASE_PATH

class TeammatesDatabase:
    def __init__(self):
        self.db_path = DATABASE_PATH
        self.init_database()
    
    def init_database(self):
        """Инициализация базы данных"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Таблица пользователей (базовая информация)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    has_profile BOOLEAN DEFAULT FALSE
                )
            ''')
            
            # Таблица профилей игроков
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS player_profiles (
                    user_id INTEGER PRIMARY KEY,
                    display_name TEXT NOT NULL,
                    age_group TEXT,
                    bio TEXT,
                    avatar_url TEXT,
                    preferred_games TEXT,  -- JSON список игр
                    skill_levels TEXT,     -- JSON объект {игра: уровень}
                    play_times TEXT,       -- JSON список времени игры
                    discord_tag TEXT,
                    steam_profile TEXT,
                    other_contacts TEXT,
                    looking_for TEXT,      -- что ищет: "Команда", "Дуо", "Компания"
                    language TEXT DEFAULT 'Русский',
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # Таблица взаимодействий между игроками
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS player_interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    from_user_id INTEGER,
                    to_user_id INTEGER,
                    interaction_type TEXT,  -- 'like', 'dislike', 'view'
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (from_user_id) REFERENCES users (user_id),
                    FOREIGN KEY (to_user_id) REFERENCES users (user_id),
                    UNIQUE(from_user_id, to_user_id, interaction_type)
                )
            ''')
            
            # Таблица мэтчей (взаимных лайков)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS matches (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user1_id INTEGER,
                    user2_id INTEGER,
                    matched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT TRUE,
                    FOREIGN KEY (user1_id) REFERENCES users (user_id),
                    FOREIGN KEY (user2_id) REFERENCES users (user_id),
                    UNIQUE(user1_id, user2_id)
                )
            ''')
            
            # Таблица сообщений между мэтчами
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS match_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    match_id INTEGER,
                    from_user_id INTEGER,
                    message_text TEXT,
                    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (match_id) REFERENCES matches (id),
                    FOREIGN KEY (from_user_id) REFERENCES users (user_id)
                )
            ''')
            
            conn.commit()
    
    def add_user(self, user_id, username=None, first_name=None):
        """Добавить нового пользователя"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO users (user_id, username, first_name)
                VALUES (?, ?, ?)
            ''', (user_id, username, first_name))
            conn.commit()
    
    def get_user(self, user_id):
        """Получить информацию о пользователе"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            return cursor.fetchone()
    
    def has_profile(self, user_id):
        """Проверить, есть ли у пользователя профиль"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT has_profile FROM users WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()
            return result[0] if result else False
    
    def create_profile(self, user_id, profile_data):
        """Создать профиль игрока"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Создаем профиль
            cursor.execute('''
                INSERT OR REPLACE INTO player_profiles 
                (user_id, display_name, age_group, bio, preferred_games, skill_levels, 
                 play_times, discord_tag, steam_profile, looking_for, language)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id,
                profile_data['display_name'],
                profile_data['age_group'],
                profile_data['bio'],
                json.dumps(profile_data['preferred_games']),
                json.dumps(profile_data['skill_levels']),
                json.dumps(profile_data['play_times']),
                profile_data.get('discord_tag'),
                profile_data.get('steam_profile'),
                profile_data['looking_for'],
                profile_data.get('language', 'Русский')
            ))
            
            # Обновляем флаг наличия профиля
            cursor.execute('UPDATE users SET has_profile = TRUE WHERE user_id = ?', (user_id,))
            conn.commit()
    
    def get_profile(self, user_id):
        """Получить профиль игрока"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM player_profiles WHERE user_id = ?', (user_id,))
            return cursor.fetchone()
    
    def update_profile(self, user_id, profile_data):
        """Обновить профиль игрока"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE player_profiles SET
                display_name = ?, age_group = ?, bio = ?, preferred_games = ?,
                skill_levels = ?, play_times = ?, discord_tag = ?, steam_profile = ?,
                looking_for = ?, language = ?, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            ''', (
                profile_data['display_name'],
                profile_data['age_group'],
                profile_data['bio'],
                json.dumps(profile_data['preferred_games']),
                json.dumps(profile_data['skill_levels']),
                json.dumps(profile_data['play_times']),
                profile_data.get('discord_tag'),
                profile_data.get('steam_profile'),
                profile_data['looking_for'],
                profile_data.get('language', 'Русский'),
                user_id
            ))
            conn.commit()
    
    def get_next_player_for_user(self, user_id):
        """Получить следующего игрока для просмотра"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Получаем игроков, которых пользователь еще не видел
            cursor.execute('''
                SELECT pp.* FROM player_profiles pp
                WHERE pp.user_id != ? 
                AND pp.is_active = TRUE
                AND pp.user_id NOT IN (
                    SELECT to_user_id FROM player_interactions 
                    WHERE from_user_id = ? AND interaction_type IN ('like', 'dislike')
                )
                ORDER BY RANDOM()
                LIMIT 1
            ''', (user_id, user_id))
            return cursor.fetchone()
    
    def record_interaction(self, from_user_id, to_user_id, interaction_type):
        """Записать взаимодействие между игроками"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Записываем взаимодействие
            cursor.execute('''
                INSERT OR REPLACE INTO player_interactions 
                (from_user_id, to_user_id, interaction_type)
                VALUES (?, ?, ?)
            ''', (from_user_id, to_user_id, interaction_type))
            
            # Если это лайк, проверяем взаимность
            if interaction_type == 'like':
                cursor.execute('''
                    SELECT id FROM player_interactions 
                    WHERE from_user_id = ? AND to_user_id = ? AND interaction_type = 'like'
                ''', (to_user_id, from_user_id))
                
                if cursor.fetchone():  # Есть взаимный лайк
                    # Создаем мэтч
                    user1_id = min(from_user_id, to_user_id)
                    user2_id = max(from_user_id, to_user_id)
                    
                    cursor.execute('''
                        INSERT OR IGNORE INTO matches (user1_id, user2_id)
                        VALUES (?, ?)
                    ''', (user1_id, user2_id))
                    
                    conn.commit()
                    return True  # Возвращаем True если это мэтч
            
            conn.commit()
            return False
    
    def get_user_matches(self, user_id):
        """Получить мэтчи пользователя"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT m.*, pp1.display_name as user1_name, pp2.display_name as user2_name,
                       pp1.preferred_games as user1_games, pp2.preferred_games as user2_games
                FROM matches m
                JOIN player_profiles pp1 ON m.user1_id = pp1.user_id
                JOIN player_profiles pp2 ON m.user2_id = pp2.user_id
                WHERE (m.user1_id = ? OR m.user2_id = ?) AND m.is_active = TRUE
                ORDER BY m.matched_at DESC
            ''', (user_id, user_id))
            return cursor.fetchall()
    
    def get_user_stats(self, user_id):
        """Получить статистику пользователя"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Количество лайков отданных
            cursor.execute('''
                SELECT COUNT(*) FROM player_interactions 
                WHERE from_user_id = ? AND interaction_type = 'like'
            ''', (user_id,))
            likes_given = cursor.fetchone()[0]
            
            # Количество лайков полученных
            cursor.execute('''
                SELECT COUNT(*) FROM player_interactions 
                WHERE to_user_id = ? AND interaction_type = 'like'
            ''', (user_id,))
            likes_received = cursor.fetchone()[0]
            
            # Количество мэтчей
            cursor.execute('''
                SELECT COUNT(*) FROM matches 
                WHERE (user1_id = ? OR user2_id = ?) AND is_active = TRUE
            ''', (user_id, user_id))
            matches_count = cursor.fetchone()[0]
            
            # Количество просмотренных профилей
            cursor.execute('''
                SELECT COUNT(*) FROM player_interactions 
                WHERE from_user_id = ? AND interaction_type IN ('like', 'dislike')
            ''', (user_id,))
            profiles_viewed = cursor.fetchone()[0]
            
            return {
                'likes_given': likes_given,
                'likes_received': likes_received,
                'matches_count': matches_count,
                'profiles_viewed': profiles_viewed
            }
    
    def search_players_by_game(self, user_id, game_name):
        """Поиск игроков по конкретной игре"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT pp.* FROM player_profiles pp
                WHERE pp.user_id != ? 
                AND pp.is_active = TRUE
                AND pp.preferred_games LIKE ?
                ORDER BY pp.updated_at DESC
            ''', (user_id, f'%{game_name}%'))
            return cursor.fetchall()
    
    def add_sample_profiles(self):
        """Добавить примеры профилей для тестирования"""
        sample_profiles = [
            {
                'user_id': 111111111,
                'display_name': 'ProGamer2024',
                'age_group': '21-25',
                'bio': 'Ищу команду для CS2 и Valorant. Играю на высоком уровне, общительный.',
                'preferred_games': ['Counter-Strike 2', 'Valorant', 'Apex Legends'],
                'skill_levels': {'Counter-Strike 2': 'Профи', 'Valorant': 'Опытный'},
                'play_times': ['Вечером', 'Выходные'],
                'discord_tag': 'ProGamer#1234',
                'looking_for': 'Команда',
                'language': 'Русский'
            },
            {
                'user_id': 222222222,
                'display_name': 'CasualGirl',
                'age_group': '18-25',
                'bio': 'Люблю играть в Minecraft и Among Us. Ищу дружескую компанию для совместных игр.',
                'preferred_games': ['Minecraft', 'Among Us', 'Fall Guys'],
                'skill_levels': {'Minecraft': 'Любитель', 'Among Us': 'Опытный'},
                'play_times': ['Днем', 'Вечером'],
                'discord_tag': 'CasualGirl#5678',
                'looking_for': 'Компания',
                'language': 'Русский'
            }
        ]
        
        # Добавляем пользователей и профили
        for profile in sample_profiles:
            user_id = profile['user_id']
            self.add_user(user_id, f"sample_user_{user_id}", "Sample User")
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR IGNORE INTO player_profiles 
                    (user_id, display_name, age_group, bio, preferred_games, skill_levels, 
                     play_times, discord_tag, looking_for, language)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    user_id,
                    profile['display_name'],
                    profile['age_group'],
                    profile['bio'],
                    json.dumps(profile['preferred_games']),
                    json.dumps(profile['skill_levels']),
                    json.dumps(profile['play_times']),
                    profile['discord_tag'],
                    profile['looking_for'],
                    profile['language']
                ))
                
                cursor.execute('UPDATE users SET has_profile = TRUE WHERE user_id = ?', (user_id,))
                conn.commit()