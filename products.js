// Products Database
const products = [
    // Fleurs
    {
        id: 1,
        name: 'OG Kush',
        category: 'flower',
        emoji: '🌸',
        description: 'Classique incontournable. Puissant et relaxant.',
        price: 45.99
    },
    {
        id: 2,
        name: 'Sativa Mix',
        category: 'flower',
        emoji: '🌿',
        description: 'Énergisant et créatif. Parfait le jour.',
        price: 39.99
    },
    {
        id: 3,
        name: 'Purple Haze',
        category: 'flower',
        emoji: '🌺',
        description: 'Légendaire. Saveur fruitée et douce.',
        price: 52.99
    },
    // Huiles
    {
        id: 4,
        name: 'CBD Oil 10ml',
        category: 'oil',
        emoji: '🧴',
        description: 'Pure et concentrée. 1000mg CBD.',
        price: 29.99
    },
    {
        id: 5,
        name: 'Full Spectrum Oil',
        category: 'oil',
        emoji: '🫙',
        description: 'Tous les cannabinoïdes. Effet entourage.',
        price: 34.99
    },
    // Comestibles
    {
        id: 6,
        name: 'Gummies Mix',
        category: 'edibles',
        emoji: '🍬',
        description: '10 gummies délicieux. 100mg CBD/pièce.',
        price: 24.99
    },
    {
        id: 7,
        name: 'Brownie CBD',
        category: 'edibles',
        emoji: '🍫',
        description: 'Chocolat artisanal. 200mg CBD.',
        price: 19.99
    },
    // Vapes
    {
        id: 8,
        name: 'Vape Pen',
        category: 'vape',
        emoji: '💨',
        description: 'Portable et discret. Batterie 2h.',
        price: 44.99
    },
    {
        id: 9,
        name: 'Cartridge Assort',
        category: 'vape',
        emoji: '🔧',
        description: 'Pack 3 saveurs. Compatible tous vapes.',
        price: 49.99
    },
    // Accessoires
    {
        id: 10,
        name: 'Grinder Premium',
        category: 'accessories',
        emoji: '🛠️',
        description: 'Aluminium 4 étages. Tamis fin.',
        price: 22.99
    },
    {
        id: 11,
        name: 'Pochettes Storage',
        category: 'accessories',
        emoji: '📦',
        description: 'Pack de 5 pochettes hermétiques.',
        price: 14.99
    },
    {
        id: 12,
        name: 'Glass Case',
        category: 'accessories',
        emoji: '🏺',
        description: 'Protège et conserve tes produits.',
        price: 19.99
    }
];

// Render Products
function renderProducts(filtered = products) {
    const grid = document.getElementById('productsGrid');
    grid.innerHTML = '';

    filtered.forEach(product => {
        const card = document.createElement('div');
        card.className = 'product-card';
        card.innerHTML = `
            <div class="product-emoji">${product.emoji}</div>
            <div class="product-name">${product.name}</div>
            <div class="product-description">${product.description}</div>
            <div class="product-price">$${product.price.toFixed(2)}</div>
            <button class="add-to-cart-btn" onclick="addToCart(${product.id})">
                🛒 Ajouter au panier
            </button>
        `;
        grid.appendChild(card);
    });
}

// Filter Products
function filterProducts(category) {
    // Update active button
    document.querySelectorAll('.menu-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');

    // Update title
    const titles = {
        'all': '🛍️ Tous les produits',
        'flower': '🌸 Fleurs',
        'oil': '🧴 Huiles',
        'edibles': '🍬 Comestibles',
        'vape': '💨 Vapes',
        'accessories': '🛠️ Accessoires'
    };
    document.getElementById('sectionTitle').textContent = titles[category];

    // Filter and render
    if (category === 'all') {
        renderProducts(products);
    } else {
        renderProducts(products.filter(p => p.category === category));
    }
}

// Initialize
window.addEventListener('load', () => {
    renderProducts();
});
