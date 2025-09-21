# Модуль конфигураций игр для TeammatesFinder

from .dota2 import DOTA2_CONFIG
from .cs2 import CS2_CONFIG  
from .valorant import VALORANT_CONFIG
from .mlbb import MLBB_CONFIG
from .lol import LOL_CONFIG

# Словарь всех игр
GAMES_CONFIG = {
    'Dota 2': DOTA2_CONFIG,
    'Counter-Strike 2': CS2_CONFIG,
    'Valorant': VALORANT_CONFIG,
    'Mobile Legends': MLBB_CONFIG,
    'League of Legends': LOL_CONFIG
}

# Список всех поддерживаемых игр
SUPPORTED_GAMES = list(GAMES_CONFIG.keys())

def get_game_config(game_name):
    """Получить конфигурацию игры по названию"""
    return GAMES_CONFIG.get(game_name)

def get_game_ranks(game_name):
    """Получить список рангов для игры"""
    config = get_game_config(game_name)
    return config.get('ranks', []) if config else []

def get_game_roles(game_name):
    """Получить список ролей для игры"""
    config = get_game_config(game_name)
    return config.get('roles', []) if config else []

def get_game_servers(game_name):
    """Получить список серверов для игры"""
    config = get_game_config(game_name)
    return config.get('servers', []) if config else []

