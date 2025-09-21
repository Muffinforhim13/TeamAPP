// Конфигурация для TeammatesFinder Mini App

const CONFIG = {
    // API endpoints
    API_BASE_URL: window.location.origin + '/api',
    
    // Telegram WebApp
    TELEGRAM_APP: window.Telegram?.WebApp,
    
    // Настройки свайпов
    SWIPE: {
        MIN_DISTANCE: 50,        // Минимальная дистанция для свайпа
        MIN_VELOCITY: 0.3,       // Минимальная скорость свайпа
        THRESHOLD: 100,          // Порог для автоматического свайпа
        ANIMATION_DURATION: 300  // Длительность анимации
    },
    
    // Игры с эмодзи
    GAMES: {
        'Dota 2': '🔴',
        'Counter-Strike 2': '🔫',
        'Valorant': '⚡',
        'Mobile Legends': '⚔️',
        'League of Legends': '⚡'
    },
    
    // Дебаг режим
    DEBUG: true
};

// Инициализация Telegram WebApp
if (CONFIG.TELEGRAM_APP) {
    CONFIG.TELEGRAM_APP.ready();
    CONFIG.TELEGRAM_APP.expand();
    
    // Применяем тему Telegram
    document.documentElement.style.setProperty('--tg-theme-bg-color', 
        CONFIG.TELEGRAM_APP.themeParams.bg_color || '#F2F2F7');
    document.documentElement.style.setProperty('--tg-theme-text-color', 
        CONFIG.TELEGRAM_APP.themeParams.text_color || '#000000');
    document.documentElement.style.setProperty('--tg-theme-secondary-bg-color', 
        CONFIG.TELEGRAM_APP.themeParams.secondary_bg_color || '#FFFFFF');
}

// Логирование
const log = (...args) => {
    if (CONFIG.DEBUG) {
        console.log('[TeammatesFinder]', ...args);
    }
};

const logError = (...args) => {
    console.error('[TeammatesFinder Error]', ...args);
};

