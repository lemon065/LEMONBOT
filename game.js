// Game State
let gameState = {
    lemons: 0,
    energy: 100,
    maxEnergy: 100,
    creatures: [],
    creatureCounter: 0
};

// Creatures Types avec COULEURS DINGUES
const CREATURE_TYPES = [
    { name: 'CITRON EXPLOSIF', emoji: '🍋', petard: '💣', multiplier: 1, color: '#ffff00' },
    { name: 'MEGA BOOM', emoji: '💥', petard: '🎆', multiplier: 1.8, color: '#ff0000' },
    { name: 'ULTRA ZILLA', emoji: '🦖', petard: '💥', multiplier: 2.2, color: '#00ff00' },
    { name: 'CYBER CITRON', emoji: '🤖', petard: '⚡', multiplier: 1.5, color: '#00ffff' },
    { name: 'ARMAGEDDON', emoji: '🌋', petard: '🎇', multiplier: 3, color: '#ff00ff' },
    { name: 'PSYCHO BOMB', emoji: '🎪', petard: '🎉', multiplier: 2.5, color: '#ffaa00' }
];

// Canvas pour les explosions
const canvas = document.getElementById('explosionCanvas');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});

class Particle {
    constructor(x, y, color) {
        this.x = x;
        this.y = y;
        this.vx = (Math.random() - 0.5) * 20;
        this.vy = (Math.random() - 0.5) * 20 - 5;
        this.life = 100;
        this.color = color;
        this.size = Math.random() * 10 + 5;
    }

    update() {
        this.x += this.vx;
        this.y += this.vy;
        this.vy += 0.5;
        this.life -= 2;
    }

    draw() {
        ctx.save();
        ctx.globalAlpha = this.life / 100;
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    }
}

let particles = [];

function createExplosion(x, y, color) {
    for (let i = 0; i < 30; i++) {
        particles.push(new Particle(x, y, color));
    }
}

function animateParticles() {
    particles = particles.filter(p => p.life > 0);
    particles.forEach(p => {
        p.update();
        p.draw();
    });
    
    if (particles.length > 0) {
        requestAnimationFrame(animateParticles);
    }
}

// Load game from localStorage
function loadGame() {
    const saved = localStorage.getItem('lemonbotFarmzULTRA');
    if (saved) {
        gameState = JSON.parse(saved);
    }
    updateUI();
}

// Save game to localStorage
function saveGame() {
    localStorage.setItem('lemonbotFarmzULTRA', JSON.stringify(gameState));
}

// Add log entry
function addLog(message, type = 'normal') {
    const logElement = document.getElementById('log');
    const entry = document.createElement('p');
    entry.className = `log-entry ${type}`;
    entry.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
    logElement.insertBefore(entry, logElement.firstChild);
    
    while (logElement.children.length > 25) {
        logElement.removeChild(logElement.lastChild);
    }
}

// Update UI
function updateUI() {
    document.getElementById('lemons').textContent = gameState.lemons;
    document.getElementById('energy').textContent = gameState.energy;
    document.getElementById('creatures').textContent = gameState.creatures.length;
    
    document.querySelector('.harvest-btn').disabled = gameState.energy < 10;
    document.querySelector('.feed-btn').disabled = gameState.energy < 20 || gameState.creatures.length === 0;
    document.querySelector('.spawn-btn').disabled = gameState.lemons < 50;
    
    updateCreaturesDisplay();
    saveGame();
}

// Display creatures
function updateCreaturesDisplay() {
    const grid = document.getElementById('creaturesGrid');
    grid.innerHTML = '';
    
    gameState.creatures.forEach((creature, index) => {
        const card = document.createElement('div');
        card.className = 'creature-card';
        card.style.borderColor = creature.color;
        card.style.background = `linear-gradient(135deg, ${creature.color}40, ${creature.color}20)`;
        
        card.innerHTML = `
            <div class="creature-emoji">${creature.emoji}</div>
            <div class="creature-petard">💣</div>
            <div class="creature-name" style="color: ${creature.color};">${creature.name}</div>
            <div class="creature-health" style="color: ${creature.color};">❤️ ${creature.health}%</div>
        `;
        
        card.addEventListener('click', () => interactWithCreature(index));
        grid.appendChild(card);
    });
}

// Spawn new creature
function spawnCreature() {
    if (gameState.lemons < 50) {
        addLog('❌ PAS ASSEZ DE CITRONS EXPLOSIFS!!!', 'error');
        createExplosion(window.innerWidth / 2, window.innerHeight / 2, '#ff0000');
        return;
    }
    
    gameState.lemons -= 50;
    const type = CREATURE_TYPES[Math.floor(Math.random() * CREATURE_TYPES.length)];
    
    const creature = {
        id: gameState.creatureCounter++,
        name: type.name,
        emoji: type.emoji,
        petard: type.petard,
        health: 100,
        type: type.name,
        multiplier: type.multiplier,
        color: type.color,
        createdAt: Date.now()
    };
    
    gameState.creatures.push(creature);
    addLog(`🎆 ${creature.name} EST NÉ!!!! 💥🎇`, 'success');
    createExplosion(window.innerWidth / 2, window.innerHeight / 2, type.color);
    animateParticles();
    updateUI();
}

// Interact with creature (click)
function interactWithCreature(index) {
    const creature = gameState.creatures[index];
    if (!creature) return;
    
    creature.health = Math.min(100, creature.health + 5);
    gameState.lemons += 5;
    addLog(`🎉 ${creature.name} EST HEUREUX! +5 CITRONS EXPLOSIFS!`, 'success');
    
    // Mini explosion
    const cards = document.querySelectorAll('.creature-card');
    const rect = cards[index].getBoundingClientRect();
    createExplosion(rect.left + rect.width / 2, rect.top + rect.height / 2, creature.color);
    animateParticles();
    
    updateUI();
}

// Harvest lemons
function harvestLemmons() {
    if (gameState.energy < 10) {
        addLog('❌ PAS ASSEZ DÉNERGIE NUCLÉAIRE!!!', 'error');
        return;
    }
    
    gameState.energy -= 10;
    let harvest = 50;
    
    gameState.creatures.forEach(creature => {
        if (creature.health > 50) {
            harvest += Math.floor(15 * creature.multiplier);
        }
    });
    
    gameState.lemons += harvest;
    addLog(`💥💥💥 EXPLOSION DE CITRONS! +${harvest} POINTS! 💥💥💥`, 'success');
    createExplosion(window.innerWidth / 2, window.innerHeight / 2, '#ffff00');
    animateParticles();
    updateUI();
}

// Feed creatures
function feedCreatures() {
    if (gameState.energy < 20) {
        addLog('❌ PAS ASSEZ DÉNERGIE!!!', 'error');
        return;
    }
    
    if (gameState.creatures.length === 0) {
        addLog('❌ AUCUNE CRÉATURE À NOURRIR!', 'error');
        return;
    }
    
    gameState.energy -= 20;
    gameState.creatures.forEach(creature => {
        creature.health = Math.min(100, creature.health + 20);
    });
    
    addLog(`🔥 TOUS LES ${gameState.creatures.length} MONSTRES SONT RASSASIÉS!!! 🔥`, 'success');
    createExplosion(window.innerWidth / 2, window.innerHeight / 2, '#ff8800');
    animateParticles();
    updateUI();
}

// Rest to restore energy
function rest() {
    gameState.energy = gameState.maxEnergy;
    addLog('⚡ RECHARGE NUCLÉAIRE COMPLÈTE! ⚡⚡⚡', 'success');
    createExplosion(window.innerWidth / 2, window.innerHeight / 2, '#0000ff');
    animateParticles();
    updateUI();
}

// Toggle shop
function toggleShop() {
    const shop = document.getElementById('shopPanel');
    if (shop.style.display === 'none') {
        shop.style.display = 'block';
        createExplosion(window.innerWidth / 2, window.innerHeight / 2, '#ff00ff');
        animateParticles();
    } else {
        shop.style.display = 'none';
    }
}

// Shop: Buy lemmons
function buyLemmons(amount) {
    gameState.lemons += amount;
    addLog(`🎁 +${amount} CITRONS EXPLOSIFS ACHETÉS!`, 'warning');
    createExplosion(window.innerWidth / 2, window.innerHeight / 2, '#ffff00');
    animateParticles();
    updateUI();
}

// Shop: Buy energy
function buyEnergy(amount) {
    gameState.energy = Math.min(gameState.maxEnergy + 200, gameState.energy + amount);
    addLog(`⚡ +${amount} ÉNERGIE NUCLÉAIRE ACHETÉE!`, 'warning');
    createExplosion(window.innerWidth / 2, window.innerHeight / 2, '#00ffff');
    animateParticles();
    updateUI();
}

// Shop: Buy bundle
function buyBundle() {
    gameState.lemons += 2000;
    gameState.energy = gameState.maxEnergy + 200;
    addLog(`🎆 PACK ULTIME ACHETÉ! PURE FOLIE! 🎆🎆🎆`, 'success');
    createExplosion(window.innerWidth / 2, window.innerHeight / 2, '#ff00ff');
    createExplosion(window.innerWidth / 2 + 100, window.innerHeight / 2 + 100, '#00ff00');
    createExplosion(window.innerWidth / 2 - 100, window.innerHeight / 2 - 100, '#00ffff');
    animateParticles();
    updateUI();
}

// Reset game
function resetGame() {
    if (confirm('🚨 ÊTES-VOUS FOU?! CELA EFFACERA TOUT! 🚨')) {
        gameState = {
            lemons: 0,
            energy: 100,
            maxEnergy: 100,
            creatures: [],
            creatureCounter: 0
        };
        localStorage.removeItem('lemonbotFarmzULTRA');
        addLog('🔄 JEU RÉINITIALISÉ DANS UN NUAGE DE FUMÉE! 💨💨💨', 'success');
        for (let i = 0; i < 3; i++) {
            setTimeout(() => {
                createExplosion(
                    Math.random() * window.innerWidth,
                    Math.random() * window.innerHeight,
                    ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff'][Math.floor(Math.random() * 5)]
                );
                animateParticles();
            }, i * 200);
        }
        updateUI();
    }
}

// Auto-decay creatures health
function decayCreaturesHealth() {
    gameState.creatures = gameState.creatures.filter(creature => {
        creature.health = Math.max(0, creature.health - 1);
        return creature.health > 0;
    });
    updateUI();
}

// Game loop
setInterval(() => {
    if (gameState.creatures.length > 0) {
        decayCreaturesHealth();
    }
}, 10000);

// Initialize
window.addEventListener('load', () => {
    loadGame();
    addLog('🎮 BIENVENUE DANS LE CHAOS ABSOLU!', 'success');
    addLog('🍋 CRÉE TES CITRONS EXPLOSIFS ET DEVIENT MILLIARDAIRE!', 'warning');
    addLog('💥 TOUT PEUT EXPLOSER À TOUT MOMENT! 💥', 'error');
    createExplosion(window.innerWidth / 2, window.innerHeight / 2, '#00ffff');
    animateParticles();
});
