// Swiper функциональность для карточек игроков

class CardSwiper {
    constructor(container) {
        this.container = container;
        this.currentCard = null;
        this.isAnimating = false;
        this.startX = 0;
        this.startY = 0;
        this.currentX = 0;
        this.currentY = 0;
        this.isDragging = false;
        
        this.bindEvents();
    }
    
    bindEvents() {
        // Touch события
        this.container.addEventListener('touchstart', this.handleStart.bind(this), { passive: true });
        this.container.addEventListener('touchmove', this.handleMove.bind(this), { passive: false });
        this.container.addEventListener('touchend', this.handleEnd.bind(this), { passive: true });
        
        // Mouse события для десктопа
        this.container.addEventListener('mousedown', this.handleStart.bind(this));
        this.container.addEventListener('mousemove', this.handleMove.bind(this));
        this.container.addEventListener('mouseup', this.handleEnd.bind(this));
        this.container.addEventListener('mouseleave', this.handleEnd.bind(this));
    }
    
    handleStart(e) {
        if (this.isAnimating) return;
        
        this.currentCard = e.target.closest('.player-card');
        if (!this.currentCard) return;
        
        const clientX = e.touches ? e.touches[0].clientX : e.clientX;
        const clientY = e.touches ? e.touches[0].clientY : e.clientY;
        
        this.startX = clientX;
        this.startY = clientY;
        this.currentX = clientX;
        this.currentY = clientY;
        this.isDragging = true;
        
        this.currentCard.classList.add('dragging');
        
        log('Swipe started');
    }
    
    handleMove(e) {
        if (!this.isDragging || !this.currentCard || this.isAnimating) return;
        
        e.preventDefault();
        
        const clientX = e.touches ? e.touches[0].clientX : e.clientX;
        const clientY = e.touches ? e.touches[0].clientY : e.clientY;
        
        this.currentX = clientX;
        this.currentY = clientY;
        
        const deltaX = this.currentX - this.startX;
        const deltaY = this.currentY - this.startY;
        
        // Вычисляем угол поворота
        const rotation = deltaX * 0.1;
        const opacity = 1 - Math.abs(deltaX) / 300;
        
        // Применяем трансформацию
        this.currentCard.style.transform = `translateX(${deltaX}px) translateY(${deltaY}px) rotate(${rotation}deg)`;
        this.currentCard.style.opacity = Math.max(0.3, opacity);
        
        // Показываем индикаторы свайпа
        this.updateSwipeIndicators(deltaX);
    }
    
    handleEnd(e) {
        if (!this.isDragging || !this.currentCard) return;
        
        this.isDragging = false;
        this.currentCard.classList.remove('dragging');
        
        const deltaX = this.currentX - this.startX;
        const deltaY = this.currentY - this.startY;
        const distance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
        const velocity = distance / 100; // Примерная скорость
        
        // Определяем направление свайпа
        if (Math.abs(deltaX) > CONFIG.SWIPE.MIN_DISTANCE && velocity > CONFIG.SWIPE.MIN_VELOCITY) {
            if (deltaX > CONFIG.SWIPE.THRESHOLD) {
                this.swipeRight();
            } else if (deltaX < -CONFIG.SWIPE.THRESHOLD) {
                this.swipeLeft();
            } else {
                this.snapBack();
            }
        } else {
            this.snapBack();
        }
        
        // Убираем индикаторы
        this.hideSwipeIndicators();
        
        log('Swipe ended');
    }
    
    updateSwipeIndicators(deltaX) {
        const likeIndicator = this.currentCard.querySelector('.swipe-indicator.like');
        const dislikeIndicator = this.currentCard.querySelector('.swipe-indicator.dislike');
        
        if (deltaX > 50) {
            likeIndicator?.classList.add('active');
            dislikeIndicator?.classList.remove('active');
        } else if (deltaX < -50) {
            dislikeIndicator?.classList.add('active');
            likeIndicator?.classList.remove('active');
        } else {
            likeIndicator?.classList.remove('active');
            dislikeIndicator?.classList.remove('active');
        }
    }
    
    hideSwipeIndicators() {
        if (this.currentCard) {
            this.currentCard.querySelector('.swipe-indicator.like')?.classList.remove('active');
            this.currentCard.querySelector('.swipe-indicator.dislike')?.classList.remove('active');
        }
    }
    
    swipeRight() {
        if (!this.currentCard) return;
        
        this.isAnimating = true;
        this.currentCard.classList.add('swiped-right');
        
        const userId = this.currentCard.dataset.userId;
        
        setTimeout(() => {
            this.removeCard();
            this.isAnimating = false;
            
            // Отправляем лайк
            if (userId) {
                app.handlePlayerInteraction(userId, 'like');
            }
        }, CONFIG.SWIPE.ANIMATION_DURATION);
        
        log('Swiped right (like)');
    }
    
    swipeLeft() {
        if (!this.currentCard) return;
        
        this.isAnimating = true;
        this.currentCard.classList.add('swiped-left');
        
        const userId = this.currentCard.dataset.userId;
        
        setTimeout(() => {
            this.removeCard();
            this.isAnimating = false;
            
            // Отправляем дизлайк
            if (userId) {
                app.handlePlayerInteraction(userId, 'dislike');
            }
        }, CONFIG.SWIPE.ANIMATION_DURATION);
        
        log('Swiped left (dislike)');
    }
    
    snapBack() {
        if (!this.currentCard) return;
        
        this.currentCard.style.transform = '';
        this.currentCard.style.opacity = '';
        this.currentCard.style.transition = 'transform 0.3s ease, opacity 0.3s ease';
        
        setTimeout(() => {
            if (this.currentCard) {
                this.currentCard.style.transition = '';
            }
        }, 300);
        
        log('Snapped back');
    }
    
    removeCard() {
        if (this.currentCard) {
            this.currentCard.remove();
            this.currentCard = null;
            
            // Проверяем, есть ли еще карточки
            const remainingCards = this.container.querySelectorAll('.player-card');
            if (remainingCards.length === 0) {
                app.showNoMoreCards();
            }
        }
    }
    
    // Программные свайпы для кнопок
    programmaticSwipeLeft() {
        this.currentCard = this.container.querySelector('.player-card:last-child');
        if (this.currentCard) {
            this.swipeLeft();
        }
    }
    
    programmaticSwipeRight() {
        this.currentCard = this.container.querySelector('.player-card:last-child');
        if (this.currentCard) {
            this.swipeRight();
        }
    }
}

