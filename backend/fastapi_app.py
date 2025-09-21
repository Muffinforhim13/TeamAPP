# FastAPI версия Backend для TeammatesFinder Mini App

from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
import json
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

# Добавляем корневую папку в путь для импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import TeammatesDatabase
from games import GAMES_CONFIG

# Создаем FastAPI приложение
app = FastAPI(
    title="TeammatesFinder API",
    description="API для поиска тиммейтов по играм",
    version="1.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация базы данных
db = TeammatesDatabase()

# Pydantic модели для валидации данных
class ProfileCreate(BaseModel):
    display_name: str
    age_group: str
    bio: str
    preferred_games: List[str]
    skill_levels: dict = {}
    play_times: List[str] = ["Вечером"]
    discord_tag: Optional[str] = None
    steam_profile: Optional[str] = None
    looking_for: str
    language: str = "Русский"

class PlayerInteraction(BaseModel):
    target_user_id: int
    interaction_type: str  # 'like' или 'dislike'

# Статические файлы фронтенда
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """Отдаем главную страницу фронтенда"""
    try:
        with open("../frontend/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Frontend не найден</h1>", status_code=404)

@app.get("/api/health")
async def health_check():
    """Проверка работоспособности API"""
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "backend": "FastAPI"
    }

@app.get("/api/games")
async def get_games():
    """Получить список всех игр с конфигурациями"""
    games_list = []
    for game_name, config in GAMES_CONFIG.items():
        games_list.append({
            "name": game_name,
            "display_name": config["display_name"],
            "emoji": config["emoji"],
            "type": config["type"],
            "team_size": config["team_size"]
        })
    
    return {
        "games": games_list,
        "count": len(games_list)
    }

def get_user_id_from_headers(
    x_telegram_user_id: Optional[str] = Header(None)
) -> int:
    """Извлекаем User ID из заголовков Telegram"""
    if not x_telegram_user_id:
        raise HTTPException(status_code=400, detail="User ID not provided")
    
    try:
        return int(x_telegram_user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID")

@app.get("/api/user/profile")
async def get_user_profile(
    user_id: int = None,
    x_telegram_user_id: Optional[str] = Header(None),
    x_telegram_username: Optional[str] = Header(None),
    x_telegram_first_name: Optional[str] = Header(None)
):
    """Получить профиль пользователя"""
    if not user_id:
        user_id = get_user_id_from_headers(x_telegram_user_id)
    
    try:
        # Проверяем есть ли профиль
        if not db.has_profile(user_id):
            return {"has_profile": False}
        
        # Получаем профиль
        profile = db.get_profile(user_id)
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        # Форматируем профиль
        profile_data = format_profile_data(profile)
        
        # Получаем статистику
        stats = db.get_user_stats(user_id)
        
        return {
            "has_profile": True,
            "profile": profile_data,
            "stats": stats
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/user/profile")
async def create_user_profile(
    profile_data: ProfileCreate,
    x_telegram_user_id: Optional[str] = Header(None),
    x_telegram_username: Optional[str] = Header(None),
    x_telegram_first_name: Optional[str] = Header(None)
):
    """Создать профиль пользователя"""
    user_id = get_user_id_from_headers(x_telegram_user_id)
    
    try:
        # Добавляем пользователя если его нет
        db.add_user(user_id, x_telegram_username, x_telegram_first_name)
        
        # Создаем профиль
        db.create_profile(user_id, profile_data.dict())
        
        return {
            "success": True,
            "message": "Profile created successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/players/next")
async def get_next_player(
    x_telegram_user_id: Optional[str] = Header(None)
):
    """Получить следующего игрока для просмотра"""
    user_id = get_user_id_from_headers(x_telegram_user_id)
    
    try:
        # Проверяем есть ли профиль у пользователя
        if not db.has_profile(user_id):
            raise HTTPException(status_code=400, detail="User has no profile")
        
        # Получаем следующего игрока
        player = db.get_next_player_for_user(user_id)
        
        if not player:
            return {"player": None, "message": "No more players"}
        
        # Форматируем данные игрока
        player_data = format_profile_data(player)
        
        return {
            "player": player_data,
            "has_more": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/players/interact")
async def interact_with_player(
    interaction: PlayerInteraction,
    x_telegram_user_id: Optional[str] = Header(None)
):
    """Взаимодействие с игроком (лайк/дизлайк)"""
    user_id = get_user_id_from_headers(x_telegram_user_id)
    
    try:
        if interaction.interaction_type not in ['like', 'dislike']:
            raise HTTPException(status_code=400, detail="Invalid interaction type")
        
        # Записываем взаимодействие
        is_match = db.record_interaction(
            user_id, 
            interaction.target_user_id, 
            interaction.interaction_type
        )
        
        response = {
            "success": True,
            "interaction_type": interaction.interaction_type,
            "is_match": is_match
        }
        
        # Если это мэтч, добавляем информацию о партнере
        if is_match:
            partner_profile = db.get_profile(interaction.target_user_id)
            if partner_profile:
                response["match_partner"] = format_profile_data(partner_profile, include_contacts=True)
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/matches")
async def get_user_matches(
    x_telegram_user_id: Optional[str] = Header(None)
):
    """Получить мэтчи пользователя"""
    user_id = get_user_id_from_headers(x_telegram_user_id)
    
    try:
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
                "match_id": match_id,
                "partner_id": partner_id,
                "partner_name": partner_name,
                "partner_games": json.loads(partner_games) if partner_games else [],
                "partner_profile": partner_data,
                "matched_at": matched_at,
                "is_active": is_active
            })
        
        return {
            "matches": matches_data,
            "count": len(matches_data)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
            "name": game,
            "emoji": config.get("emoji", "🎮"),
            "skill_level": skills_dict.get(game, "Не указан")
        })
    
    profile_data = {
        "user_id": user_id,
        "display_name": display_name,
        "age_group": age_group,
        "bio": bio,
        "avatar_url": avatar_url,
        "games": games_info,
        "play_times": times_list,
        "looking_for": looking_for,
        "language": language,
        "created_at": created_at,
        "updated_at": updated_at
    }
    
    # Добавляем контакты только если нужно
    if include_contacts:
        profile_data["contacts"] = {
            "discord": discord_tag,
            "steam": steam_profile,
            "other": other_contacts
        }
    
    return profile_data

if __name__ == "__main__":
    import uvicorn
    
    # Настройка кодировки для Windows
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass
    
    # Добавляем тестовые профили при запуске
    db.add_sample_profiles()
    
    try:
        print("🚀 TeammatesFinder FastAPI Backend запущен!")
        print("📱 Фронтенд доступен на: http://localhost:8000")
        print("🔗 API документация: http://localhost:8000/docs")
        print("📊 ReDoc документация: http://localhost:8000/redoc")
    except UnicodeEncodeError:
        print("=> TeammatesFinder FastAPI Backend запущен!")
        print("=> Фронтенд доступен на: http://localhost:8000")
        print("=> API документация: http://localhost:8000/docs")
        print("=> ReDoc документация: http://localhost:8000/redoc")
    
    uvicorn.run(
        "fastapi_app:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )
