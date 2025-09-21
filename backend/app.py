# Backend API для TeammatesFinder Mini App

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
import json
from datetime import datetime

# Добавляем корневую папку в путь для импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import TeammatesDatabase
from games import GAMES_CONFIG

app = Flask(__name__)
CORS(app)  # Разрешаем CORS для фронтенда

# Инициализация базы данных
db = TeammatesDatabase()

# Статические файлы фронтенда
@app.route('/')
def serve_frontend():
    return send_from_directory('templates', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    try:
        return send_from_directory('templates', path)
    except:
        return send_from_directory('../frontend', path)

# API маршруты

@app.route('/api/health', methods=['GET'])
def health_check():
    """Проверка работоспособности API"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/games', methods=['GET'])
def get_games():
    """Получить список всех игр с конфигурациями"""
    games_list = []
    for game_name, config in GAMES_CONFIG.items():
        games_list.append({
            'name': game_name,
            'display_name': config['display_name'],
            'emoji': config['emoji'],
            'type': config['type'],
            'team_size': config['team_size']
        })
    
    return jsonify({
        'games': games_list,
        'count': len(games_list)
    })

@app.route('/api/user/profile', methods=['GET'])
def get_user_profile():
    """Получить профиль пользователя"""
    user_id = request.headers.get('X-Telegram-User-ID')
    
    if not user_id:
        return jsonify({'error': 'User ID not provided'}), 400
    
    try:
        user_id = int(user_id)
        
        # Проверяем есть ли профиль
        if not db.has_profile(user_id):
            return jsonify({'has_profile': False})
        
        # Получаем профиль
        profile = db.get_profile(user_id)
        if not profile:
            return jsonify({'error': 'Profile not found'}), 404
        
        # Форматируем профиль
        profile_data = format_profile_data(profile)
        
        # Получаем статистику
        stats = db.get_user_stats(user_id)
        
        return jsonify({
            'has_profile': True,
            'profile': profile_data,
            'stats': stats
        })
        
    except ValueError:
        return jsonify({'error': 'Invalid user ID'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/user/profile', methods=['POST'])
def create_user_profile():
    """Создать профиль пользователя"""
    user_id = request.headers.get('X-Telegram-User-ID')
    username = request.headers.get('X-Telegram-Username')
    first_name = request.headers.get('X-Telegram-First-Name')
    
    if not user_id:
        return jsonify({'error': 'User ID not provided'}), 400
    
    try:
        user_id = int(user_id)
        data = request.get_json()
        
        # Валидация данных
        required_fields = ['display_name', 'age_group', 'bio', 'preferred_games', 'looking_for']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Field {field} is required'}), 400
        
        # Добавляем пользователя если его нет
        db.add_user(user_id, username, first_name)
        
        # Подготавливаем данные профиля
        profile_data = {
            'display_name': data['display_name'],
            'age_group': data['age_group'],
            'bio': data['bio'],
            'preferred_games': data['preferred_games'],
            'skill_levels': data.get('skill_levels', {}),
            'play_times': data.get('play_times', ['Вечером']),
            'discord_tag': data.get('discord_tag'),
            'steam_profile': data.get('steam_profile'),
            'looking_for': data['looking_for'],
            'language': 'Русский'
        }
        
        # Создаем профиль
        db.create_profile(user_id, profile_data)
        
        return jsonify({
            'success': True,
            'message': 'Profile created successfully'
        })
        
    except ValueError:
        return jsonify({'error': 'Invalid user ID'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/players/next', methods=['GET'])
def get_next_player():
    """Получить следующего игрока для просмотра"""
    user_id = request.headers.get('X-Telegram-User-ID')
    
    if not user_id:
        return jsonify({'error': 'User ID not provided'}), 400
    
    try:
        user_id = int(user_id)
        
        # Проверяем есть ли профиль у пользователя
        if not db.has_profile(user_id):
            return jsonify({'error': 'User has no profile'}), 400
        
        # Получаем следующего игрока
        player = db.get_next_player_for_user(user_id)
        
        if not player:
            return jsonify({'player': None, 'message': 'No more players'})
        
        # Форматируем данные игрока
        player_data = format_profile_data(player)
        
        return jsonify({
            'player': player_data,
            'has_more': True
        })
        
    except ValueError:
        return jsonify({'error': 'Invalid user ID'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/players/interact', methods=['POST'])
def interact_with_player():
    """Взаимодействие с игроком (лайк/дизлайк)"""
    user_id = request.headers.get('X-Telegram-User-ID')
    
    if not user_id:
        return jsonify({'error': 'User ID not provided'}), 400
    
    try:
        user_id = int(user_id)
        data = request.get_json()
        
        target_user_id = data.get('target_user_id')
        interaction_type = data.get('interaction_type')  # 'like' или 'dislike'
        
        if not target_user_id or not interaction_type:
            return jsonify({'error': 'Missing required fields'}), 400
        
        if interaction_type not in ['like', 'dislike']:
            return jsonify({'error': 'Invalid interaction type'}), 400
        
        # Записываем взаимодействие
        is_match = db.record_interaction(user_id, target_user_id, interaction_type)
        
        response = {
            'success': True,
            'interaction_type': interaction_type,
            'is_match': is_match
        }
        
        # Если это мэтч, добавляем информацию о партнере
        if is_match:
            partner_profile = db.get_profile(target_user_id)
            if partner_profile:
                response['match_partner'] = format_profile_data(partner_profile, include_contacts=True)
        
        return jsonify(response)
        
    except ValueError:
        return jsonify({'error': 'Invalid user ID'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/matches', methods=['GET'])
def get_user_matches():
    """Получить мэтчи пользователя"""
    user_id = request.headers.get('X-Telegram-User-ID')
    
    if not user_id:
        return jsonify({'error': 'User ID not provided'}), 400
    
    try:
        user_id = int(user_id)
        
        # Получаем мэтчи
        matches = db.get_user_matches(user_id)
        
        matches_data = []
        for match in matches:
            (match_id, user1_id, user2_id, matched_at, is_active, 
             user1_name, user2_name, user1_games, user2_games) = match
            
            # Определяем партнера
            partner_id = user2_id if user1_id == user_id else user1_id
            partner_name = user2_name if user1_id == user_id else user1_name
            partner_games = user2_games if user1_id == user_id else user1_games
            
            # Получаем полный профиль партнера
            partner_profile = db.get_profile(partner_id)
            partner_data = format_profile_data(partner_profile, include_contacts=True) if partner_profile else None
            
            matches_data.append({
                'match_id': match_id,
                'partner_id': partner_id,
                'partner_name': partner_name,
                'partner_games': json.loads(partner_games) if partner_games else [],
                'partner_profile': partner_data,
                'matched_at': matched_at,
                'is_active': is_active
            })
        
        return jsonify({
            'matches': matches_data,
            'count': len(matches_data)
        })
        
    except ValueError:
        return jsonify({'error': 'Invalid user ID'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def format_profile_data(profile, include_contacts=False):
    """Форматировать данные профиля для API"""
    if not profile:
        return None
    
    (user_id, display_name, age_group, bio, avatar_url, preferred_games, 
     skill_levels, play_times, discord_tag, steam_profile, other_contacts, 
     looking_for, language, is_active, created_at, updated_at) = profile
    
    # Парсим JSON данные
    games_list = json.loads(preferred_games) if preferred_games else []
    skills_dict = json.loads(skill_levels) if skill_levels else {}
    times_list = json.loads(play_times) if play_times else []
    
    # Форматируем игры с информацией
    games_info = []
    for game in games_list:
        config = GAMES_CONFIG.get(game, {})
        games_info.append({
            'name': game,
            'emoji': config.get('emoji', '🎮'),
            'skill_level': skills_dict.get(game, 'Не указан')
        })
    
    profile_data = {
        'user_id': user_id,
        'display_name': display_name,
        'age_group': age_group,
        'bio': bio,
        'avatar_url': avatar_url,
        'games': games_info,
        'play_times': times_list,
        'looking_for': looking_for,
        'language': language,
        'created_at': created_at,
        'updated_at': updated_at
    }
    
    # Добавляем контакты только если нужно
    if include_contacts:
        profile_data['contacts'] = {
            'discord': discord_tag,
            'steam': steam_profile,
            'other': other_contacts
        }
    
    return profile_data

if __name__ == '__main__':
    # Настройка кодировки для Windows
    import locale
    import codecs
    
    try:
        # Пытаемся установить UTF-8 для консоли
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except:
        # Если не получается, используем безопасный вывод
        pass
    
    # Добавляем тестовые профили при запуске
    db.add_sample_profiles()
    
    try:
        print("🚀 TeammatesFinder Backend запущен!")
        print("📱 Фронтенд доступен на: http://localhost:5000")
        print("🔗 API доступен на: http://localhost:5000/api/")
    except UnicodeEncodeError:
        print("=> TeammatesFinder Backend запущен!")
        print("=> Фронтенд доступен на: http://localhost:5000")
        print("=> API доступен на: http://localhost:5000/api/")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

