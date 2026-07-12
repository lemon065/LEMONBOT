#!/usr/bin/env python3
"""
LEMONBOT - Bot Telegram pour cultiver des citrons!
"""

import logging
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ConversationHandler
)
from config import TELEGRAM_BOT_TOKEN, LOG_LEVEL
from handlers import Handlers
import sys

# Configuration du logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=LOG_LEVEL
)
logger = logging.getLogger(__name__)

async def main():
    """Fonction principale"""
    
    # Vérifier que le token existe
    if not TELEGRAM_BOT_TOKEN:
        logger.error("❌ ERREUR: Token Telegram Bot manquant!")
        logger.error("Veuillez configurer TELEGRAM_BOT_TOKEN dans le fichier .env")
        sys.exit(1)
    
    # Créer l'application
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    logger.info("🤖 LEMONBOT - Initialisation...")
    
    # Handlers de commandes
    app.add_handler(CommandHandler('start', Handlers.start))
    app.add_handler(CommandHandler('help', Handlers.help_command))
    
    # Handlers de boutons
    app.add_handler(CallbackQueryHandler(Handlers.button_callback))
    
    # Handlers de messages texte (pour les avis)
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        Handlers.handle_review_text
    ))
    
    logger.info("✅ LEMONBOT est prêt!")
    logger.info("🚀 Démarrage du bot...")
    
    # Démarrer le bot
    await app.run_polling(
        allowed_updates=['message', 'callback_query'],
        drop_pending_updates=True
    )

if __name__ == '__main__':
    import asyncio
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n⛔ Bot arrêté.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Erreur fatale: {e}")
        sys.exit(1)
