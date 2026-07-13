// Main
function handleMessageInput(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message to chat
    const chatMessages = document.getElementById('chatMessages');
    const userMsg = document.createElement('div');
    userMsg.style.cssText = 'text-align: right; margin-bottom: 12px;';
    userMsg.innerHTML = `
        <div style="background: #2a9d8f; color: white; padding: 12px 15px; border-radius: 12px; display: inline-block; max-width: 400px;">
            ${message}
        </div>
    `;
    chatMessages.appendChild(userMsg);
    
    input.value = '';
    
    // Bot response
    setTimeout(() => {
        const botMsg = document.createElement('div');
        botMsg.innerHTML = `
            <div style="background: #f0f0f0; padding: 12px 15px; border-radius: 12px; display: inline-block; max-width: 400px; color: #222;">
                Merci pour ta question! 😊 Explore nos produits et jeux! 🎮
            </div>
        `;
        chatMessages.appendChild(botMsg);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 500);
}

// Initialize
window.addEventListener('load', () => {
    document.getElementById('statPoints').textContent = gamePoints;
});
