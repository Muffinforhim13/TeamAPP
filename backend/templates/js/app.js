// Главное приложение TeammatesFinder - Обновленная версия

class TeammatesFinderApp {
    constructor() {
        this.currentUser = null;
        this.currentPlayers = [];
        this.swiper = null;
        this.matches = [];
        this.selectedGames = [];
        this.userPhoto = null;
        
        this.init();
    }
    
    async init() {
        log('Initializing TeammatesFinder App...');
        
        try {
            // Проверяем API
            await api.health();
            log('API connection successful');
            
            // Инициализируем UI
            this.initializeUI();
            
            // Проверяем профиль пользователя
            await this.checkUserProfile();
            
        } catch (error) {
            logError('Failed to initialize app:', error);
            this.showError('Ошибка подключения к серверу');
        }
    }
    
    initializeUI() {
        // Инициализируем swiper
        const cardsContainer = document.getElementById('cards-stack');
        if (cardsContainer) {
            this.swiper = new CardSwiper(cardsContainer);
        }
        
        // Обработчики событий
        this.bindEvents();
        
        // Инициализируем форму профиля  
        this.initializeProfileForm();
        
        log('UI initialized');
    }
    
    bindEvents() {
        // Кнопки действий
        document.getElementById('like-btn')?.addEventListener('click', () => {
            this.swiper?.programmaticSwipeRight();
        });
        
        document.getElementById('dislike-btn')?.addEventListener('click', () => {
            this.swiper?.programmaticSwipeLeft();
        });
        
        document.getElementById('info-btn')?.addEventListener('click', () => {
            this.showPlayerInfo();
        });
        
        // Навигация
        document.getElementById('matches-btn')?.addEventListener('click', () => {
            this.showMatches();
        });
        
        document.getElementById('profile-btn')?.addEventListener('click', () => {
            this.showProfile();
        });
        
        // Главное меню
        document.getElementById('my-profile-card')?.addEventListener('click', () => {
            this.showMyProfile();
        });
        
        document.getElementById('browse-players-card')?.addEventListener('click', () => {
            this.showBrowsePlayers();
        });
        
        document.getElementById('my-matches-card')?.addEventListener('click', () => {
            this.showMatches();
        });
        
        // Кнопки назад
        document.getElementById('back-from-matches')?.addEventListener('click', () => {
            this.showScreen('main-app');
        });
        
        document.getElementById('back-from-profile')?.addEventListener('click', () => {
            this.showScreen('main-app');
        });
        
        document.getElementById('back-from-browse')?.addEventListener('click', () => {
            this.showScreen('main-app');
        });
        
        // Фото загрузка
        document.getElementById('photo-upload-area')?.addEventListener('click', () => {
            document.getElementById('photo-input').click();
        });
        
        document.getElementById('photo-input')?.addEventListener('change', (e) => {
            this.handlePhotoUpload(e);
        });
        
        // Обновление карточек
        document.getElementById('refresh-btn')?.addEventListener('click', () => {
            this.loadPlayers();
        });
        
        // Модальные окна
        this.initializeModals();
        
        // Форма профиля
        document.getElementById('profile-form')?.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleProfileSubmit();
        });
        
        // Счетчик символов в био
        const bioTextarea = document.getElementById('bio');
        const charCounter = document.querySelector('.char-counter');
        if (bioTextarea && charCounter) {
            bioTextarea.addEventListener('input', () => {
                charCounter.textContent = `${bioTextarea.value.length}/200`;
            });
        }
    }
    
    handlePhotoUpload(event) {
        const file = event.target.files[0];
        if (!file) return;
        
        // Проверяем размер файла (макс 5MB)
        if (file.size > 5 * 1024 * 1024) {
            this.showError('Файл слишком большой. Максимум 5MB');
            return;
        }
        
        // Проверяем тип файла
        if (!file.type.startsWith('image/')) {
            this.showError('Выберите изображение');
            return;
        }
        
        const reader = new FileReader();
        reader.onload = (e) => {
            this.userPhoto = e.target.result;
            
            // Показываем превью
            const preview = document.getElementById('preview-photo');
            const placeholder = document.getElementById('upload-placeholder');
            
            if (preview && placeholder) {
                preview.src = this.userPhoto;
                preview.classList.remove('hidden');
                placeholder.style.display = 'none';
            }
        };
        
        reader.readAsDataURL(file);
    }
    
    async initializeProfileForm() {
        // Обработчики для кнопок игр уже есть в HTML
        const gamesContainer = document.getElementById('games-selector');
        if (!gamesContainer) return;
        
        // Добавляем обработчики
        gamesContainer.addEventListener('click', (e) => {
            const gameBtn = e.target.closest('.game-btn');
            if (gameBtn) {
                this.toggleGameSelection(gameBtn);
            }
        });
    }
    
    toggleGameSelection(gameElement) {
        const gameName = gameElement.dataset.game;
        
        if (gameElement.classList.contains('selected')) {
            gameElement.classList.remove('selected');
            this.selectedGames = this.selectedGames.filter(g => g !== gameName);
        } else {
            gameElement.classList.add('selected');
            this.selectedGames.push(gameName);
        }
        
        log('Selected games:', this.selectedGames);
    }
    
    async checkUserProfile() {
        try {
            const profileData = await api.getUserProfile();
            
            if (profileData.has_profile) {
                this.currentUser = profileData.profile;
                this.showScreen('main-app');
                this.updateMatchesCount();
            } else {
                this.showScreen('profile-setup');
            }
            
        } catch (error) {
            logError('Failed to check user profile:', error);
            this.showScreen('profile-setup');
        } finally {
            this.hideLoading();
        }
    }
    
    async handleProfileSubmit() {
        try {
            // Проверяем обязательные поля
            const displayName = document.getElementById('display-name').value;
            const ageGroup = document.getElementById('age-group').value;
            const bio = document.getElementById('bio').value;
            const lookingFor = document.getElementById('looking-for').value;
            const discord = document.getElementById('discord').value;
            
            if (!displayName.trim()) {
                this.showError('Укажите игровой ник');
                return;
            }
            
            if (!ageGroup) {
                this.showError('Выберите возрастную группу');
                return;
            }
            
            if (!lookingFor) {
                this.showError('Выберите что ищете');
                return;
            }
            
            if (this.selectedGames.length === 0) {
                this.showError('Выберите хотя бы одну игру');
                return;
            }
            
            this.showLoading();
            
            const profileData = {
                display_name: displayName.trim(),
                age_group: ageGroup,
                bio: bio.trim() || null,
                preferred_games: this.selectedGames,
                looking_for: lookingFor,
                discord_tag: discord.trim() || null
            };
            
            const result = await api.createProfile(profileData);
            
            if (result.success) {
                this.showSuccess('Профиль создан успешно!');
                this.currentUser = profileData;
                
                setTimeout(() => {
                    this.showScreen('main-app');
                    this.loadPlayers();
                }, 1500);
            }
            
        } catch (error) {
            logError('Failed to create profile:', error);
            this.showError('Ошибка создания профиля');
        } finally {
            this.hideLoading();
        }
    }
    
    showMyProfile() {
        if (!this.currentUser) {
            this.showError('Профиль не найден');
            return;
        }
        
        // Заполняем данные профиля
        document.getElementById('profile-photo-display').src = this.currentUser.photo || '';
        document.getElementById('profile-name-display').textContent = 
            `${this.currentUser.real_name || 'Игрок'}, ${this.currentUser.age || '?'}`;
        document.getElementById('profile-bio-display').textContent = this.currentUser.bio || '';
        document.getElementById('profile-discord-display').textContent = `@${this.currentUser.discord_username}`;
        
        // Заполняем игры
        const gamesList = document.getElementById('profile-games-list');
        if (gamesList && this.currentUser.preferred_games) {
            const mainGames = [
                { name: 'Counter-Strike 2', emoji: '🔫' },
                { name: 'Dota 2', emoji: '🔴' },
                { name: 'Valorant', emoji: '⚡' },
                { name: 'Mobile Legends', emoji: '⚔️' },
                { name: 'League of Legends', emoji: '⚡' }
            ];
            
            gamesList.innerHTML = mainGames.map(game => {
                const isSelected = this.currentUser.preferred_games.includes(game.name);
                return `
                    <div class="game-item ${isSelected ? 'selected' : 'not-selected'}">
                        <span class="game-item-icon">${game.emoji}</span>
                        <div class="game-item-name">${game.name}</div>
                        <div class="game-item-details">${isSelected ? 'Играю' : 'Не играю'}</div>
                    </div>
                `;
            }).join('');
        }
        
        this.showScreen('my-profile-screen');
    }
    
    showBrowsePlayers() {
        this.showScreen('browse-screen');
        this.loadPlayers();
    }
    
    updateMatchesCount() {
        const count = this.matches.length;
        document.getElementById('matches-count').textContent = count;
        document.getElementById('matches-preview').textContent = 
            count > 0 ? `У тебя ${count} мэтч${count === 1 ? '' : count < 5 ? 'а' : 'ей'}!` : 'У тебя 0 мэтчей';
    }
    
    // Остальные методы остаются как в оригинальном app.js
    async loadPlayers() {
        try {
            this.showLoading();
            
            const playersData = await api.getNextPlayer();
            
            if (playersData.player) {
                this.addPlayerCard(playersData.player);
                
                // Загружаем еще несколько карточек
                for (let i = 0; i < 3; i++) {
                    try {
                        const nextPlayer = await api.getNextPlayer();
                        if (nextPlayer.player) {
                            this.addPlayerCard(nextPlayer.player);
                        } else {
                            break;
                        }
                    } catch (error) {
                        break;
                    }
                }
            } else {
                this.showNoMoreCards();
            }
        } catch (error) {
            logError('Failed to load players:', error);
            this.showError('Ошибка загрузки игроков');
        } finally {
            this.hideLoading();
        }
    }

    addPlayerCard(player) {
        const cardsStack = document.getElementById('cards-stack');
        if (!cardsStack) return;

        const card = this.createPlayerCard(player);
        cardsStack.appendChild(card);

        // Добавляем обработчики swipe для этой карточки
        this.swiper?.addCard(card);
    }

    createPlayerCard(player) {
        const card = document.createElement('div');
        card.className = 'player-card';
        card.dataset.playerId = player.user_id;

        const gamesHtml = player.games ? player.games.map(game => 
            `<span class="game-tag">${game.emoji || '🎮'} ${game.name}</span>`
        ).join('') : '';

        card.innerHTML = `
            <div class="card-header">
                <div class="player-photo">
                    <img src="${player.photo || '/default-avatar.png'}" alt="Фото игрока">
                </div>
                <div class="player-info">
                    <div class="player-name">${player.real_name || player.display_name || 'Игрок'}</div>
                    <div class="player-age">${player.age ? `${player.age} лет` : (player.age_group || '')}</div>
                </div>
            </div>
            
            <div class="card-body">
                <div class="player-bio">${player.bio || ''}</div>
                <div class="player-games">${gamesHtml}</div>
                <div class="player-contact">
                    <span class="contact-icon">💬</span>
                    <span>@${player.discord_username || player.discord_tag || 'discord'}</span>
                </div>
            </div>
        `;

        return card;
    }

    showNoMoreCards() {
        document.getElementById('no-cards')?.classList.remove('hidden');
    }

    async loadMatches() {
        try {
            const matchesData = await api.getMatches();
            this.matches = matchesData.matches || [];
            this.updateMatchesCount();
        } catch (error) {
            logError('Failed to load matches:', error);
        }
    }

    showMatches() {
        const matchesList = document.getElementById('matches-list');
        if (!matchesList) return;

        if (this.matches.length === 0) {
            matchesList.innerHTML = `
                <div style="text-align: center; padding: 40px 20px;">
                    <h3>💔 Пока нет мэтчей</h3>
                    <p>Продолжай искать, чтобы найти тиммейтов!</p>
                    <button class="btn btn-primary" onclick="app.showBrowsePlayers()">
                        Искать тиммейтов
                    </button>
                </div>
            `;
        } else {
            matchesList.innerHTML = this.matches.map(match => `
                <div class="match-item">
                    <div class="match-photo">
                        <img src="${match.photo || '/default-avatar.png'}" alt="Фото">
                    </div>
                    <div class="match-info">
                        <div class="match-name">${match.real_name || match.display_name || 'Игрок'}</div>
                        <div class="match-games">
                            ${match.preferred_games ? match.preferred_games.slice(0, 2).join(', ') : ''}
                        </div>
                        <div class="match-contact">@${match.discord_username}</div>
                    </div>
                </div>
            `).join('');
        }

        this.showScreen('matches-screen');
    }

    // Utility methods
    showScreen(screenId) {
        document.querySelectorAll('.screen').forEach(screen => {
            screen.classList.remove('active');
        });

        document.getElementById(screenId)?.classList.add('active');
    }

    showLoading() {
        document.getElementById('loading')?.classList.add('active');
    }

    hideLoading() {
        document.getElementById('loading')?.classList.remove('active');
    }

    showError(message) {
        this.showNotification(message, 'error');
    }

    showSuccess(message) {
        this.showNotification(message, 'success');
    }

    showNotification(message, type = 'info') {
        // Создаем простое уведомление
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'error' ? '#ff4757' : type === 'success' ? '#2ed573' : '#3742fa'};
            color: white;
            padding: 15px 20px;
            border-radius: 10px;
            z-index: 10000;
            font-weight: 600;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            animation: slideIn 0.3s ease;
        `;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    initializeModals() {
        // Закрытие модальных окон
        document.querySelectorAll('.modal .close').forEach(closeBtn => {
            closeBtn.addEventListener('click', (e) => {
                e.target.closest('.modal').classList.remove('active');
            });
        });
        
        // Закрытие по клику вне модального окна
        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    modal.classList.remove('active');
                }
            });
        });
    }

    getTelegramUserId() {
        if (window.Telegram?.WebApp?.initDataUnsafe?.user?.id) {
            return window.Telegram.WebApp.initDataUnsafe.user.id;
        }
        return 'demo_user'; // для тестирования
    }
}

// Инициализация приложения
document.addEventListener('DOMContentLoaded', () => {
    window.app = new TeammatesFinderApp();
});
