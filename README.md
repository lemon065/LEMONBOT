# 🍋 LEMONBOT - Bot Telegram

**Le meilleur bot Telegram pour cultiver des citrons!**

![Logo LEMONBOT](file_00000000f32071f48c90fbb8b078d1a0.png)

## 🎯 Fonctionnalités

✅ **Menu interactif** - Interface facile et intuitive  
✅ **Système de ferme** - Cultive et récolte tes citrons  
✅ **Système d'avis** - Laisse ton avis (1-5 étoiles)  
✅ **Shop complet** - Achète des upgrades et des bonus  
✅ **Statistiques** - Suivi de ta progression  
✅ **Mini-jeux** - Gagne des récompenses  
✅ **Système de niveau** - Progressez et débloquez du contenu  

## 🚀 Installation

### Prérequis
- Python 3.9+
- pip (gestionnaire de paquets Python)
- Un token Telegram Bot (obtenu via @BotFather)

### Étapes

1. **Cloner le repo**
```bash
git clone https://github.com/lemon065/LEMONBOT.git
cd LEMONBOT
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer le bot**
```bash
cp .env.example .env
# Éditer .env et ajouter ton token Telegram
```

5. **Lancer le bot**
```bash
python main.py
```

## 📱 Utilisation

### Commandes
- `/start` - Démarrer le bot
- `/help` - Afficher l'aide
- `/stats` - Voir les statistiques

### Menu Principal

- 🎮 **Jouer** - Joue à des mini-jeux et gagne des citrons
- 🌾 **Ma Ferme** - Gère ta ferme et récolte tes citrons
- 📊 **Stats** - Vois ta progression
- 🛍️ **Shop** - Achète des équipements et des bonus
- ⭐ **Avis** - Vois les avis et laisse ton note
- ⚙️ **Paramètres** - Configure le bot
- 💬 **Support** - Nous contacter
- ℹ️ **Infos** - À propos de LEMONBOT

## 🗄️ Structure du Projet

```
LEMONBOT/
├── main.py              # Point d'entrée principal
├── config.py            # Configuration du bot
├── database.py          # Gestion de la base de données
├── keyboards.py         # Claviers et boutons
├── handlers.py          # Gestionnaires d'événements
├── requirements.txt     # Dépendances Python
├── .env.example         # Template d'environnement
├── .gitignore           # Fichiers à ignorer
└── README.md            # Ce fichier
```

## 📊 Architecture

### Base de Données
Le bot utilise SQLite avec les tables suivantes:

- **users** - Informations des joueurs
- **reviews** - Avis et évaluations
- **farm** - Données de la ferme
- **inventory** - Inventaire du joueur
- **statistics** - Statistiques globales

### Workflow

```
Utilisateur -> Message/Bouton -> Handler
                                   ↓
                            Base de Données
                                   ↓
                          Réponse avec Menu
```

## 🔐 Sécurité

- ✅ Variables d'environnement pour les tokens
- ✅ Base de données locale (SQLite)
- ✅ Validation des entrées
- ✅ Gestion des erreurs

## 🛠️ Développement

### Ajouter une nouvelle fonctionnalité

1. Créer une nouvelle méthode dans `Handlers`
2. Ajouter les boutons correspondants dans `keyboards.py`
3. Ajouter le callback handler dans `button_callback`
4. Tester le bot

### Exemple: Ajouter un bouton

```python
# Dans keyboards.py
InlineKeyboardButton("🎨 Nouvelle Fonction", callback_data='new_function')

# Dans handlers.py
elif callback_data == 'new_function':
    await Handlers.new_function(query, user)

@staticmethod
async def new_function(query, user):
    text = "Ma nouvelle fonction!"
    await query.edit_message_text(text=text, ...)
```

## 📝 Licence

Ce projet est ouvert à la contribution!

## 👨‍💻 Auteur

**lemon065** - [GitHub](https://github.com/lemon065)

## 📞 Support

Un problème? Des suggestions?
- 📧 Email: support@lemonbot.com
- 💬 Telegram: Utilisez le bouton "Support" dans le bot

---

**Made with ❤️ for farming lemons** 🍋
