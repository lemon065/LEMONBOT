from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction
from database import db
from keyboards import Keyboards
from config import MESSAGES, EMOJIS
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class Handlers:
    """Gestionnaire de tous les handlers du bot"""
    
    # ==================== START & HELP ====================
    
    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande /start"""
        user = update.effective_user
        chat_id = update.effective_chat.id
        
        # Ajouter l'utilisateur à la base de données
        db.add_user(user.id, user.username or 'Anonymous', user.first_name or 'User')
        
        # Message de bienvenue
        welcome_text = f"""🍋 **BIENVENUE SUR LEMONBOT!** 🍋

👋 Salut {user.first_name}!

Bienvenue dans l'univers de la culture de citrons! 🌾

**Qu'est-ce que tu peux faire?**
• 🎮 Jouer et cultiver tes citrons
• 📊 Voir tes statistiques
• 💬 Laisser des avis
• 🛍️ Accéder au shop
• ⚙️ Configurer le bot

Choisissez une option ci-dessous:"""
        
        await update.message.reply_text(
            welcome_text,
            reply_markup=Keyboards.menu_principal(),
            parse_mode='Markdown'
        )
    
    @staticmethod
    async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande /help"""
        help_text = """🍋 **AIDE - LEMONBOT** 🍋

**Commandes disponibles:**
/start - Recommencer
/help - Affiche cette aide
/stats - Voir vos statistiques
/play - Jouer

**Menu Principal:**
Use les boutons pour naviguer dans le bot!

**Besoin d'aide?**
Cliquez sur "💬 Support" pour nous contacter.
"""
        await update.message.reply_text(
            help_text,
            parse_mode='Markdown',
            reply_markup=Keyboards.back_button()
        )
    
    # ==================== MENU BUTTONS ====================
    
    @staticmethod
    async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gérer tous les clics sur les boutons"""
        query = update.callback_query
        await query.answer()
        
        callback_data = query.data
        user_id = query.from_user.id
        user = db.get_user(user_id)
        
        # Menu Principal
        if callback_data == 'back_menu':
            await Handlers.show_menu(query, user)
        
        # Farm
        elif callback_data == 'farm':
            await Handlers.show_farm(query, user)
        elif callback_data == 'harvest':
            await Handlers.harvest_lemons(query, user)
        elif callback_data == 'upgrade_farm':
            await Handlers.upgrade_farm(query, user)
        
        # Stats
        elif callback_data == 'stats':
            await Handlers.show_stats(query, user)
        
        # Shop
        elif callback_data == 'shop':
            await query.edit_message_text(
                text="🛍️ **SHOP LEMONBOT**\n\nQue veux-tu acheter?",
                reply_markup=Keyboards.menu_shop(),
                parse_mode='Markdown'
            )
        elif callback_data == 'shop_equipment':
            await Handlers.show_shop_equipment(query, user)
        elif callback_data == 'shop_bonus':
            await Handlers.show_shop_bonus(query, user)
        
        # Reviews
        elif callback_data == 'reviews':
            await query.edit_message_text(
                text="⭐ **AVIS LEMONBOT**\n\nVois les avis des autres joueurs ou laisse le tien!",
                reply_markup=Keyboards.menu_reviews(),
                parse_mode='Markdown'
            )
        elif callback_data == 'view_reviews':
            await Handlers.view_reviews(query)
        elif callback_data == 'write_review':
            await query.edit_message_text(
                text="✍️ **LAISSER UN AVIS**\n\nNote LEMONBOT de 1 à 5 étoiles:",
                reply_markup=Keyboards.rating_buttons(),
                parse_mode='Markdown'
            )
        elif callback_data.startswith('rate_'):
            rating = int(callback_data.split('_')[1])
            context.user_data['rating'] = rating
            await query.edit_message_text(
                text=f"Merci! Tu as choisi {rating} ⭐\n\nEcris maintenant ton commentaire (ou /skip pour sauter):",
                parse_mode='Markdown'
            )
        
        # Play
        elif callback_data == 'play':
            await Handlers.play_game(query, user)
        
        # Settings
        elif callback_data == 'settings':
            await query.edit_message_text(
                text="⚙️ **PARAMÈTRES**\n\nConfigure le bot:",
                reply_markup=Keyboards.menu_settings(),
                parse_mode='Markdown'
            )
        elif callback_data == 'notifications':
            await query.edit_message_text(
                text="🔔 **NOTIFICATIONS**\n\n✅ Les notifications sont activées.",
                reply_markup=Keyboards.back_button(),
                parse_mode='Markdown'
            )
        elif callback_data == 'language':
            await query.edit_message_text(
                text="🌍 **LANGUE**\n\n🇫🇷 Français (actuelle)",
                reply_markup=Keyboards.back_button(),
                parse_mode='Markdown'
            )
        
        # Support
        elif callback_data == 'support':
            await query.edit_message_text(
                text="💬 **SUPPORT**\n\n📧 Email: support@lemonbot.com\n🌐 Site: www.lemonbot.com\n\nNous te répondrons au plus vite!",
                reply_markup=Keyboards.back_button(),
                parse_mode='Markdown'
            )
        
        # Info
        elif callback_data == 'info':
            await query.edit_message_text(
                text="""ℹ️ **À PROPOS DE LEMONBOT**

🍋 LEMONBOT v1.0

Le meilleur bot pour cultiver des citrons!

👨‍💻 Développé avec ❤️
📱 Disponible 24/7
⚡ Rapide et fiable

🎯 Objectif: Cultiver le plus de citrons!
""",
                reply_markup=Keyboards.back_button(),
                parse_mode='Markdown'
            )
    
    # ==================== GAME FUNCTIONS ====================
    
    @staticmethod
    async def show_menu(query, user):
        """Afficher le menu principal"""
        if user:
            text = f"""🍋 **MENU PRINCIPAL**

👤 **Joueur:** {user['first_name']}
💰 **Solde:** {user['balance']:.0f} citrons
📊 **Niveau:** {user['level']}
⚡ **EXP:** {user['exp']}

Que veux-tu faire?"""
        else:
            text = "🍋 **MENU PRINCIPAL**\n\nQue veux-tu faire?"
        
        await query.edit_message_text(
            text=text,
            reply_markup=Keyboards.menu_principal(),
            parse_mode='Markdown'
        )
    
    @staticmethod
    async def show_farm(query, user):
        """Afficher la ferme"""
        text = f"""🌾 **MA FERME**

👤 **Joueur:** {user['first_name']}
🍋 **Citrons:** {user['balance']:.0f}
📊 **Niveau Ferme:** {user['level']}

💡 **Conseil:** Récolte régulièrement!
"""
        await query.edit_message_text(
            text=text,
            reply_markup=Keyboards.menu_ferme(),
            parse_mode='Markdown'
        )
    
    @staticmethod
    async def harvest_lemons(query, user):
        """Récolter les citrons"""
        harvest_amount = 10 + (user['level'] * 5)
        db.update_balance(user['user_id'], harvest_amount)
        
        text = f"""🎉 **RÉCOLTE!**

✅ Tu as récolté **{harvest_amount}** citrons!

🍋 **Nouveau solde:** {user['balance'] + harvest_amount:.0f}
"""
        await query.edit_message_text(
            text=text,
            reply_markup=Keyboards.menu_ferme(),
            parse_mode='Markdown'
        )
    
    @staticmethod
    async def upgrade_farm(query, user):
        """Upgrade la ferme"""
        cost = 50 * (user['level'] + 1)
        
        if user['balance'] >= cost:
            db.update_balance(user['user_id'], -cost)
            db.update_exp(user['user_id'], 50)
            
            text = f"""🚀 **UPGRADE RÉUSSI!**

✅ Ferme améliorée au niveau {user['level'] + 1}!

💰 **Coût:** {cost} citrons
🍋 **Nouveau solde:** {user['balance'] - cost:.0f}
⚡ **EXP:** +50
"""
        else:
            text = f"""❌ **UPGRADE ÉCHOUÉ**

💰 **Coût:** {cost} citrons
🍋 **Solde actuel:** {user['balance']:.0f}

😢 Tu n'as pas assez de citrons!
"""
        
        await query.edit_message_text(
            text=text,
            reply_markup=Keyboards.menu_ferme(),
            parse_mode='Markdown'
        )
    
    @staticmethod
    async def show_stats(query, user):
        """Afficher les stats"""
        text = f"""📊 **MES STATISTIQUES**

👤 **Joueur:** {user['first_name']}
🍋 **Citrons Total:** {user['balance']:.0f}
📊 **Niveau:** {user['level']}
⚡ **Expérience:** {user['exp']}/1000
📅 **Membre depuis:** {user['created_at']}

🏆 **Progression:** {(user['exp'] % 1000)}%
"""
        await query.edit_message_text(
            text=text,
            reply_markup=Keyboards.back_button(),
            parse_mode='Markdown'
        )
    
    @staticmethod
    async def play_game(query, user):
        """Jouer mini jeu"""
        import random
        
        game_result = random.choice([True, False])
        
        if game_result:
            reward = random.randint(10, 50)
            db.update_balance(user['user_id'], reward)
            text = f"🎮 **MINI JEU**\n\n✅ **GAGNÉ!**\n\n🎉 Tu as remporté {reward} citrons!"
        else:
            text = "🎮 **MINI JEU**\n\n❌ **PERDU!**\n\n😢 Réessaye plus tard!"
        
        await query.edit_message_text(
            text=text,
            reply_markup=Keyboards.menu_principal(),
            parse_mode='Markdown'
        )
    
    @staticmethod
    async def show_shop_equipment(query, user):
        """Afficher le shop équipement"""
        text = """🚜 **ÉQUIPEMENT**

1️⃣ **Pioche Dorée** - 100 🍋
2️⃣ **Tracteur** - 500 🍋
3️⃣ **Robot Fermier** - 2000 🍋

💡 Améliore ta récolte!
"""
        await query.edit_message_text(
            text=text,
            reply_markup=Keyboards.back_button(),
            parse_mode='Markdown'
        )
    
    @staticmethod
    async def show_shop_bonus(query, user):
        """Afficher le shop bonus"""
        text = """💰 **BONUS**

🎁 **Paquet Démarrage** - 50 🍋
📦 **Boîte Mystère** - 200 🍋
👑 **Pack Premium** - 1000 🍋

✨ Éclaire ton expérience!
"""
        await query.edit_message_text(
            text=text,
            reply_markup=Keyboards.back_button(),
            parse_mode='Markdown'
        )
    
    @staticmethod
    async def view_reviews(query):
        """Afficher les avis"""
        reviews = db.get_reviews(limit=5)
        
        if reviews:
            reviews_text = "⭐ **AVIS DES JOUEURS**\n\n"
            for review in reviews:
                stars = "⭐" * review['rating']
                reviews_text += f"\n{stars} **{review['username']}**\n_{review['comment']}_\n"
        else:
            reviews_text = "⭐ **AVIS DES JOUEURS**\n\nPas encore d'avis! Sois le premier à en laisser un!"
        
        await query.edit_message_text(
            text=reviews_text,
            reply_markup=Keyboards.back_button(),
            parse_mode='Markdown'
        )
    
    @staticmethod
    async def handle_review_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gérer le texte de l'avis"""
        user_id = update.effective_user.id
        comment = update.message.text
        
        if 'rating' in context.user_data:
            rating = context.user_data['rating']
            
            if db.add_review(user_id, rating, comment):
                await update.message.reply_text(
                    "✅ **Merci pour ton avis!**\n\n🙏 Nous l'avons bien reçu!",
                    reply_markup=Keyboards.back_button(),
                    parse_mode='Markdown'
                )
                context.user_data.pop('rating', None)
            else:
                await update.message.reply_text(
                    "❌ Erreur lors de l'enregistrement de l'avis.",
                    reply_markup=Keyboards.back_button()
                )

# Export des handlers
handlers_instance = Handlers()
