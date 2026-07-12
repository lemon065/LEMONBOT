import os
from dotenv import load_dotenv

load_dotenv()

# Configuration du bot
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
ADMIN_ID = int(os.getenv('ADMIN_ID', '0'))
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Emojis pour le menu
EMOJIS = {
    'home': '🏠',
    'play': '🎮',
    'stats': '📊',
    'shop': '🛍️',
    'farm': '🌾',
    'reviews': '⭐',
    'settings': '⚙️',
    'support': '💬',
    'info': 'ℹ️',
    'lemon': '🍋',
    'back': '◀️',
    'next': '▶️',
    'check': '✅',
    'cross': '❌',
    'loading': '⏳',
}

# Messages
MESSAGES = {
    'welcome': '🍋 Bienvenue sur LEMONBOT! 🍋\n\nLe meilleur bot de farming de citrons!\n\nChoisissez une option ci-dessous:',
    'menu_principal': '📱 Menu Principal\n\nQue veux-tu faire?',
    'loading': 'Chargement...',
    'error': '❌ Une erreur s\'est produite. Réessaye plus tard.',
}

# Paramètres du jeu
GAME_CONFIG = {
    'initial_balance': 100,
    'max_reviews': 5,
    'harvest_time': 3600,  # secondes
}
