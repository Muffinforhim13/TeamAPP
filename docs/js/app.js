
// Автономная версия TeammatesFinder для GitHub Pages

class StandaloneApp {
    constructor() {
        this.currentUser = null;
        this.currentPlayers = window.TEST_DATA.players || [];
        this.currentPlayerIndex = 0;
        this.matches = [];
        this.init();
    }
    
    init() {
        console.log('Запуск автономной версии TeammatesFinder...');
        
        // Скрываем экран загрузки
        this.showScreen('profile-setup');
        
        // Настраиваем обработчики
        this.setupEventListeners();
        this.setupProfileForm();
    }
    
    setupEventListeners() {
        // Форма профиля
        document.getElementById('profile-form')?.addEventListener('submit', (e) => {
            e.preventDefault();
            this.createProfile();
        });
        
        // Кнопки действий
        document.getElementById('like-btn')?.addEventListener('click', () => {
            this.likePlayer();
        });
        
        document.getElementById('dislike-btn')?.addEventListener('click', () => {
            this.dislikePlayer();
        });
        
        document.getElementById('info-btn')?.addEventListener('click', () => {
            this.showPlayerInfo();
        });
        
        // Навигация
        document.getElementById('matches-btn')?.addEventListener('click', () => {
            this.showMatches();
        });
        
        document.getElementById('back-from-matches')?.addEventListener('click', () => {
            this.showScreen('main-app');
        });
        
        // Модальные окна
        document.querySelectorAll('.modal .close').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.target.closest('.modal').classList.remove('active');
            });
        });
    }
    
    setupProfileForm() {
        // Простая настройка игр
        const gamesContainer = document.getElementById('games-selector');
        if (gamesContainer) {
            const games = ['Counter-Strike 2', 'Valorant', 'Dota 2', 'League of Legends', 'Mobile Legends'];
            
            gamesContainer.innerHTML = games.map(game => 
                `<div class="game-option" data-game="${game}">${game}</div>`
            ).join('');
            
            gamesContainer.addEventListener('click', (e) => {
                if (e.target.classList.contains('game-option')) {
                    e.target.classList.toggle('selected');
                }
            });
        }
    }
    
    createProfile() {
        const formData = new FormData(document.getElementById('profile-form'));
        const selectedGames = Array.from(document.querySelectorAll('.game-option.selected'))
            .map(el => el.dataset.game);
        
        this.currentUser = {
            display_name: formData.get('display-name') || document.getElementById('display-name').value,
            age_group: formData.get('age-group') || document.getElementById('age-group').value,
            bio: formData.get('bio') || document.getElementById('bio').value,
            games: selectedGames,
            looking_for: formData.get('looking-for') || document.getElementById('looking-for').value,
            discord: formData.get('discord') || document.getElementById('discord').value
        };
        
        if (!this.currentUser.display_name || !this.currentUser.age_group || 
            !this.currentUser.bio || selectedGames.length === 0) {
            alert('Пожалуйста, заполните все поля!');
            return;
        }
        
        console.log('Профиль создан:', this.currentUser);
        this.showScreen('main-app');
        this.showNextPlayer();
    }
    
    showNextPlayer() {
        if (this.currentPlayerIndex >= this.currentPlayers.length) {
            this.showNoMorePlayers();
            return;
        }
        
        const player = this.currentPlayers[this.currentPlayerIndex];
        this.displayPlayer(player);
    }
    
    displayPlayer(player) {
        const cardsContainer = document.getElementById('cards-stack');
        if (!cardsContainer) return;
        
        cardsContainer.innerHTML = '';
        
        const gamesHtml = player.games.map(game => 
            `<span class="game-tag">${game.emoji} ${game.name}</span>`
        ).join('');
        
        const playTimes = player.play_times.join(', ');
        
        const cardHtml = `
            <div class="player-card" data-player-id="${player.user_id}">
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
                    </div>
                </div>
            </div>
        `;
        
        cardsContainer.innerHTML = cardHtml;
    }
    
    likePlayer() {
        const currentPlayer = this.currentPlayers[this.currentPlayerIndex];
        if (!currentPlayer) return;
        
        console.log('Лайк игроку:', currentPlayer.display_name);
        
        // Симулируем мэтч (50% шанс)
        if (Math.random() > 0.5) {
            this.matches.push(currentPlayer);
            this.showMatch(currentPlayer);
        }
        
        this.nextPlayer();
    }
    
    dislikePlayer() {
        console.log('Дизлайк игроку');
        this.nextPlayer();
    }
    
    nextPlayer() {
        this.currentPlayerIndex++;
        
        // Анимация удаления карточки
        const card = document.querySelector('.player-card');
        if (card) {
            card.style.transform = 'translateX(100%) rotate(30deg)';
            card.style.opacity = '0';
            
            setTimeout(() => {
                this.showNextPlayer();
            }, 300);
        } else {
            this.showNextPlayer();
        }
    }
    
    showMatch(player) {
        const notification = document.getElementById('match-notification');
        if (notification) {
            notification.querySelector('.match-content').innerHTML = `
                <h3>🎉 Это мэтч!</h3>
                <p>У вас взаимный лайк с <strong>${player.display_name}</strong>!</p>
                <p>Discord: ${player.contacts.discord || 'Не указан'}</p>
                <button class="btn btn-primary" onclick="this.closest('.match-notification').classList.remove('show')">Отлично!</button>
            `;
            
            notification.classList.add('show');
            
            setTimeout(() => {
                notification.classList.remove('show');
            }, 5000);
        }
        
        // Обновляем счетчик мэтчей
        document.getElementById('matches-count').textContent = this.matches.length;
    }
    
    showMatches() {
        const matchesList = document.getElementById('matches-list');
        if (!matchesList) return;
        
        if (this.matches.length === 0) {
            matchesList.innerHTML = `
                <div style="text-align: center; padding: 40px 20px;">
                    <h3>💔 Пока нет мэтчей</h3>
                    <p>Продолжай свайпать!</p>
                </div>
            `;
        } else {
            matchesList.innerHTML = this.matches.map(match => `
                <div class="match-item">
                    <div class="match-avatar">
                        ${match.display_name.charAt(0).toUpperCase()}
                    </div>
                    <div class="match-info">
                        <div class="match-name">${match.display_name}</div>
                        <div class="match-games">
                            ${match.games.map(g => g.emoji).join(' ')} 
                            ${match.games.map(g => g.name).slice(0, 2).join(', ')}
                        </div>
                        <div style="margin-top: 8px; font-size: 0.85rem;">
                            Discord: ${match.contacts.discord || 'Не указан'}
                        </div>
                    </div>
                </div>
            `).join('');
        }
        
        this.showScreen('matches-screen');
    }
    
    showPlayerInfo() {
        const currentPlayer = this.currentPlayers[this.currentPlayerIndex];
        if (!currentPlayer) return;
        
        alert(`Информация об игроке: ${currentPlayer.display_name}\n\n${currentPlayer.bio}\n\nКонтакты: ${currentPlayer.contacts.discord || 'Не указаны'}`);
    }
    
    showNoMorePlayers() {
        document.getElementById('no-cards')?.classList.remove('hidden');
    }
    
    showScreen(screenId) {
        document.querySelectorAll('.screen').forEach(screen => {
            screen.classList.remove('active');
        });
        
        document.getElementById(screenId)?.classList.add('active');
    }
}

// Запуск приложения
document.addEventListener('DOMContentLoaded', () => {
    window.app = new StandaloneApp();
});
