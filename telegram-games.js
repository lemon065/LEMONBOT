// Games
function startGame(gameType) {
    const modal = document.getElementById('gameModal');
    const gameContent = document.getElementById('gameContent');
    
    let html = '';
    
    switch(gameType) {
        case 'clicker':
            html = `
                <h2>🔥 Weed Clicker</h2>
                <div style="text-align: center; margin: 30px 0;">
                    <button id="clickBtn" style="font-size: 8em; border: none; background: none; cursor: pointer; transition: transform 0.1s;" onclick="clickButton()">🌿</button>
                    <div style="font-size: 2em; color: #2a9d8f; margin: 30px 0; font-weight: bold;">
                        Score: <span id="clickScore">0</span>
                    </div>
                    <p style="color: #999; margin-bottom: 20px;">Clique le plus vite possible!</p>
                    <button onclick="endClickerGame()" style="padding: 10px 20px; background: #f0f0f0; border: 1px solid #e5e5e5; border-radius: 8px; cursor: pointer;">Terminer</button>
                </div>
            `;
            break;
        case 'spin':
            html = `
                <h2>🎡 Lucky Spin</h2>
                <div style="text-align: center; margin: 30px 0;">
                    <div id="wheelSpinner" style="font-size: 6em; margin: 30px 0; transition: transform 1s ease-out;">🎡</div>
                    <button id="spinBtn" onclick="spinWheel()" style="padding: 15px 30px; background: #2a9d8f; color: white; border: none; border-radius: 8px; font-size: 1.1em; cursor: pointer; font-weight: 600; transition: all 0.2s;" onmouseover="this.style.background='#1f7469'" onmouseout="this.style.background='#2a9d8f'">SPINNER!</button>
                    <div id="spinResult" style="font-size: 1.3em; color: #2a9d8f; margin-top: 20px; font-weight: bold;"></div>
                    <button onclick="closeGameModal()" style="padding: 10px 20px; background: #f0f0f0; border: 1px solid #e5e5e5; border-radius: 8px; cursor: pointer; margin-top: 20px;">Fermer</button>
                </div>
            `;
            break;
        case 'memory':
            const cards = ['🌿', '🌿', '💨', '💨', '🍃', '🍃', '🌱', '🌱'];
            const shuffled = cards.sort(() => Math.random() - 0.5);
            html = `
                <h2>🧠 Memory Game</h2>
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin: 30px 0; max-width: 400px;">
                    ${shuffled.map((card, i) => `
                        <button data-card="${card}" onclick="flipCard(this)" 
                            style="padding: 30px; font-size: 2em; background: #2a9d8f; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: bold;">?
                        </button>
                    `).join('')}
                </div>
                <div style="text-align: center; font-size: 1.2em; color: #2a9d8f; font-weight: bold; margin: 20px 0;">
                    Paires trouvées: <span id="memoryMatches">0</span>/4
                </div>
                <button onclick="closeGameModal()" style="width: 100%; padding: 10px; background: #f0f0f0; border: 1px solid #e5e5e5; border-radius: 8px; cursor: pointer;">Fermer</button>
            `;
            break;
        case 'grow':
            html = `
                <h2>🌱 Cultiver ta Plante</h2>
                <div style="text-align: center; margin: 30px 0;">
                    <div id="plantEmoji" style="font-size: 5em; margin: 30px 0; transition: transform 0.3s;">🌱</div>
                    <div style="font-size: 1.3em; color: #2a9d8f; margin: 20px 0; font-weight: bold;">
                        Croissance: <span id="growPercent">0</span>%
                    </div>
                    <div style="display: flex; gap: 10px; justify-content: center; margin: 20px 0;">
                        <button onclick="waterPlant()" style="padding: 12px 20px; background: #2a9d8f; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: 600;">💧 Arroser</button>
                        <button onclick="sunnyPlant()" style="padding: 12px 20px; background: #FFD700; color: #222; border: none; border-radius: 8px; cursor: pointer; font-weight: 600;">☀️ Soleil</button>
                    </div>
                    <button onclick="closeGameModal()" style="width: 100%; padding: 10px; background: #f0f0f0; border: 1px solid #e5e5e5; border-radius: 8px; cursor: pointer; margin-top: 20px;">Fermer</button>
                </div>
            `;
            break;
    }
    
    gameContent.innerHTML = html;
    modal.classList.add('open');
    
    if (gameType === 'clicker') {
        window.clickerScore = 0;
    }
    if (gameType === 'memory') {
        window.memoryFlipped = [];
        window.memoryMatches = 0;
    }
    if (gameType === 'grow') {
        window.plantGrowth = 0;
        const stages = ['🌱', '🌿', '🍃', '🌾', '🌳'];
        window.plantStages = stages;
    }
}

function startQuickGame(type) {
    startGame(type);
}

function closeGameModal() {
    document.getElementById('gameModal').classList.remove('open');
}

// Clicker
function clickButton() {
    window.clickerScore = (window.clickerScore || 0) + 1;
    document.getElementById('clickScore').textContent = window.clickerScore;
    
    const btn = document.getElementById('clickBtn');
    btn.style.transform = 'scale(0.9)';
    setTimeout(() => btn.style.transform = 'scale(1)', 100);
    
    if (window.clickerScore % 10 === 0) {
        showNotification(`🔥 ${window.clickerScore} clics!`);
    }
}

function endClickerGame() {
    gamePoints += Math.floor(window.clickerScore / 10);
    document.getElementById('statPoints').textContent = gamePoints;
    showNotification(`🎉 +${Math.floor(window.clickerScore / 10)} points gagnés!`);
    closeGameModal();
}

// Spin
function spinWheel() {
    const btn = document.getElementById('spinBtn');
    btn.disabled = true;
    
    const results = [
        { emoji: '🎁', text: '+10 points!' },
        { emoji: '💰', text: '+25 points!' },
        { emoji: '🎉', text: 'Jackpot! +50 points!' },
        { emoji: '😢', text: 'Rien...' },
        { emoji: '⭐', text: '+15 points!' },
        { emoji: '🏆', text: '+30 points!' }
    ];
    
    const result = results[Math.floor(Math.random() * results.length)];
    const wheel = document.getElementById('wheelSpinner');
    
    wheel.style.transform = 'rotate(360deg)';
    
    setTimeout(() => {
        wheel.style.transform = 'rotate(0deg)';
        const points = parseInt(result.text.match(/\d+/)?.[0] || 0);
        gamePoints += points;
        document.getElementById('statPoints').textContent = gamePoints;
        document.getElementById('spinResult').innerHTML = `${result.emoji} <strong>${result.text}</strong>`;
        btn.disabled = false;
    }, 1000);
}

// Memory
let memoryFlipped = [];
let memoryMatches = 0;

function flipCard(element) {
    if (element.style.background === 'rgba(42, 157, 143, 0.3)' || memoryFlipped.length >= 2) return;
    
    const card = element.dataset.card;
    element.textContent = card;
    element.style.background = 'rgba(42, 157, 143, 0.3)';
    memoryFlipped.push({ element, card });
    
    if (memoryFlipped.length === 2) {
        if (memoryFlipped[0].card === memoryFlipped[1].card) {
            memoryMatches++;
            document.getElementById('memoryMatches').textContent = memoryMatches;
            memoryFlipped = [];
            
            gamePoints += 5;
            document.getElementById('statPoints').textContent = gamePoints;
            
            if (memoryMatches === 4) {
                showNotification('🎉 Tu as gagné! +20 bonus points!');
                gamePoints += 20;
                document.getElementById('statPoints').textContent = gamePoints;
                setTimeout(() => closeGameModal(), 1000);
            }
        } else {
            setTimeout(() => {
                memoryFlipped[0].element.textContent = '?';
                memoryFlipped[0].element.style.background = '#2a9d8f';
                memoryFlipped[1].element.textContent = '?';
                memoryFlipped[1].element.style.background = '#2a9d8f';
                memoryFlipped = [];
            }, 800);
        }
    }
}

// Grow
let plantGrowth = 0;

function waterPlant() {
    plantGrowth += 10;
    updatePlantDisplay();
}

function sunnyPlant() {
    plantGrowth += 15;
    updatePlantDisplay();
}

function updatePlantDisplay() {
    const stages = ['🌱', '🌿', '🍃', '🌾', '🌳'];
    const stage = Math.min(4, Math.floor(plantGrowth / 25));
    document.getElementById('plantEmoji').textContent = stages[stage];
    document.getElementById('growPercent').textContent = plantGrowth;
    
    if (plantGrowth >= 100) {
        gamePoints += 15;
        document.getElementById('statPoints').textContent = gamePoints;
        showNotification('🎉 Ta plante est prête! +15 points!');
        plantGrowth = 0;
        updatePlantDisplay();
    }
}
