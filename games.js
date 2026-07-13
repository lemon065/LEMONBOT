// Games
function toggleGames() {
    document.getElementById('gamesPanel').classList.toggle('open');
}

function startGame(game) {
    const gameContainer = document.getElementById('gameContainer');
    const gameContent = document.getElementById('gameContent');

    switch(game) {
        case 'grow':
            gameContent.innerHTML = growGameHTML();
            initGrowGame();
            break;
        case 'clicker':
            gameContent.innerHTML = clickerGameHTML();
            initClickerGame();
            break;
        case 'spin':
            gameContent.innerHTML = spinGameHTML();
            initSpinGame();
            break;
        case 'memory':
            gameContent.innerHTML = memoryGameHTML();
            initMemoryGame();
            break;
    }

    gameContainer.style.display = 'flex';
    toggleGames();
}

function closeGame() {
    document.getElementById('gameContainer').style.display = 'none';
}

// GROW GAME
function growGameHTML() {
    return `
        <div style="text-align: center;">
            <h2>🌱 Cultiver ta Plante</h2>
            <div style="font-size: 5em; margin: 30px 0; animation: grow-bounce 1s ease-in-out infinite;" id="plantEmoji">🌱</div>
            <div style="font-size: 1.3em; color: #4CAF50; margin: 20px 0;">
                Stade: <span id="growStage">Graine</span>
            </div>
            <div style="font-size: 1.2em; color: #90EE90; margin: 15px 0;">
                Croissance: <span id="growPercent">0</span>%
            </div>
            <button style="padding: 15px 30px; background: #4CAF50; color: white; border: none; border-radius: 8px; font-size: 1.1em; cursor: pointer; margin: 20px 5px;" onclick="waterPlant()">💧 Arroser</button>
            <button style="padding: 15px 30px; background: #FFD700; color: black; border: none; border-radius: 8px; font-size: 1.1em; cursor: pointer; margin: 20px 5px;" onclick="sunnePlant()">☀️ Soleil</button>
        </div>
    `;
}

let plantGrowth = 0;
const plantStages = ['🌱', '🌿', '🍃', '🌳', '🌲'];
const stageNames = ['Graine', 'Jeune Pousse', 'Plante', 'Arbuste', 'Plante Mature'];

function waterPlant() {
    plantGrowth += 10;
    updatePlant();
}

function sunnePlant() {
    plantGrowth += 15;
    updatePlant();
}

function updatePlant() {
    const stage = Math.min(4, Math.floor(plantGrowth / 25));
    document.getElementById('plantEmoji').textContent = plantStages[stage];
    document.getElementById('growStage').textContent = stageNames[stage];
    document.getElementById('growPercent').textContent = plantGrowth;

    if (plantGrowth >= 100) {
        setTimeout(() => {
            showNotification('🎉 Ta plante est prête! Récolte: +50 points!');
            plantGrowth = 0;
            updatePlant();
        }, 500);
    }
}

// CLICKER GAME
function clickerGameHTML() {
    return `
        <div style="text-align: center;">
            <h2>🎯 Weed Clicker</h2>
            <button style="font-size: 8em; border: none; background: none; cursor: pointer; margin: 30px 0; transition: transform 0.1s;" id="clickBtn" onclick="clickWeed()">🍃</button>
            <div style="font-size: 2em; color: #4CAF50; margin: 30px 0;">
                Score: <span id="clickScore">0</span>
            </div>
            <div style="font-size: 1.2em; color: #90EE90;">
                Clique le plus vite possible!
            </div>
        </div>
    `;
}

let clickScore = 0;
function clickWeed() {
    clickScore++;
    document.getElementById('clickScore').textContent = clickScore;
    
    const btn = document.getElementById('clickBtn');
    btn.style.transform = 'scale(0.9)';
    setTimeout(() => btn.style.transform = 'scale(1)', 100);

    if (clickScore % 10 === 0) {
        showNotification(`🔥 ${clickScore} clics! Continue!`);
    }
}

function initClickerGame() {
    clickScore = 0;
}

// SPIN GAME
function spinGameHTML() {
    return `
        <div style="text-align: center;">
            <h2>🎡 Lucky Spin</h2>
            <div style="font-size: 6em; margin: 30px 0; animation: spin-wheel 2s linear;" id="wheelEmoji">🎡</div>
            <button style="padding: 15px 30px; background: #FFD700; color: black; border: none; border-radius: 8px; font-size: 1.2em; cursor: pointer; margin: 20px;" id="spinBtn" onclick="spinWheel()">SPINNER!</button>
            <div style="font-size: 1.3em; color: #4CAF50; margin: 20px 0;" id="spinResult"></div>
        </div>
    `;
}

function spinWheel() {
    const btn = document.getElementById('spinBtn');
    btn.disabled = true;
    
    const results = [
        { emoji: '🎁', text: 'Gagné 50 points!' },
        { emoji: '💰', text: 'Gagné 100 points!' },
        { emoji: '🎉', text: 'Jackpot! 200 points!' },
        { emoji: '😢', text: 'Rien... Réessaie!' },
        { emoji: '⭐', text: 'Gagné 75 points!' },
        { emoji: '🏆', text: 'Champion! 150 points!' }
    ];

    const result = results[Math.floor(Math.random() * results.length)];
    
    document.getElementById('wheelEmoji').style.animation = 'spin-wheel 1s linear';
    
    setTimeout(() => {
        document.getElementById('spinResult').innerHTML = `${result.emoji} <strong>${result.text}</strong>`;
        btn.disabled = false;
    }, 1000);
}

// MEMORY GAME
function memoryGameHTML() {
    const cards = Array(8).fill(0).map((_, i) => ['🌿', '🌿', '🍃', '🍃', '💨', '💨', '🌱', '🌱'][i]);
    const shuffled = cards.sort(() => Math.random() - 0.5);
    
    return `
        <div style="text-align: center;">
            <h2>🧠 Memory Game</h2>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin: 30px 0; max-width: 400px; margin-left: auto; margin-right: auto;">
                ${shuffled.map((card, i) => `
                    <button 
                        style="padding: 30px; font-size: 2em; background: #4CAF50; border: 2px solid #90EE90; border-radius: 8px; cursor: pointer; transition: all 0.2s;"
                        onclick="flipMemoryCard(this)" 
                        data-card="${card}"
                    >?
                    </button>
                `).join('')}
            </div>
            <div style="font-size: 1.2em; color: #4CAF50;">
                Pairs trouvées: <span id="memoryMatches">0</span>/4
            </div>
        </div>
    `;
}

let memoryFlipped = [];
let memoryMatches = 0;

function flipMemoryCard(element) {
    if (element.style.background === 'rgba(76, 175, 80, 0.3)') return;
    
    const card = element.dataset.card;
    element.textContent = card;
    element.style.background = 'rgba(76, 175, 80, 0.3)';
    
    memoryFlipped.push({ element, card });
    
    if (memoryFlipped.length === 2) {
        if (memoryFlipped[0].card === memoryFlipped[1].card) {
            memoryMatches++;
            document.getElementById('memoryMatches').textContent = memoryMatches;
            memoryFlipped = [];
            
            if (memoryMatches === 4) {
                showNotification('🎉 Tu as gagné! Bravo!');
            }
        } else {
            setTimeout(() => {
                memoryFlipped[0].element.textContent = '?';
                memoryFlipped[0].element.style.background = '#4CAF50';
                memoryFlipped[1].element.textContent = '?';
                memoryFlipped[1].element.style.background = '#4CAF50';
                memoryFlipped = [];
            }, 800);
        }
    }
}

function initMemoryGame() {
    memoryFlipped = [];
    memoryMatches = 0;
}

// Animation styles
const gameStyles = document.createElement('style');
gameStyles.textContent = `
    @keyframes grow-bounce {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    @keyframes spin-wheel {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
`;
document.head.appendChild(gameStyles);
