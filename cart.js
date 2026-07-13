// Cart Management
let cart = [];

function addToCart(productId) {
    const product = products.find(p => p.id === productId);
    if (!product) return;

    const existingItem = cart.find(item => item.id === productId);
    
    if (existingItem) {
        existingItem.quantity++;
    } else {
        cart.push({ ...product, quantity: 1 });
    }

    updateCart();
    showNotification(`✅ ${product.name} ajouté au panier!`);
}

function removeFromCart(productId) {
    cart = cart.filter(item => item.id !== productId);
    updateCart();
}

function updateCart() {
    // Update count
    document.getElementById('cartCount').textContent = cart.reduce((sum, item) => sum + item.quantity, 0);

    // Update items display
    const cartItems = document.getElementById('cartItems');
    if (cart.length === 0) {
        cartItems.innerHTML = '<p class="empty-cart">Votre panier est vide</p>';
    } else {
        cartItems.innerHTML = cart.map(item => `
            <div class="cart-item">
                <span class="cart-item-name">${item.emoji} ${item.name} x${item.quantity}</span>
                <span class="cart-item-price">$${(item.price * item.quantity).toFixed(2)}</span>
                <button class="cart-item-remove" onclick="removeFromCart(${item.id})">❌</button>
            </div>
        `).join('');
    }

    // Update total
    const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    document.getElementById('cartTotal').textContent = total.toFixed(2);

    // Save to localStorage
    localStorage.setItem('cart', JSON.stringify(cart));
}

function toggleCart() {
    document.getElementById('cartPanel').classList.toggle('open');
}

function checkout() {
    if (cart.length === 0) {
        showNotification('⚠️ Votre panier est vide!');
        return;
    }

    const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    showNotification(`✅ Commande de $${total.toFixed(2)} confirmée! 🎉`);
    
    // Clear cart
    cart = [];
    updateCart();
    toggleCart();
}

// Load cart from localStorage
window.addEventListener('load', () => {
    const saved = localStorage.getItem('cart');
    if (saved) {
        cart = JSON.parse(saved);
        updateCart();
    }
});

function showNotification(message) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: #4CAF50;
        color: white;
        padding: 15px 25px;
        border-radius: 8px;
        font-weight: bold;
        z-index: 3000;
        animation: slideIn 0.3s ease-out;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 2000);
}

const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(400px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(400px); opacity: 0; }
    }
`;
document.head.appendChild(style);
