import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ChatAction
import json
from datetime import datetime

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Token
TOKEN = "8916158056:AAGzi0PvoY2BfEI7rqVc-A7_pj7XihvNIgc"

# Products Database
PRODUCTS = {
    'flower': [
        {'id': 1, 'name': 'OG Kush', 'emoji': '🌸', 'desc': 'Classique puissant', 'price': 45.99},
        {'id': 2, 'name': 'Sativa Mix', 'emoji': '🌿', 'desc': 'Énergisant', 'price': 39.99},
        {'id': 3, 'name': 'Purple Haze', 'emoji': '🌺', 'desc': 'Légendaire', 'price': 52.99},
    ],
    'oil': [
        {'id': 4, 'name': 'CBD Oil 10ml', 'emoji': '🧴', 'desc': '1000mg CBD', 'price': 29.99},
        {'id': 5, 'name': 'Full Spectrum', 'emoji': '🧪', 'desc': 'Effet entourage', 'price': 34.99},
    ],
    'edibles': [
        {'id': 6, 'name': 'Gummies Mix', 'emoji': '🍬', 'desc': '100mg CBD/pièce', 'price': 24.99},
        {'id': 7, 'name': 'Brownie CBD', 'emoji': '🍫', 'desc': 'Artisanal', 'price': 19.99},
    ],
    'vape': [
        {'id': 8, 'name': 'Vape Pen', 'emoji': '💨', 'desc': 'Portable', 'price': 44.99},
        {'id': 9, 'name': 'Cartridge Pack', 'emoji': '🔫', 'desc': '3 saveurs', 'price': 49.99},
    ],
    'accessories': [
        {'id': 10, 'name': 'Grinder Premium', 'emoji': '⚙️', 'desc': 'Aluminium', 'price': 22.99},
        {'id': 11, 'name': 'Storage Pack', 'emoji': '📦', 'desc': '5 pochettes', 'price': 14.99},
    ]
}

# User data storage (in production, use database)
user_data = {}

def get_user_cart(user_id):
    """Get or create user cart"""
    if user_id not in user_data:
        user_data[user_id] = {'cart': [], 'points': 0, 'balance': 0}
    return user_data[user_id]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command"""
    user = update.effective_user
    get_user_cart(user.id)  # Initialize user
    
    welcome_text = f"""🍋🔫 **BIENVENUE SUR LEMONBOT CBD SHOP** 🔫🍋

🍋 Salut {user.first_name}! Bienvenue chez nous!

**Voici ce que tu peux faire:**
/menu - 🛍️ Voir nos produits
/jeux - 🎮 Jouer et gagner des points
/panier - 🛒 Voir ton panier
/commander - ✅ Passer une commande
/aide - ℹ️ Besoin d'aide?

💰 **Promotions:**
✨ -15% sur les huiles
🎉 -20% pour 2+ produits
🚚 Livraison gratuite >$50

**Que veux-tu faire?**"""
    
    keyboard = [
        [InlineKeyboardButton("🛍️ Menu Produits", callback_data='menu'),
         InlineKeyboardButton("🎮 Jeux", callback_data='jeux')],
        [InlineKeyboardButton("🛒 Panier", callback_data='panier'),
         InlineKeyboardButton("ℹ️ Aide", callback_data='aide')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show menu"""
    query = update.callback_query
    await query.answer()
    
    menu_text = """🛍️ **MENU PRODUITS**

Choisissez une catégorie:"""
    
    keyboard = [
        [InlineKeyboardButton("🌸 Fleurs", callback_data='cat_flower'),
         InlineKeyboardButton("🧴 Huiles", callback_data='cat_oil')],
        [InlineKeyboardButton("🍬 Comestibles", callback_data='cat_edibles'),
         InlineKeyboardButton("💨 Vapes", callback_data='cat_vape')],
        [InlineKeyboardButton("⚙️ Accessoires", callback_data='cat_accessories')],
        [InlineKeyboardButton("⬅️ Retour", callback_data='back_main')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(menu_text, reply_markup=reply_markup, parse_mode='Markdown')

async def show_category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show products by category"""
    query = update.callback_query
    await query.answer()
    
    category = query.data.split('_')[1]
    products = PRODUCTS.get(category, [])
    
    if not products:
        await query.edit_message_text("❌ Catégorie introuvable")
        return
    
    text = f"🛍️ **PRODUITS: {category.upper()}**\n\n"
    
    for product in products:
        text += f"{product['emoji']} **{product['name']}**\n"
        text += f"   {product['desc']}\n"
        text += f"   💰 ${product['price']}\n\n"
    
    keyboard = [[InlineKeyboardButton(f"{p['emoji']} {p['name']}", callback_data=f"product_{p['id']}") for p in [products[i] if i < len(products) else None]][i:i+2] for i in range(0, len(products), 2)]
    keyboard.append([InlineKeyboardButton("⬅️ Retour", callback_data='menu')])
    
    # Build keyboard properly
    keyboard = []
    for i in range(0, len(products), 2):
        row = []
        for j in range(2):
            if i+j < len(products):
                p = products[i+j]
                row.append(InlineKeyboardButton(f"{p['emoji']} {p['name']}", callback_data=f"product_{p['id']}"))
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton("⬅️ Retour", callback_data='menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def show_product(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show product details"""
    query = update.callback_query
    await query.answer()
    
    product_id = int(query.data.split('_')[1])
    
    # Find product
    product = None
    for category_products in PRODUCTS.values():
        for p in category_products:
            if p['id'] == product_id:
                product = p
                break
    
    if not product:
        await query.edit_message_text("❌ Produit introuvable")
        return
    
    text = f"""🛍️ **{product['emoji']} {product['name']}**

**Description:** {product['desc']}

💰 **Prix:** ${product['price']}

✨ Premium quality - 100% légal

**Veux-tu ajouter au panier?**"""
    
    keyboard = [
        [InlineKeyboardButton(f"➕ Ajouter (${product['price']})", callback_data=f"add_{product_id}")],
        [InlineKeyboardButton("⬅️ Retour", callback_data='menu')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def add_to_cart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add product to cart"""
    query = update.callback_query
    user_id = query.from_user.id
    
    product_id = int(query.data.split('_')[1])
    
    # Find product
    product = None
    for category_products in PRODUCTS.values():
        for p in category_products:
            if p['id'] == product_id:
                product = p
                break
    
    if not product:
        await query.answer("❌ Produit introuvable", show_alert=True)
        return
    
    # Add to cart
    user_cart = get_user_cart(user_id)
    user_cart['cart'].append(product)
    
    await query.answer(f"✅ {product['name']} ajouté au panier!", show_alert=True)
    
    # Show menu again
    await menu(update, context)

async def show_cart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show cart"""
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    
    user_cart = get_user_cart(user_id)
    cart = user_cart['cart']
    
    if not cart:
        text = "🛒 **TON PANIER EST VIDE**\n\nAjoute des produits!"
        keyboard = [[InlineKeyboardButton("🛍️ Voir Menu", callback_data='menu')]]
    else:
        text = "🛒 **TON PANIER**\n\n"
        total = 0
        for i, product in enumerate(cart, 1):
            text += f"{i}. {product['emoji']} {product['name']} - ${product['price']}\n"
            total += product['price']
        
        text += f"\n💰 **Total:** ${total:.2f}\n\n🎉 +15% offert si tu rejoins nos jeux!"
        
        keyboard = [
            [InlineKeyboardButton("✅ Commander", callback_data='checkout'),
             InlineKeyboardButton("🗑️ Vider", callback_data='clear_cart')],
            [InlineKeyboardButton("➕ Continuer Shopping", callback_data='menu')],
        ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def games(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show games menu"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_cart = get_user_cart(user_id)
    
    text = f"""🎮 **ZONE DE JEUX**

🍋 Gagne des points et des récompenses!

**Tes points actuels:** ⭐ {user_cart['points']}

Choisis un jeu:"""
    
    keyboard = [
        [InlineKeyboardButton("🔥 Clicker Game", callback_data='game_clicker'),
         InlineKeyboardButton("🎡 Lucky Spin", callback_data='game_spin')],
        [InlineKeyboardButton("🧠 Memory", callback_data='game_memory'),
         InlineKeyboardButton("🌱 Grow Plant", callback_data='game_grow')],
        [InlineKeyboardButton("⬅️ Retour", callback_data='back_main')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def start_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start a game"""
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    
    game_type = query.data.split('_')[1]
    user_cart = get_user_cart(user_id)
    
    if game_type == 'clicker':
        text = """🔥 **CLICKER GAME**

⏱️ Clique aussi vite que possible!

Appuie sur le bouton ci-dessous 10 fois aussi vite que tu peux!

⚠️ C'est parti! 3... 2... 1..."""
        context.user_data['clicker_clicks'] = 0
        context.user_data['game_start_time'] = datetime.now()
        keyboard = [[InlineKeyboardButton("👆 CLIC!", callback_data='clicker_click')]]
    
    elif game_type == 'spin':
        text = """🎡 **LUCKY SPIN**

🌟 Tourne la roue et gagne des récompenses!

Chaque spin te donne une chance de gagner! 🍀"""
        keyboard = [[InlineKeyboardButton("🎡 SPINNER!", callback_data='spin_wheel')]]
    
    elif game_type == 'memory':
        text = """🧠 **MEMORY GAME**

🎯 Trouve les paires!

J'ai caché 4 paires. Clique pour les révéler!

🎮 C'est parti!"""
        context.user_data['memory_revealed'] = []
        keyboard = [
            [InlineKeyboardButton("🎮 Card 1", callback_data='mem_1'),
             InlineKeyboardButton("🎮 Card 2", callback_data='mem_2')],
            [InlineKeyboardButton("🎮 Card 3", callback_data='mem_3'),
             InlineKeyboardButton("🎮 Card 4", callback_data='mem_4')],
        ]
    
    else:  # grow
        text = """🌱 **CULTIVER TA PLANTE**

🌿 Prends soin de ta plante!

Arrose-la et donne-lui du soleil pour la faire croître.

Atteins 100% de croissance pour gagner 20 points! 🎉"""
        context.user_data['plant_growth'] = 0
        keyboard = [
            [InlineKeyboardButton("💧 Arroser (+10%)", callback_data='grow_water'),
             InlineKeyboardButton("☀️ Soleil (+15%)", callback_data='grow_sun')],
            [InlineKeyboardButton("📊 Voir Croissance", callback_data='grow_check')],
        ]
    
    keyboard.append([InlineKeyboardButton("⬅️ Retour aux Jeux", callback_data='jeux')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def clicker_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle clicker game clicks"""
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    
    if 'clicker_clicks' not in context.user_data:
        context.user_data['clicker_clicks'] = 0
    
    context.user_data['clicker_clicks'] += 1
    clicks = context.user_data['clicker_clicks']
    
    if clicks >= 10:
        user_cart = get_user_cart(user_id)
        points_earned = 10
        user_cart['points'] += points_earned
        
        text = f"""🎉 **PARTIE TERMINÉE!**

👆 Vous avez cliqué: {clicks} fois!

⭐ Points gagnés: +{points_earned}

**Votre score total:** ⭐ {user_cart['points']}

🏆 Excellent! Vous êtes un champion du clic!"""
        
        keyboard = [[InlineKeyboardButton("🔄 Rejouer", callback_data='game_clicker'),
                     InlineKeyboardButton("🎮 Autres Jeux", callback_data='jeux')]]
    else:
        text = f"🔥 **CLICKER GAME**\n\n👆 Clics: {clicks}/10\n\nContinue!"
        keyboard = [[InlineKeyboardButton("👆 CLIC!", callback_data='clicker_click')]]
    
    keyboard.append([InlineKeyboardButton("⬅️ Retour aux Jeux", callback_data='jeux')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def spin_wheel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle spin wheel"""
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    
    import random
    
    rewards = [
        {'emoji': '🎁', 'points': 5, 'text': 'Petit gain!'},
        {'emoji': '🌟', 'points': 15, 'text': 'Bonus moyen!'},
        {'emoji': '🎉', 'points': 30, 'text': 'Jackpot!!!'},
        {'emoji': '😢', 'points': 0, 'text': 'Rien cette fois...'},
        {'emoji': '💫', 'points': 10, 'text': 'Beau gain!'},
        {'emoji': '👑', 'points': 25, 'text': 'Super bonus!'},
    ]
    
    reward = random.choice(rewards)
    user_cart = get_user_cart(user_id)
    user_cart['points'] += reward['points']
    
    text = f"""🎡 **ROUE TOURNE...**

{reward['emoji']} {reward['text']}

⭐ Points gagnés: +{reward['points']}

**Votre score:** ⭐ {user_cart['points']}

🍀 Bonne chance!"""
    
    keyboard = [[InlineKeyboardButton("🔄 Rejouer", callback_data='game_spin'),
                 InlineKeyboardButton("🎮 Autres Jeux", callback_data='jeux')]]
    keyboard.append([InlineKeyboardButton("⬅️ Retour aux Jeux", callback_data='jeux')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def grow_water(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Water the plant"""
    query = update.callback_query
    await query.answer()
    
    if 'plant_growth' not in context.user_data:
        context.user_data['plant_growth'] = 0
    
    context.user_data['plant_growth'] += 10
    growth = context.user_data['plant_growth']
    
    stages = ['🌱', '🌿', '🍀', '🌳']
    stage = min(int(growth / 30), 3)
    
    text = f"""🌱 **CULTIVER TA PLANTE**

{stages[stage]} Croissance: {growth}%

💧 Tu as arrosé la plante!"""
    
    if growth >= 100:
        user_id = query.from_user.id
        user_cart = get_user_cart(user_id)
        user_cart['points'] += 20
        text += f"\n\n🎉 **PLANTE PRÊTE!**\n⭐ +20 points!\n**Score total:** {user_cart['points']}"
    
    keyboard = [
        [InlineKeyboardButton("💧 Arroser (+10%)", callback_data='grow_water'),
         InlineKeyboardButton("☀️ Soleil (+15%)", callback_data='grow_sun')],
        [InlineKeyboardButton("🔄 Recommencer", callback_data='game_grow'),
         InlineKeyboardButton("🎮 Autres Jeux", callback_data='jeux')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def grow_sun(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Give sun to plant"""
    query = update.callback_query
    await query.answer()
    
    if 'plant_growth' not in context.user_data:
        context.user_data['plant_growth'] = 0
    
    context.user_data['plant_growth'] += 15
    growth = context.user_data['plant_growth']
    
    stages = ['🌱', '🌿', '🍀', '🌳']
    stage = min(int(growth / 30), 3)
    
    text = f"""🌱 **CULTIVER TA PLANTE**

{stages[stage]} Croissance: {growth}%

☀️ Tu as donné du soleil!"""
    
    if growth >= 100:
        user_id = query.from_user.id
        user_cart = get_user_cart(user_id)
        user_cart['points'] += 20
        text += f"\n\n🎉 **PLANTE PRÊTE!**\n⭐ +20 points!\n**Score total:** {user_cart['points']}"
    
    keyboard = [
        [InlineKeyboardButton("💧 Arroser (+10%)", callback_data='grow_water'),
         InlineKeyboardButton("☀️ Soleil (+15%)", callback_data='grow_sun')],
        [InlineKeyboardButton("🔄 Recommencer", callback_data='game_grow'),
         InlineKeyboardButton("🎮 Autres Jeux", callback_data='jeux')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Help command"""
    query = update.callback_query
    await query.answer()
    
    text = """ℹ️ **AIDE & SUPPORT**

**🛍️ MENU PRODUITS**
Vois tous nos produits CBD premium

**🎮 JEUX**
Joue et accumule des points!
Gagne des bonus sur tes achats!

**🛒 PANIER**
Gère ton panier d'achats

**✅ COMMANDER**
Passe ta commande maintenant

**💬 CONTACT**
Besoin d'aide? Contacte @LemonBot_Support

📞 Support 24/7
💳 Paiement sécurisé
🚚 Livraison rapide

🍋 Merci d'être avec nous!"""
    
    keyboard = [[InlineKeyboardButton("⬅️ Retour", callback_data='back_main')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def back_main(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Go back to main menu"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    welcome_text = f"""🍋🔫 **LEMONBOT CBD SHOP** 🔫🍋

**Que veux-tu faire?**"""
    
    keyboard = [
        [InlineKeyboardButton("🛍️ Menu", callback_data='menu'),
         InlineKeyboardButton("🎮 Jeux", callback_data='jeux')],
        [InlineKeyboardButton("🛒 Panier", callback_data='panier'),
         InlineKeyboardButton("ℹ️ Aide", callback_data='aide')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def checkout(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Checkout"""
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    
    user_cart = get_user_cart(user_id)
    
    if not user_cart['cart']:
        text = "🛒 Ton panier est vide!"
        keyboard = [[InlineKeyboardButton("🛍️ Voir Menu", callback_data='menu')]]
    else:
        total = sum(p['price'] for p in user_cart['cart'])
        text = f"""✅ **COMMANDE CONFIRMÉE!**

🍋 Merci d'avoir choisi LEMONBOT CBD SHOP!

💰 **Total:** ${total:.2f}
⭐ **Points gagnés:** +{len(user_cart['cart'])}

📍 Livraison prévue en 2-3 jours

🎉 Merci pour ton achat!"""
        
        user_cart['cart'] = []
        keyboard = [[InlineKeyboardButton("🛍️ Continuer Shopping", callback_data='menu')]]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def clear_cart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Clear cart"""
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer("🗑️ Panier vidé!", show_alert=True)
    
    user_cart = get_user_cart(user_id)
    user_cart['cart'] = []
    
    await show_cart(update, context)

def main():
    """Start the bot"""
    application = Application.builder().token(TOKEN).build()
    
    # Command handlers
    application.add_handler(CommandHandler("start", start))
    
    # Callback handlers
    application.add_handler(CallbackQueryHandler(menu, pattern='^menu$'))
    application.add_handler(CallbackQueryHandler(show_category, pattern='^cat_'))
    application.add_handler(CallbackQueryHandler(show_product, pattern='^product_'))
    application.add_handler(CallbackQueryHandler(add_to_cart, pattern='^add_'))
    application.add_handler(CallbackQueryHandler(show_cart, pattern='^panier$'))
    application.add_handler(CallbackQueryHandler(games, pattern='^jeux$'))
    application.add_handler(CallbackQueryHandler(start_game, pattern='^game_'))
    application.add_handler(CallbackQueryHandler(clicker_click, pattern='^clicker_click$'))
    application.add_handler(CallbackQueryHandler(spin_wheel, pattern='^spin_wheel$'))
    application.add_handler(CallbackQueryHandler(grow_water, pattern='^grow_water$'))
    application.add_handler(CallbackQueryHandler(grow_sun, pattern='^grow_sun$'))
    application.add_handler(CallbackQueryHandler(help_command, pattern='^aide$'))
    application.add_handler(CallbackQueryHandler(back_main, pattern='^back_main$'))
    application.add_handler(CallbackQueryHandler(checkout, pattern='^checkout$'))
    application.add_handler(CallbackQueryHandler(clear_cart, pattern='^clear_cart$'))
    
    # Start bot
    print("🤖 BOT TELEGRAM EN LIGNE!")
    print("🍋 LEMONBOT CBD SHOP")
    print("⚙️ Connecté...")
    
    application.run_polling()

if __name__ == '__main__':
    main()
