// Главное приложение TeammatesFinder

class TeammatesFinderApp {
    constructor() {
        this.currentUser = null;
        this.currentPlayers = [];
        this.swiper = null;
        this.matches = [];
        this.selectedGames = [];
        
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
        
        document.getElementById('back-from-matches')?.addEventListener('click', () => {
            this.showScreen('main-app');
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
    
    async initializeProfileForm() {
        try {
            // Загружаем список игр
            const gamesData = await api.getGames();
            const gamesContainer = document.getElementById('games-selector');
            
            if (gamesContainer && gamesData.games) {
                gamesContainer.innerHTML = '';
                
                gamesData.games.forEach(game => {
                    const gameElement = document.createElement('div');
                    gameElement.className = 'game-option';
                    gameElement.innerHTML = `${game.emoji} ${game.name}`;
                    gameElement.dataset.gameName = game.name;
                    
                    gameElement.addEventListener('click', () => {
                        this.toggleGameSelection(gameElement);
                    });
                    
                    gamesContainer.appendChild(gameElement);
                });
            }
        } catch (error) {
            logError('Failed to load games:', error);
        }
    }
    
    toggleGameSelection(gameElement) {
        const gameName = gameElement.dataset.gameName;
        
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
                await this.loadPlayers();
                await this.loadMatches();
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
            const formData = new FormData(document.getElementById('profile-form'));
            
            const profileData = {
                display_name: formData.get('display-name') || document.getElementById('display-name').value,
                age_group: formData.get('age-group') || document.getElementById('age-group').value,
                bio: formData.get('bio') || document.getElementById('bio').value,
                preferred_games: this.selectedGames,
                looking_for: formData.get('looking-for') || document.getElementById('looking-for').value,
                discord_tag: formData.get('discord') || document.getElementById('discord').value,
                skill_levels: {}, // TODO: добавить выбор уровней для каждой игры
                play_times: ['Вечером'] // TODO: добавить выбор времени игры
            };
            
            // Валидация
            if (!profileData.display_name || !profileData.age_group || !profileData.bio || 
                !profileData.looking_for || this.selectedGames.length === 0) {
                this.showError('Пожалуйста, заполните все обязательные поля');
                return;
            }
            
            this.showLoading();
            
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
        const cardsContainer = document.getElementById('cards-stack');
        if (!cardsContainer) return;
        
        const cardElement = this.createPlayerCard(player);
        cardsContainer.appendChild(cardElement);
        
        // Добавляем анимацию появления
        setTimeout(() => {
            cardElement.classList.add('fade-in');
        }, 100);
        
        log('Added player card:', player.display_name);
    }
    
    createPlayerCard(player) {
        const card = document.createElement('div');
        card.className = 'player-card';
        card.dataset.userId = player.user_id;
        
        // Форматируем игры
        const gamesHtml = player.games.map(game => 
            `<span class="game-tag">${game.emoji} ${game.name}</span>`
        ).join('');
        
        // Форматируем детали
        const playTimes = player.play_times.join(', ');
        
        card.innerHTML = `
            <div class="swipe-indicator like">❤️</div>
            <div class="swipe-indicator dislike">❌</div>
            
            <div class="card-header">
                <div class="player-name">${player.display_name}</div>
                <div class="player-meta">${player.age_group} • ${player.looking_for}</div>
                <div class="player-games">${gamesHtml}</div>
            </div>
            
            <div class="card-body">
                <div class="player-bio">${player.bio}</div>
                
                <div class="player-details">
                    <div class="detail-row">
                        <span class="detail-icon">🕐</span>
                        <span>Играет ${playTimes}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-icon">🌍</span>
                        <span>${player.language}</span>
                    </div>
                </div>
            </div>
        `;
        
        return card;
    }
    
    async handlePlayerInteraction(userId, interactionType) {
        try {
            const result = await api.interactWithPlayer(parseInt(userId), interactionType);
            
            if (result.is_match) {
                this.showMatchNotification(result.match_partner);
                await this.loadMatches(); // Обновляем список мэтчей
            }
            
            // Загружаем следующего игрока
            setTimeout(() => {
                this.loadNextPlayer();
            }, 500);
            
        } catch (error) {
            logError('Failed to handle player interaction:', error);
        }
    }
    
    async loadNextPlayer() {
        try {
            const playerData = await api.getNextPlayer();
            
            if (playerData.player) {
                this.addPlayerCard(playerData.player);
            } else {
                const remainingCards = document.querySelectorAll('.player-card');
                if (remainingCards.length === 0) {
                    this.showNoMoreCards();
                }
            }
            
        } catch (error) {
            logError('Failed to load next player:', error);
        }
    }
    
    showMatchNotification(partner) {
        const notification = document.getElementById('match-notification');
        if (notification && partner) {
            // Обновляем содержимое уведомления
            const content = notification.querySelector('.match-content');
            if (content) {
                content.innerHTML = `
                    <h3>🎉 Это мэтч!</h3>
                    <p>У вас взаимный лайк с <strong>${partner.display_name}</strong>!</p>
                    <button id="view-match" class="btn btn-primary">Посмотреть контакты</button>
                `;
                
                // Обработчик для кнопки
                content.querySelector('#view-match').addEventListener('click', () => {
                    notification.classList.remove('show');
                    this.showMatches();
                });
            }
            
            notification.classList.add('show');
            
            // Автоматически скрываем через 5 секунд
            setTimeout(() => {
                notification.classList.remove('show');
            }, 5000);
        }
    }
    
    async loadMatches() {
        try {
            const matchesData = await api.getUserMatches();
            this.matches = matchesData.matches || [];
            
            // Обновляем счетчик мэтчей
            const matchesCount = document.getElementById('matches-count');
            if (matchesCount) {
                matchesCount.textContent = this.matches.length;
            }
            
        } catch (error) {
            logError('Failed to load matches:', error);
        }
    }
    
    showMatches() {
        const matchesList = document.getElementById('matches-list');
        if (!matchesList) return;
        
        if (this.matches.length === 0) {
            matchesList.innerHTML = `
                <div style="text-align: center; padding: 40px 20px; color: var(--secondary-text-color);">
                    <h3>💔 Пока нет мэтчей</h3>
                    <p>Продолжай свайпать, чтобы найти тиммейтов!</p>
                </div>
            `;
        } else {
            matchesList.innerHTML = this.matches.map(match => `
                <div class="match-item">
                    <div class="match-avatar">
                        ${match.partner_name.charAt(0).toUpperCase()}
                    </div>
                    <div class="match-info">
                        <div class="match-name">${match.partner_name}</div>
                        <div class="match-games">
                            ${match.partner_games.map(game => CONFIG.GAMES[game] || '🎮').join(' ')} 
                            ${match.partner_games.slice(0, 3).join(', ')}
                        </div>
                        ${match.partner_profile?.contacts ? `
                            <div style="margin-top: 8px; font-size: 0.85rem;">
                                ${match.partner_profile.contacts.discord ? `📞 ${match.partner_profile.contacts.discord}` : ''}
                                ${match.partner_profile.contacts.steam ? `🔗 Steam` : ''}
                            </div>
                        ` : ''}
                    </div>
                </div>
            `).join('');
        }
        
        this.showScreen('matches-screen');
    }
    
    showPlayerInfo() {
        const currentCard = document.querySelector('.player-card:last-child');
        if (!currentCard) return;
        
        const userId = currentCard.dataset.userId;
        // TODO: Показать подробную информацию об игроке в модальном окне
        
        log('Show player info for user:', userId);
    }
    
    showProfile() {
        const modal = document.getElementById('profile-modal');
        const profileInfo = document.getElementById('profile-info');
        
        if (modal && profileInfo && this.currentUser) {
            profileInfo.innerHTML = `
                <div style="margin-bottom: 20px;">
                    <h4>${this.currentUser.display_name}</h4>
                    <p style="color: var(--secondary-text-color); margin: 5px 0;">
                        ${this.currentUser.age_group} • ${this.currentUser.looking_for}
                    </p>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <strong>О себе:</strong><br>
                    ${this.currentUser.bio}
                </div>
                
                <div style="margin-bottom: 15px;">
                    <strong>Игры:</strong><br>
                    ${this.currentUser.games?.map(game => `${game.emoji} ${game.name}`).join(', ') || 'Не указаны'}
                </div>
                
                <div>
                    <strong>Время игры:</strong><br>
                    ${this.currentUser.play_times?.join(', ') || 'Не указано'}
                </div>
            `;
            
            modal.classList.add('active');
        }
    }
    
    showNoMoreCards() {
        document.getElementById('no-cards')?.classList.remove('hidden');
    }
    
    showScreen(screenId) {
        // Скрываем все экраны
        document.querySelectorAll('.screen').forEach(screen => {
            screen.classList.remove('active');
        });
        
        // Показываем нужный экран
        const screen = document.getElementById(screenId);
        if (screen) {
            screen.classList.add('active');
        }
        
        log('Showing screen:', screenId);
    }
    
    showLoading() {
        this.showScreen('loading');
    }
    
    hideLoading() {
        // Загрузочный экран скрывается автоматически при показе другого экрана
    }
    
    showError(message) {
        // TODO: Показать toast уведомление об ошибке
        if (CONFIG.TELEGRAM_APP) {
            CONFIG.TELEGRAM_APP.showAlert(message);
        } else {
            alert(message);
        }
        logError('Error shown to user:', message);
    }
    
    showSuccess(message) {
        // TODO: Показать toast уведомление об успехе
        if (CONFIG.TELEGRAM_APP) {
            CONFIG.TELEGRAM_APP.showAlert(message);
        } else {
            alert(message);
        }
        log('Success shown to user:', message);
    }
}

// Инициализируем приложение когда DOM готов
document.addEventListener('DOMContentLoaded', () => {
    window.app = new TeammatesFinderApp();
});

