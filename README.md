# FlixStream - Backend API

Backend Flask pour le système d'abonnement IPTV FlixStream.

## 🚀 Fonctionnalités

- **Gestion des abonnements** : Création, consultation et renouvellement automatique
- **Base de données SQLite** : Stockage sécurisé de toutes les informations clients
- **API RESTful** : Endpoints pour toutes les opérations
- **Intégration API Dino** : Création automatique des comptes IPTV
- **Statistiques** : Dashboard pour suivre les abonnements
- **Système de relance** : Détection automatique des abonnements à renouveler

## 📋 Prérequis

- Python 3.11+
- pip

## 🔧 Installation

1. **Cloner le repository**
```bash
git clone <votre-repo>
cd flixstream_backend
```

2. **Créer et activer l'environnement virtuel**
```bash
python3.11 -m venv venv
source venv/bin/activate  # Sur Linux/Mac
# ou
venv\Scripts\activate  # Sur Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer les variables d'environnement**

Créez un fichier `.env` à la racine du projet :
```
DINO_API_URL=https://votre-panel-dino.com/api
DINO_API_KEY=votre_cle_api_ici
SECRET_KEY=votre_cle_secrete_flask
```

## 🏃 Démarrage

```bash
source venv/bin/activate
python src/main.py
```

Le serveur démarre sur `http://localhost:5000`

## 📡 Endpoints API

### Créer un abonnement
```
POST /api/subscribe
Content-Type: application/json

{
  "fullName": "Jean Dupont",
  "email": "jean@example.com",
  "phone": "+33612345678",
  "contactMethod": "whatsapp",
  "plan": {
    "id": "12months",
    "name": "12 Mois",
    "price": "59.99€",
    "duration": "12 mois"
  }
}
```

### Récupérer tous les abonnements
```
GET /api/subscriptions
```

### Récupérer un abonnement spécifique
```
GET /api/subscriptions/<id>
```

### Récupérer les abonnements qui expirent bientôt
```
GET /api/subscriptions/expiring
```

### Renouveler un abonnement
```
POST /api/subscriptions/<id>/renew
```

### Obtenir les statistiques
```
GET /api/stats
```

## 🗄️ Structure de la base de données

### Table `subscriptions`

| Champ | Type | Description |
|-------|------|-------------|
| id | Integer | Identifiant unique |
| full_name | String(200) | Nom complet du client |
| email | String(200) | Email du client |
| phone | String(50) | Numéro de téléphone |
| contact_method | String(20) | whatsapp ou telegram |
| plan_id | String(50) | ID du plan (3months, 6months, 12months) |
| plan_name | String(50) | Nom du plan |
| plan_price | String(20) | Prix du plan |
| plan_duration | String(50) | Durée du plan |
| status | String(20) | pending, active, expired |
| created_at | DateTime | Date de création |
| expires_at | DateTime | Date d'expiration |
| iptv_username | String(100) | Nom d'utilisateur IPTV |
| iptv_password | String(100) | Mot de passe IPTV |
| iptv_url | String(200) | URL du serveur IPTV |

## 🔌 Configuration de l'API Dino

La fonction `create_iptv_account()` dans `src/routes/subscription.py` doit être adaptée selon la documentation de votre API Dino Panel.

**Exemple de configuration typique :**

```python
def create_iptv_account(plan_id, full_name, email):
    duration_days = {
        '3months': 90,
        '6months': 180,
        '12months': 365
    }
    
    days = duration_days.get(plan_id, 90)
    
    payload = {
        'username': f"user_{datetime.now().timestamp()}",
        'password': f"pass_{datetime.now().timestamp()}",
        'email': email,
        'full_name': full_name,
        'duration': days,
        'max_connections': 1,
        'is_trial': False
    }
    
    headers = {
        'Authorization': f'Bearer {DINO_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(
        f'{DINO_API_URL}/create_user',
        json=payload,
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        return {
            'username': data.get('username'),
            'password': data.get('password'),
            'url': data.get('server_url'),
            'expires_at': datetime.now() + timedelta(days=days)
        }
    
    return None
```

## 📊 Accès à la base de données

La base de données SQLite se trouve dans `src/database/app.db`.

**Pour consulter les données :**

```bash
sqlite3 src/database/app.db
```

**Commandes SQL utiles :**

```sql
-- Voir tous les abonnements
SELECT * FROM subscriptions;

-- Voir les abonnements actifs
SELECT * FROM subscriptions WHERE status = 'active';

-- Voir les abonnements qui expirent bientôt
SELECT * FROM subscriptions 
WHERE expires_at <= datetime('now', '+30 days') 
AND status = 'active';

-- Statistiques par plan
SELECT plan_name, COUNT(*) as count 
FROM subscriptions 
GROUP BY plan_name;
```

## 🔄 Système de relance automatique

Pour mettre en place un système de relance automatique des clients dont l'abonnement expire bientôt :

1. Créez un script cron qui appelle l'endpoint `/api/subscriptions/expiring`
2. Pour chaque abonnement retourné, envoyez un message WhatsApp/Telegram au client
3. Utilisez l'endpoint `/api/subscriptions/<id>/renew` pour renouveler après paiement

**Exemple de script Python pour les relances :**

```python
import requests
from datetime import datetime

# Récupérer les abonnements qui expirent
response = requests.get('http://localhost:5000/api/subscriptions/expiring')
subscriptions = response.json()['subscriptions']

for sub in subscriptions:
    # Envoyer un message de relance
    message = f"""
    Bonjour {sub['full_name']},
    
    Votre abonnement FlixStream expire le {sub['expires_at']}.
    
    Pour renouveler, contactez-nous !
    """
    
    # Envoyer via WhatsApp/Telegram API
    # send_message(sub['phone'], message, sub['contact_method'])
```

## 🔒 Sécurité

- **Ne jamais commiter** le fichier `.env` ou les clés API
- **Changer** la `SECRET_KEY` en production
- **Utiliser HTTPS** en production
- **Limiter** les accès à la base de données
- **Valider** toutes les entrées utilisateur

## 📦 Déploiement

Pour déployer en production, vous pouvez utiliser :
- **Heroku**
- **DigitalOcean**
- **AWS**
- **VPS avec Nginx + Gunicorn**

## 📝 Licence

Tous droits réservés © 2025 FlixStream

