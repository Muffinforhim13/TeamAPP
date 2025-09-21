# Конфигурация для League of Legends

LOL_CONFIG = {
    'name': 'League of Legends',
    'display_name': '⚡ League of Legends',
    'emoji': '⚡',
    'type': 'MOBA',
    'team_size': 5,
    
    # Ранги LoL (2024 Season)
    'ranks': [
        'Iron IV',
        'Iron III',
        'Iron II', 
        'Iron I',
        'Bronze IV',
        'Bronze III',
        'Bronze II',
        'Bronze I',
        'Silver IV',
        'Silver III',
        'Silver II',
        'Silver I',
        'Gold IV',
        'Gold III',
        'Gold II',
        'Gold I',
        'Platinum IV',
        'Platinum III',
        'Platinum II',
        'Platinum I',
        'Emerald IV',
        'Emerald III',
        'Emerald II',
        'Emerald I',
        'Diamond IV',
        'Diamond III',
        'Diamond II',
        'Diamond I',
        'Master',
        'Grandmaster',
        'Challenger',
        'Не калиброван'
    ],
    
    # Роли в LoL
    'roles': [
        '⚔️ Top (Топ)',
        '🌲 Jungle (Лес)',
        '⚡ Mid (Мид)',
        '🏹 ADC (АДК)',
        '🛡️ Support (Саппорт)',
        '🔄 Fill (Автозаполнение)'
    ],
    
    # Популярные чемпионы по ролям
    'champions': {
        'Top': [
            'Garen', 'Darius', 'Fiora', 'Camille', 'Jax',
            'Aatrox', 'Riven', 'Yasuo', 'Irelia', 'Sett',
            'Ornn', 'Malphite', 'Cho\'Gath', 'Sion', 'K\'Sante'
        ],
        'Jungle': [
            'Graves', 'Kha\'Zix', 'Lee Sin', 'Ekko', 'Hecarim',
            'Amumu', 'Warwick', 'Master Yi', 'Shyvana', 'Viego',
            'Kindred', 'Elise', 'Rek\'Sai', 'Sejuani', 'Lillia'
        ],
        'Mid': [
            'Yasuo', 'Yone', 'Zed', 'Ahri', 'Syndra',
            'Orianna', 'Azir', 'LeBlanc', 'Katarina', 'Akali',
            'Viktor', 'Corki', 'Kassadin', 'Vex', 'Hwei'
        ],
        'ADC': [
            'Jinx', 'Caitlyn', 'Ezreal', 'Vayne', 'Kai\'Sa',
            'Xayah', 'Miss Fortune', 'Ashe', 'Jhin', 'Lucian',
            'Aphelios', 'Samira', 'Zeri', 'Nilah', 'Briar'
        ],
        'Support': [
            'Thresh', 'Blitzcrank', 'Leona', 'Nautilus', 'Alistar',
            'Lulu', 'Janna', 'Soraka', 'Nami', 'Yuumi',
            'Pyke', 'Rakan', 'Braum', 'Zyra', 'Milio'
        ]
    },
    
    # Серверы/регионы
    'servers': [
        '🇷🇺 Russia (RU)',
        '🇪🇺 EU West (EUW)',
        '🇪🇺 EU Nordic & East (EUNE)',
        '🇺🇸 North America (NA)',
        '🇰🇷 Korea (KR)',
        '🇨🇳 China (CN)',
        '🇧🇷 Brazil (BR)',
        '🇯🇵 Japan (JP)',
        '🇦🇺 Oceania (OCE)',
        '🇹🇷 Turkey (TR)',
        '🇸🇬 Singapore (SG)'
    ],
    
    # Режимы игры
    'game_modes': [
        '🏆 Ranked Solo/Duo',
        '👥 Ranked Flex',
        '⚔️ Normal Draft',
        '🎲 Normal Blind',
        '🏃 ARAM',
        '🎯 Ultimate Spellbook',
        '🎪 Rotating Game Modes',
        '🤖 AI режимы',
        '🏆 Clash'
    ],
    
    # Что ищет игрок
    'looking_for': [
        '👥 Постоянная команда 5x5',
        '🤝 Дуо партнер для ranked',
        '🏆 Clash команда',
        '📚 Тренировки и VoD review',
        '😄 Normal games',
        '🎯 Climb в ранге',
        '🏅 Tournament команда',
        '🎮 ARAM компания',
        '🎓 Coaching/менторство'
    ],
    
    # Дополнительные критерии
    'additional_info': [
        '🎤 Есть микрофон',
        '🇷🇺 Говорю на русском',
        '🇬🇧 Говорю на английском',
        '🌃 Играю поздно вечером',
        '🌅 Играю утром/днем',
        '💪 Серьезный подход',
        '😊 Без токсичности',
        '📊 Анализирую игру',
        '🎯 Знаю мету',
        '🏆 Опыт турниров',
        '💰 Много скинов'
    ],
    
    # Стиль игры
    'playstyles': [
        '🎯 Aggressive (Агрессивный)',
        '🛡️ Defensive (Оборонительный)',
        '🧠 Macro-focused (Макро игра)',
        '⚔️ Teamfight oriented',
        '🕵️ Split-push',
        '🎭 Versatile (Универсальный)'
    ],
    
    # Типы игроков
    'player_types': [
        '🏆 Ranked grinder',
        '😄 For fun player',
        '🎓 Learning focused',
        '🏅 Competitive player',
        '🎮 One-trick pony',
        '🔄 Jack of all trades'
    ],
    
    # Полезные ссылки
    'links': {
        'official': 'https://www.leagueoflegends.com/',
        'opgg': 'https://op.gg/',
        'u.gg': 'https://u.gg/',
        'reddit': 'https://www.reddit.com/r/leagueoflegends/',
        'probuilds': 'https://probuilds.net/',
        'lolalytics': 'https://lolalytics.com/'
    },
    
    # Советы для профиля
    'profile_tips': [
        'Укажи свой Summoner Name и сервер',
        'Напиши мейн роли и чемпионов',
        'Укажи текущий и целевой ранг',
        'Опиши стиль игры и предпочтения',
        'Укажи когда обычно играешь',
        'Добавь ссылку на op.gg профиль',
        'Укажи опыт игры и достижения'
    ]
}

