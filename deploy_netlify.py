#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Развертывание TeammatesFinder на Netlify
Бесплатный HTTPS хостинг
"""

import os
import json
import shutil
import zipfile

def create_netlify_version():
    """Создать версию для Netlify"""
    
    print("🚀 Создаем версию для Netlify...")
    
    # Создаем папку для деплоя
    if os.path.exists('netlify-deploy'):
        shutil.rmtree('netlify-deploy')
    os.makedirs('netlify-deploy')
    
    # Копируем фронтенд файлы
    shutil.copytree('frontend', 'netlify-deploy', dirs_exist_ok=True)
    
    # Создаем автономное приложение
    create_standalone_app_netlify()
    
    # Создаем ZIP для загрузки
    create_deployment_zip()
    
    print("✅ Версия для Netlify готова!")
    print("")
    print("📋 ИНСТРУКЦИИ ПО ДЕПЛОЮ НА NETLIFY:")
    print("1. Иди на https://netlify.com")
    print("2. Зарегистрируйся/войди")
    print("3. Drag & Drop файл 'netlify-deploy.zip' на страницу")
    print("4. Получишь HTTPS URL типа: https://random-name.netlify.app")
    print("5. Укажи этот URL в @BotFather")
    print("")
    print("🎁 БОНУС: Netlify автоматически обновляется при изменениях!")

def create_standalone_app_netlify():
    """Создать автономное приложение для Netlify"""
    
    # Копируем тестовые данные
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
            },
            {
                "user_id": 4,
                "display_name": "MLBBQueen",
                "age_group": "21-25",
                "bio": "Mobile Legends фанатка! Mythic ранг. Ищу команду для турниров.",
                "games": [
                    {"name": "Mobile Legends", "emoji": "⚔️", "skill_level": "Профи"}
                ],
                "play_times": ["Вечером", "Выходные"],
                "looking_for": "Команда",
                "contacts": {"discord": "MLBBQueen#1111"}
            },
            {
                "user_id": 5,
                "display_name": "LoLMaster",
                "age_group": "24-28",
                "bio": "League of Legends Diamond. Играю на всех ролях, предпочитаю ADC.",
                "games": [
                    {"name": "League of Legends", "emoji": "⚡", "skill_level": "Опытный"}
                ],
                "play_times": ["Вечером", "Ночью"],
                "looking_for": "Дуо",
                "contacts": {"discord": "LoLMaster#2222"}
            }
        ]
    }
    
    # Сохраняем данные
    with open('netlify-deploy/data.js', 'w', encoding='utf-8') as f:
        f.write(f'window.TEST_DATA = {json.dumps(test_data, ensure_ascii=False, indent=2)};')
    
    # Создаем улучшенную версию приложения
    create_enhanced_app_js()
    
    # Обновляем HTML
    update_html_for_netlify()

def create_enhanced_app_js():
    """Создать улучшенную версию приложения"""
    
    app_js = '''
// TeammatesFinder - Улучшенная автономная версия

class TeammatesFinder {
    constructor() {
        this.currentUser = null;
        this.currentPlayers = window.TEST_DATA?.players || [];
        this.currentPlayerIndex = 0;
        this.matches = JSON.parse(localStorage.getItem('matches') || '[]');
        this.viewedPlayers = JSON.parse(localStorage.getItem('viewedPlayers') || '[]');
        this.init();
    }
    
    init() {
        console.log('🎮 TeammatesFinder запущен!');
        
        // Инициализация Telegram WebApp
        if (window.Telegram?.WebApp) {
            window.Telegram.WebApp.ready();
            window.Telegram.WebApp.expand();
        }
        
        this.showScreen('profile-setup');
        this.setupEventListeners();
        this.setupProfileForm();
        this.updateMatchesCount();
    }
    
    setupEventListeners() {
        // Форма профиля
        document.getElementById('profile-form')?.addEventListener('submit', (e) => {
            e.preventDefault();
            this.createProfile();
        });
        
        // Кнопки действий
        document.getElementById('like-btn')?.addEventListener('click', () => this.likePlayer());
        document.getElementById('dislike-btn')?.addEventListener('click', () => this.dislikePlayer());
        document.getElementById('info-btn')?.addEventListener('click', () => this.showPlayerInfo());
        
        // Навигация
        document.getElementById('matches-btn')?.addEventListener('click', () => this.showMatches());
        document.getElementById('back-from-matches')?.addEventListener('click', () => this.showScreen('main-app'));
        document.getElementById('refresh-btn')?.addEventListener('click', () => this.resetAndRestart());
        
        // Модальные окна
        document.querySelectorAll('.modal .close').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.target.closest('.modal').classList.remove('active');
            });
        });
        
        // Свайпы на мобильных
        this.setupSwipeListeners();
        
        // Счетчик символов
        const bioTextarea = document.getElementById('bio');
        const charCounter = document.querySelector('.char-counter');
        if (bioTextarea && charCounter) {
            bioTextarea.addEventListener('input', () => {
                charCounter.textContent = `${bioTextarea.value.length}/200`;
            });
        }
    }
    
    setupSwipeListeners() {
        const cardsContainer = document.getElementById('cards-stack');
        if (!cardsContainer) return;
        
        let startX = 0;
        let currentX = 0;
        let isDragging = false;
        
        const handleStart = (e) => {
            isDragging = true;
            startX = e.touches ? e.touches[0].clientX : e.clientX;
            currentX = startX;
        };
        
        const handleMove = (e) => {
            if (!isDragging) return;
            e.preventDefault();
            
            currentX = e.touches ? e.touches[0].clientX : e.clientX;
            const deltaX = currentX - startX;
            const card = cardsContainer.querySelector('.player-card');
            
            if (card) {
                const rotation = deltaX * 0.1;
                card.style.transform = `translateX(${deltaX}px) rotate(${rotation}deg)`;
                card.style.opacity = Math.max(0.3, 1 - Math.abs(deltaX) / 300);
            }
        };
        
        const handleEnd = () => {
            if (!isDragging) return;
            isDragging = false;
            
            const deltaX = currentX - startX;
            const card = cardsContainer.querySelector('.player-card');
            
            if (Math.abs(deltaX) > 100) {
                if (deltaX > 0) {
                    this.likePlayer();
                } else {
                    this.dislikePlayer();
                }
            } else if (card) {
                // Возвращаем карточку обратно
                card.style.transform = '';
                card.style.opacity = '';
            }
        };
        
        cardsContainer.addEventListener('touchstart', handleStart, { passive: true });
        cardsContainer.addEventListener('touchmove', handleMove, { passive: false });
        cardsContainer.addEventListener('touchend', handleEnd, { passive: true });
        
        cardsContainer.addEventListener('mousedown', handleStart);
        cardsContainer.addEventListener('mousemove', handleMove);
        cardsContainer.addEventListener('mouseup', handleEnd);
        cardsContainer.addEventListener('mouseleave', handleEnd);
    }
    
    setupProfileForm() {
        const gamesContainer = document.getElementById('games-selector');
        if (!gamesContainer) return;
        
        const games = [
            { name: 'Counter-Strike 2', emoji: '🔫' },
            { name: 'Valorant', emoji: '⚡' },
            { name: 'Dota 2', emoji: '🔴' },
            { name: 'League of Legends', emoji: '⚡' },
            { name: 'Mobile Legends', emoji: '⚔️' },
            { name: 'Minecraft', emoji: '🟫' },
            { name: 'Among Us', emoji: '🚀' }
        ];
        
        gamesContainer.innerHTML = games.map(game => 
            `<div class="game-option" data-game="${game.name}">
                ${game.emoji} ${game.name}
            </div>`
        ).join('');
        
        gamesContainer.addEventListener('click', (e) => {
            if (e.target.classList.contains('game-option')) {
                e.target.classList.toggle('selected');
            }
        });
    }
    
    createProfile() {
        const formData = new FormData(document.getElementById('profile-form'));
        const selectedGames = Array.from(document.querySelectorAll('.game-option.selected'))
            .map(el => el.dataset.game);
        
        this.currentUser = {
            display_name: document.getElementById('display-name').value,
            age_group: document.getElementById('age-group').value,
            bio: document.getElementById('bio').value,
            games: selectedGames,
            looking_for: document.getElementById('looking-for').value,
            discord: document.getElementById('discord').value
        };
        
        if (!this.currentUser.display_name || !this.currentUser.age_group || 
            !this.currentUser.bio || selectedGames.length === 0) {
            this.showNotification('Пожалуйста, заполните все поля!', 'error');
            return;
        }
        
        localStorage.setItem('userProfile', JSON.stringify(this.currentUser));
        this.showNotification('Профиль создан успешно!', 'success');
        
        setTimeout(() => {
            this.showScreen('main-app');
            this.showNextPlayer();
        }, 1000);
    }
    
    showNextPlayer() {
        // Фильтруем уже просмотренных игроков
        const availablePlayers = this.currentPlayers.filter(p => 
            !this.viewedPlayers.includes(p.user_id)
        );
        
        if (availablePlayers.length === 0) {
            this.showNoMorePlayers();
            return;
        }
        
        // Выбираем случайного игрока
        const randomIndex = Math.floor(Math.random() * availablePlayers.length);
        const player = availablePlayers[randomIndex];
        
        this.displayPlayer(player);
    }
    
    displayPlayer(player) {
        const cardsContainer = document.getElementById('cards-stack');
        if (!cardsContainer) return;
        
        cardsContainer.innerHTML = '';
        
        const gamesHtml = player.games.map(game => 
            `<span class="game-tag">${game.emoji} ${game.name} (${game.skill_level})</span>`
        ).join('');
        
        const playTimes = player.play_times.join(', ');
        
        const cardHtml = `
            <div class="player-card fade-in" data-player-id="${player.user_id}">
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
                            <span class="detail-icon">💬</span>
                            <span>Предпочитает ${player.looking_for.toLowerCase()}</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        cardsContainer.innerHTML = cardHtml;
        document.getElementById('no-cards')?.classList.add('hidden');
    }
    
    likePlayer() {
        const card = document.querySelector('.player-card');
        if (!card) return;
        
        const playerId = parseInt(card.dataset.playerId);
        const player = this.currentPlayers.find(p => p.user_id === playerId);
        
        if (!player) return;
        
        this.viewedPlayers.push(playerId);
        localStorage.setItem('viewedPlayers', JSON.stringify(this.viewedPlayers));
        
        // Симулируем мэтч (30% шанс)
        if (Math.random() < 0.3) {
            this.matches.push(player);
            localStorage.setItem('matches', JSON.stringify(this.matches));
            this.showMatch(player);
        } else {
            this.showNotification('❤️ Лайк отправлен!', 'success');
        }
        
        this.animateCardRemoval(card, 'right');
    }
    
    dislikePlayer() {
        const card = document.querySelector('.player-card');
        if (!card) return;
        
        const playerId = parseInt(card.dataset.playerId);
        
        this.viewedPlayers.push(playerId);
        localStorage.setItem('viewedPlayers', JSON.stringify(this.viewedPlayers));
        
        this.animateCardRemoval(card, 'left');
    }
    
    animateCardRemoval(card, direction) {
        const translateX = direction === 'right' ? '100%' : '-100%';
        const rotate = direction === 'right' ? '30deg' : '-30deg';
        
        card.style.transform = `translateX(${translateX}) rotate(${rotate})`;
        card.style.opacity = '0';
        
        setTimeout(() => {
            this.showNextPlayer();
        }, 300);
    }
    
    showMatch(player) {
        this.updateMatchesCount();
        
        const notification = document.getElementById('match-notification');
        if (notification) {
            notification.querySelector('.match-content').innerHTML = `
                <h3>🎉 Это мэтч!</h3>
                <p>У вас взаимный лайк с <strong>${player.display_name}</strong>!</p>
                <div style="margin: 15px 0;">
                    <strong>Контакты:</strong><br>
                    ${player.contacts.discord ? `Discord: ${player.contacts.discord}` : ''}
                    ${player.contacts.steam ? `<br>Steam: ${player.contacts.steam}` : ''}
                </div>
                <button class="btn btn-primary" onclick="this.closest('.match-notification').classList.remove('show')">
                    Отлично! 🎉
                </button>
            `;
            
            notification.classList.add('show');
            
            setTimeout(() => {
                notification.classList.remove('show');
            }, 8000);
        }
    }
    
    showMatches() {
        const matchesList = document.getElementById('matches-list');
        if (!matchesList) return;
        
        if (this.matches.length === 0) {
            matchesList.innerHTML = `
                <div style="text-align: center; padding: 40px 20px;">
                    <h3>💔 Пока нет мэтчей</h3>
                    <p>Продолжай свайпать, чтобы найти тиммейтов!</p>
                    <button class="btn btn-primary" onclick="app.showScreen('main-app')">
                        Вернуться к поиску
                    </button>
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
                        <div style="margin-top: 8px; font-size: 0.85rem; color: var(--secondary-text-color);">
                            ${match.contacts.discord ? `Discord: ${match.contacts.discord}` : 'Контакты скрыты'}
                            ${match.contacts.steam ? `<br>Steam: ${match.contacts.steam}` : ''}
                        </div>
                    </div>
                </div>
            `).join('');
        }
        
        this.showScreen('matches-screen');
    }
    
    showPlayerInfo() {
        const card = document.querySelector('.player-card');
        if (!card) return;
        
        const playerId = parseInt(card.dataset.playerId);
        const player = this.currentPlayers.find(p => p.user_id === playerId);
        
        if (!player) return;
        
        const gamesInfo = player.games.map(g => `${g.emoji} ${g.name} (${g.skill_level})`).join('\\n');
        
        alert(`📋 Подробная информация\\n\\n` +
              `🎮 ${player.display_name}\\n` +
              `👥 ${player.age_group}\\n` +
              `🎯 Ищет: ${player.looking_for}\\n\\n` +
              `📝 О себе:\\n${player.bio}\\n\\n` +
              `🎮 Игры:\\n${gamesInfo}\\n\\n` +
              `🕐 Время игры: ${player.play_times.join(', ')}`);
    }
    
    showNoMorePlayers() {
        document.getElementById('no-cards')?.classList.remove('hidden');
    }
    
    resetAndRestart() {
        localStorage.removeItem('viewedPlayers');
        localStorage.removeItem('matches');
        this.viewedPlayers = [];
        this.matches = [];
        this.updateMatchesCount();
        this.showNextPlayer();
        this.showNotification('🔄 Список игроков обновлен!', 'success');
    }
    
    updateMatchesCount() {
        const counter = document.getElementById('matches-count');
        if (counter) {
            counter.textContent = this.matches.length;
        }
    }
    
    showNotification(message, type = 'info') {
        // Простое уведомление
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
    
    showScreen(screenId) {
        document.querySelectorAll('.screen').forEach(screen => {
            screen.classList.remove('active');
        });
        
        document.getElementById(screenId)?.classList.add('active');
    }
}

// Запуск приложения
document.addEventListener('DOMContentLoaded', () => {
    window.app = new TeammatesFinder();
});
'''
    
    with open('netlify-deploy/js/app.js', 'w', encoding='utf-8') as f:
        f.write(app_js)

def update_html_for_netlify():
    """Обновить HTML для Netlify"""
    
    # Читаем существующий HTML
    with open('netlify-deploy/index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Добавляем мета-теги для лучшей поддержки
    updated_html = html_content.replace(
        '<title>TeammatesFinder</title>',
        '''<title>TeammatesFinder - Найди тиммейтов для игр</title>
    <meta name="description" content="Telegram Mini App для поиска тиммейтов по играм. Tinder для геймеров!">
    <meta property="og:title" content="TeammatesFinder">
    <meta property="og:description" content="Найди идеальных тиммейтов для твоих любимых игр">
    <meta property="og:type" content="website">'''
    )
    
    with open('netlify-deploy/index.html', 'w', encoding='utf-8') as f:
        f.write(updated_html)

def create_deployment_zip():
    """Создать ZIP файл для развертывания"""
    
    with zipfile.ZipFile('netlify-deploy.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('netlify-deploy'):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, 'netlify-deploy')
                zipf.write(file_path, arc_path)
    
    print("📦 Создан файл: netlify-deploy.zip")

if __name__ == '__main__':
    create_netlify_version()
