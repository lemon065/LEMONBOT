from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import EMOJIS

class Keyboards:
    @staticmethod
    def menu_principal():
        """Clavier du menu principal"""
        keyboard = [
            [
                InlineKeyboardButton(f"{EMOJIS['play']} Jouer", callback_data='play'),
                InlineKeyboardButton(f"{EMOJIS['farm']} Ma Ferme", callback_data='farm'),
            ],
            [
                InlineKeyboardButton(f"{EMOJIS['stats']} Stats", callback_data='stats'),
                InlineKeyboardButton(f"{EMOJIS['shop']} Shop", callback_data='shop'),
            ],
            [
                InlineKeyboardButton(f"{EMOJIS['reviews']} Avis (⭐)", callback_data='reviews'),
                InlineKeyboardButton(f"{EMOJIS['settings']} Paramètres", callback_data='settings'),
            ],
            [
                InlineKeyboardButton(f"{EMOJIS['support']} Support", callback_data='support'),
                InlineKeyboardButton(f"{EMOJIS['info']} Infos", callback_data='info'),
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def menu_ferme():
        """Clavier du menu ferme"""
        keyboard = [
            [
                InlineKeyboardButton(f"{EMOJIS['lemon']} Récolter", callback_data='harvest'),
                InlineKeyboardButton(f"{EMOJIS['next']} Upgrade", callback_data='upgrade_farm'),
            ],
            [
                InlineKeyboardButton(f"{EMOJIS['back']} Retour", callback_data='back_menu'),
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def menu_reviews():
        """Clavier du menu avis"""
        keyboard = [
            [
                InlineKeyboardButton(f"{EMOJIS['check']} Voir les avis", callback_data='view_reviews'),
                InlineKeyboardButton(f"✍️ Laisser un avis", callback_data='write_review'),
            ],
            [
                InlineKeyboardButton(f"{EMOJIS['back']} Retour", callback_data='back_menu'),
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def rating_buttons():
        """Clavier pour évaluer (1-5 étoiles)"""
        keyboard = [
            [
                InlineKeyboardButton("⭐", callback_data='rate_1'),
                InlineKeyboardButton("⭐⭐", callback_data='rate_2'),
                InlineKeyboardButton("⭐⭐⭐", callback_data='rate_3'),
            ],
            [
                InlineKeyboardButton("⭐⭐⭐⭐", callback_data='rate_4'),
                InlineKeyboardButton("⭐⭐⭐⭐⭐", callback_data='rate_5'),
            ],
            [
                InlineKeyboardButton(f"{EMOJIS['back']} Annuler", callback_data='back_menu'),
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def menu_shop():
        """Clavier du shop"""
        keyboard = [
            [
                InlineKeyboardButton("🚜 Équipement", callback_data='shop_equipment'),
                InlineKeyboardButton("💰 Bonus", callback_data='shop_bonus'),
            ],
            [
                InlineKeyboardButton(f"{EMOJIS['back']} Retour", callback_data='back_menu'),
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def menu_settings():
        """Clavier des paramètres"""
        keyboard = [
            [
                InlineKeyboardButton("🔔 Notifications", callback_data='notifications'),
                InlineKeyboardButton("🌍 Langue", callback_data='language'),
            ],
            [
                InlineKeyboardButton(f"{EMOJIS['back']} Retour", callback_data='back_menu'),
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def back_button():
        """Bouton retour simple"""
        keyboard = [[
            InlineKeyboardButton(f"{EMOJIS['back']} Retour", callback_data='back_menu'),
        ]]
        return InlineKeyboardMarkup(keyboard)
