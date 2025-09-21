// API клиент для TeammatesFinder

class API {
    constructor() {
        this.baseURL = CONFIG.API_BASE_URL;
        this.headers = this.getHeaders();
    }
    
    getHeaders() {
        const headers = {
            'Content-Type': 'application/json'
        };
        
        // Добавляем данные пользователя Telegram
        if (CONFIG.TELEGRAM_APP?.initDataUnsafe?.user) {
            const user = CONFIG.TELEGRAM_APP.initDataUnsafe.user;
            headers['X-Telegram-User-ID'] = user.id;
            headers['X-Telegram-Username'] = user.username || '';
            headers['X-Telegram-First-Name'] = user.first_name || '';
        } else if (CONFIG.DEBUG) {
            // Тестовые данные для разработки
            headers['X-Telegram-User-ID'] = '123456789';
            headers['X-Telegram-Username'] = 'test_user';
            headers['X-Telegram-First-Name'] = 'Test';
        }
        
        return headers;
    }
    
    async request(endpoint, options = {}) {
        try {
            const url = `${this.baseURL}${endpoint}`;
            const config = {
                headers: this.headers,
                ...options
            };
            
            log(`API Request: ${config.method || 'GET'} ${url}`);
            
            const response = await fetch(url, config);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || `HTTP ${response.status}`);
            }
            
            log(`API Response:`, data);
            return data;
            
        } catch (error) {
            logError(`API Error:`, error);
            throw error;
        }
    }
    
    // Проверка здоровья API
    async health() {
        return this.request('/health');
    }
    
    // Получить список игр
    async getGames() {
        return this.request('/games');
    }
    
    // Получить профиль пользователя
    async getUserProfile() {
        return this.request('/user/profile');
    }
    
    // Создать профиль пользователя
    async createProfile(profileData) {
        return this.request('/user/profile', {
            method: 'POST',
            body: JSON.stringify(profileData)
        });
    }
    
    // Получить следующего игрока
    async getNextPlayer() {
        return this.request('/players/next');
    }
    
    // Взаимодействие с игроком (лайк/дизлайк)
    async interactWithPlayer(targetUserId, interactionType) {
        return this.request('/players/interact', {
            method: 'POST',
            body: JSON.stringify({
                target_user_id: targetUserId,
                interaction_type: interactionType
            })
        });
    }
    
    // Получить мэтчи пользователя
    async getUserMatches() {
        return this.request('/matches');
    }
}

// Создаем глобальный экземпляр API
const api = new API();

