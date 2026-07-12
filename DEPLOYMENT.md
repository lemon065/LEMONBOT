# 🚀 Guide de Déploiement - LEMONBOT

## Options de Déploiement

### Option 1: Déploiement Local

```bash
# 1. Cloner le repo
git clone https://github.com/lemon065/LEMONBOT.git
cd LEMONBOT

# 2. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer .env
cp .env.example .env
# Ajouter ton TOKEN

# 5. Lancer le bot
python main.py
```

### Option 2: Docker

```bash
# 1. Build l'image
docker build -t lemonbot:latest .

# 2. Lancer le container
docker run -e TELEGRAM_BOT_TOKEN=your_token -d lemonbot:latest
```

### Option 3: Docker Compose

```bash
# 1. Configurer .env avec ton token
echo "TELEGRAM_BOT_TOKEN=your_token" > .env

# 2. Lancer
docker-compose up -d

# 3. Voir les logs
docker-compose logs -f
```

### Option 4: Hébergement Cloud (Heroku, Render, Railway)

#### Heroku
```bash
# 1. Installer Heroku CLI
# 2. Se connecter
heroku login

# 3. Créer une app
heroku create lemonbot

# 4. Ajouter le token
heroku config:set TELEGRAM_BOT_TOKEN=your_token

# 5. Ajouter Procfile
echo "worker: python main.py" > Procfile

# 6. Déployer
git push heroku main
```

#### Render
1. Connecter ton GitHub
2. Créer un nouveau "Background Worker"
3. Sélectionner ton repo LEMONBOT
4. Build command: `pip install -r requirements.txt`
5. Start command: `python main.py`
6. Ajouter les variables d'environnement
7. Déployer!

#### Railway
1. Connecter GitHub sur https://railway.app
2. Créer un nouveau projet
3. Ajouter les variables d'environnement
4. Déployer!

## 🔒 Obtenir le Token Telegram

1. Ouvre Telegram
2. Cherche **@BotFather**
3. Envoie `/newbot`
4. Suis les instructions
5. Copie le token
6. Ajoute-le à `.env` ou aux variables d'environnement

## 📊 Monitoring

### Logs locaux
```bash
python main.py 2>&1 | tee lemonbot.log
```

### Logs Docker
```bash
docker logs -f lemonbot
```

### Logs Docker Compose
```bash
docker-compose logs -f
```

## 🔧 Troubleshooting

### Bot ne démarre pas
- Vérifier le token dans `.env`
- Vérifier la connexion internet
- Vérifier les logs

### Erreur de base de données
- Supprimer `lemonbot.db` et relancer
- Vérifier les permissions du dossier

### Port déjà utilisé
```bash
# Trouver le processus
lsof -i :5000

# Tuer le processus
kill -9 <PID>
```

## 📈 Scaling

Pour augmenter la capacité:
- Utiliser une base de données (PostgreSQL, MongoDB)
- Ajouter une queue de jobs (Redis, RabbitMQ)
- Utiliser webhooks au lieu de polling

---

**Besoin d'aide?** Crée une issue sur GitHub! 🍋
