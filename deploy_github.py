#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Развертывание TeammatesFinder на GitHub Pages
Создает статическую версию для Mini App
"""

import os
import json
import shutil

def create_static_version():
    """Создать статическую версию для GitHub Pages"""
    
    print("🚀 Создаем статическую версию для GitHub Pages...")
    
    # Создаем папку для деплоя
    if os.path.exists('docs'):
        shutil.rmtree('docs')
    os.makedirs('docs')
    
    # Копируем фронтенд файлы
    shutil.copytree('frontend', 'docs', dirs_exist_ok=True)
    
    # Создаем простую версию без backend
    create_standalone_app()
    
    print("✅ Статическая версия создана в папке 'docs'")
    print("")
    print("📋 ИНСТРУКЦИИ ПО ДЕПЛОЮ:")
    print("1. Создай репозиторий на GitHub")
    print("2. Загрузи все файлы")
    print("3. Зайди в Settings → Pages")
    print("4. Source: Deploy from a branch")
    print("5. Branch: main")
    print("6. Folder: /docs")
    print("7. Получишь URL: https://username.github.io/repository")
    print("8. Укажи этот URL в @BotFather")

def create_standalone_app():
    """Создать автономное приложение без backend"""
    
    # Простые тестовые данные
    test_data = {
        "players": [
            {
                "user_id": 1,
                "display_name": "ProGamer2024",
                "age_group": "21-25",
                "bio": "Ищу команду для CS2 и Valorant. Играю на высоком уровне, общительный.",
                "games": [
                    {"name": "Counter-Strike 2", "emoji": "🔫", "skill_level": "Профи"},
                    {"name": "Valorant", "emoji": "⚡", "skill_level": "Опытный"}
                ],
                "play_times": ["Вечером", "Выходные"],
                "looking_for": "Команда",
                "contacts": {"discord": "ProGamer#1234"}
            },
            {
                "user_id": 2,
                "display_name": "CasualGirl",
                "age_group": "18-25", 
                "bio": "Люблю играть в Minecraft и Among Us. Ищу дружескую компанию для совместных игр.",
                "games": [
                    {"name": "Minecraft", "emoji": "🟫", "skill_level": "Любитель"},
                    {"name": "Among Us", "emoji": "🚀", "skill_level": "Опытный"}
                ],
                "play_times": ["Днем", "Вечером"],
                "looking_for": "Компания",
                "contacts": {"discord": "CasualGirl#5678"}
            },
            {
                "user_id": 3,
                "display_name": "DotaKing",
                "age_group": "26-30",
                "bio": "Играю в Dota 2 уже 8 лет. Ancient ранг. Ищу постоянную команду для катки.",
                "games": [
                    {"name": "Dota 2", "emoji": "🔴", "skill_level": "Профи"}
                ],
                "play_times": ["Вечером", "Ночью"],
                "looking_for": "Команда",
                "contacts": {"discord": "DotaKing#9999", "steam": "dotaking"}
            }
        ]
    }
    
    # Сохраняем тестовые данные
    with open('docs/data.js', 'w', encoding='utf-8') as f:
        f.write(f'window.TEST_DATA = {json.dumps(test_data, ensure_ascii=False, indent=2)};')
    
    # Создаем упрощенную версию app.js
    standalone_js = '''
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
        
        alert(`Информация об игроке: ${currentPlayer.display_name}\\n\\n${currentPlayer.bio}\\n\\nКонтакты: ${currentPlayer.contacts.discord || 'Не указаны'}`);
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
'''
    
    # Перезаписываем app.js
    with open('docs/js/app.js', 'w', encoding='utf-8') as f:
        f.write(standalone_js)
    
    # Обновляем index.html для автономной версии
    update_index_html()

def update_index_html():
    """Обновить index.html для автономной работы"""
    
    html_content = '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>TeammatesFinder</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <!-- Экран создания профиля -->
    <div id="profile-setup" class="screen active">
        <div class="container">
            <h2>🎮 Создай свой профиль</h2>
            <form id="profile-form">
                <div class="form-group">
                    <label>Игровой ник:</label>
                    <input type="text" id="display-name" placeholder="Твой ник в играх" required>
                </div>
                
                <div class="form-group">
                    <label>Возраст:</label>
                    <select id="age-group" required>
                        <option value="">Выбери возраст</option>
                        <option value="16-20">16-20</option>
                        <option value="21-25">21-25</option>
                        <option value="26-30">26-30</option>
                        <option value="31-35">31-35</option>
                        <option value="36+">36+</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>О себе:</label>
                    <textarea id="bio" placeholder="Расскажи о себе, стиле игры, целях..." maxlength="200"></textarea>
                </div>
                
                <div class="form-group">
                    <label>Основные игры:</label>
                    <div id="games-selector" class="games-grid">
                        <!-- Игры добавятся через JS -->
                    </div>
                </div>
                
                <div class="form-group">
                    <label>Что ищешь:</label>
                    <select id="looking-for" required>
                        <option value="">Выбери цель</option>
                        <option value="Команда">🏆 Команда для рейтинга</option>
                        <option value="Дуо">👥 Напарник для дуо</option>
                        <option value="Компания">😄 Компания для фана</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>Discord:</label>
                    <input type="text" id="discord" placeholder="Username#1234">
                </div>
                
                <button type="submit" class="btn btn-primary">
                    Создать профиль 🚀
                </button>
            </form>
        </div>
    </div>

    <!-- Главный экран со свайпами -->
    <div id="main-app" class="screen">
        <header class="app-header">
            <h1>🎮 TeammatesFinder</h1>
            <div class="header-actions">
                <button id="matches-btn" class="icon-btn">
                    <span class="icon">💕</span>
                    <span class="badge" id="matches-count">0</span>
                </button>
            </div>
        </header>

        <div class="cards-container">
            <div id="cards-stack">
                <!-- Карточки игроков -->
            </div>
            
            <div id="no-cards" class="no-cards hidden">
                <div class="no-cards-content">
                    <h3>🎉 Все игроки просмотрены!</h3>
                    <p>Это демо версия TeammatesFinder</p>
                </div>
            </div>
        </div>

        <div class="action-buttons">
            <button id="dislike-btn" class="action-btn dislike">
                <span class="icon">❌</span>
            </button>
            <button id="info-btn" class="action-btn info">
                <span class="icon">ℹ️</span>
            </button>
            <button id="like-btn" class="action-btn like">
                <span class="icon">❤️</span>
            </button>
        </div>
    </div>

    <!-- Экран мэтчей -->
    <div id="matches-screen" class="screen">
        <header class="screen-header">
            <button id="back-from-matches" class="back-btn">← Назад</button>
            <h2>💕 Твои мэтчи</h2>
        </header>
        <div class="container">
            <div id="matches-list"></div>
        </div>
    </div>

    <!-- Уведомление о мэтче -->
    <div id="match-notification" class="match-notification">
        <div class="match-content">
            <h3>🎉 Это мэтч!</h3>
            <p>У вас взаимный лайк!</p>
        </div>
    </div>

    <script src="data.js"></script>
    <script src="js/app.js"></script>
</body>
</html>'''
    
    with open('docs/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == '__main__':
    create_static_version()
