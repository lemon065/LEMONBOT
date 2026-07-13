// Products Data
const products = [
    { id: 1, name: 'OG Kush', category: 'flower', emoji: '🌸', description: 'Classique puissant et relaxant. Saveur terreuse.', price: 45.99 },
    { id: 2, name: 'Sativa Mix', category: 'flower', emoji: '🍃', description: 'Énergisant et créatif. Parfait le jour.', price: 39.99 },
    { id: 3, name: 'Purple Haze', category: 'flower', emoji: '🌺', description: 'Légendaire. Saveur fruitée et douce.', price: 52.99 },
    { id: 4, name: 'CBD Oil 10ml', category: 'oil', emoji: '🧴', description: 'Pure et concentrée. 1000mg CBD.', price: 29.99 },
    { id: 5, name: 'Full Spectrum Oil', category: 'oil', emoji: '🧤', description: 'Tous les cannabinoïdes. Effet entourage.', price: 34.99 },
    { id: 6, name: 'Gummies Mix', category: 'edibles', emoji: '🍬', description: '10 gummies délicieux. 100mg CBD/pièce.', price: 24.99 },
    { id: 7, name: 'Brownie CBD', category: 'edibles', emoji: '🍫', description: 'Chocolat artisanal. 200mg CBD.', price: 19.99 },
    { id: 8, name: 'Vape Pen', category: 'vape', emoji: '💨', description: 'Portable et discret. Batterie 2h.', price: 44.99 },
    { id: 9, name: 'Cartridge Assort', category: 'vape', emoji: '🔧', description: 'Pack 3 saveurs. Compatible tous vapes.', price: 49.99 },
    { id: 10, name: 'Grinder Premium', category: 'accessories', emoji: '🛠️', description: 'Aluminium 4 étages. Tamis fin.', price: 22.99 },
    { id: 11, name: 'Pochettes Storage', category: 'accessories', emoji: '📦', description: 'Pack de 5 pochettes hermétiques.', price: 14.99 },
    { id: 12, name: 'Glass Case', category: 'accessories', emoji: '🎪', description: 'Protège et conserve tes produits.', price: 19.99 }
];

const games = [
    { id: 'g1', name: 'Clicker Game', category: 'games', emoji: '🔥', description: 'Clique le plus vite possible! Deviens champion!', type: 'clicker' },
    { id: 'g2', name: 'Lucky Spin', category: 'games', emoji: '🎡', description: 'Roue de la fortune avec récompenses!', type: 'spin' },
    { id: 'g3', name: 'Memory Game', category: 'games', emoji: '🧠', description: 'Trouve les paires. Teste ta mémoire!', type: 'memory' },
    { id: 'g4', name: 'Grow Plant', category: 'games', emoji: '🌱', description: 'Cultive ta plante. Sois patient!', type: 'grow' }
];

let currentCategory = 'all';
let currentProduct = null;

function renderProductsList() {
    const list = document.getElementById('productsList');
    const allItems = currentCategory === 'games' ? games : 
                     currentCategory === 'all' ? [...products, ...games] : 
                     products.filter(p => p.category === currentCategory);

    list.innerHTML = allItems.map(item => `
        <div class="product-item ${currentProduct?.id === item.id ? 'active' : ''}" 
             onclick="selectProduct('${item.id}')"
             data-id="${item.id}">
            <div class="product-avatar">${item.emoji}</div>
            <div class="product-info">
                <div class="product-name">${item.name}</div>
                <div class="product-price">${item.type ? 'Jeu' : '$' + item.price.toFixed(2)}</div>
            </div>
        </div>
    `).join('');
}

function selectCategory(category, element) {
    document.querySelectorAll('.category-btn').forEach(btn => btn.classList.remove('active'));
    element.classList.add('active');
    currentCategory = category;
    renderProductsList();
}

function selectProduct(productId) {
    const isGame = productId.startsWith('g');
    const product = isGame ? games.find(g => g.id === productId) : products.find(p => p.id == productId);
    
    if (!product) return;
    
    currentProduct = product;
    renderProductsList();
    displayProductDetail(product, isGame);
}

function displayProductDetail(product, isGame = false) {
    const chatMessages = document.getElementById('chatMessages');
    const chatHeader = document.getElementById('chatHeader');
    
    // Update header
    document.getElementById('chatTitle').textContent = product.name;
    document.getElementById('chatSubtitle').textContent = product.description;
    
    // Display product detail
    let html = `
        <div class="product-detail">
            <div class="product-detail-header">
                <div class="product-detail-emoji">${product.emoji}</div>
                <div class="product-detail-info">
                    <h3>${product.name}</h3>
                    <p>${product.category}</p>
                </div>
            </div>
            <div class="product-detail-description">
                ${product.description}
            </div>
    `;
    
    if (isGame) {
        html += `
            <div class="product-detail-buttons">
                <button class="add-btn" onclick="startGame('${product.type}')">🎮 Jouer Maintenant</button>
            </div>
        `;
    } else {
        html += `
            <div class="product-detail-price">$${product.price.toFixed(2)}</div>
            <div class="product-detail-buttons">
                <button class="add-btn" onclick="addToCart(${product.id})">🛒 Ajouter au panier</button>
                <button class="quantity-btn" onclick="addToCart(${product.id}, 5)">+5 articles</button>
            </div>
        `;
    }
    
    html += '</div>';
    
    chatMessages.innerHTML = html;
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function searchProducts() {
    const query = document.getElementById('searchInput').value.toLowerCase();
    const allItems = [...products, ...games];
    const filtered = allItems.filter(item => 
        item.name.toLowerCase().includes(query) ||
        item.description.toLowerCase().includes(query)
    );
    
    const list = document.getElementById('productsList');
    list.innerHTML = filtered.map(item => `
        <div class="product-item" onclick="selectProduct('${item.id}')" data-id="${item.id}">
            <div class="product-avatar">${item.emoji}</div>
            <div class="product-info">
                <div class="product-name">${item.name}</div>
                <div class="product-price">${item.type ? 'Jeu' : '$' + item.price.toFixed(2)}</div>
            </div>
        </div>
    `).join('');
}

// Initialize
window.addEventListener('load', () => {
    renderProductsList();
});
