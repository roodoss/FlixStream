from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from src.models.subscription import db, Subscription
from src.utils.email_sender import send_subscription_email, send_renewal_reminder_email
import requests
import os

subscription_bp = Blueprint('subscription', __name__)

# Configuration de l'API Dino (à personnaliser avec vos vraies informations)
DINO_API_URL = os.environ.get('DINO_API_URL', 'https://your-dino-panel.com/api')
DINO_API_KEY = os.environ.get('DINO_API_KEY', 'your_api_key_here')

def create_iptv_account(plan_id, full_name, email):
    """
    Crée un compte IPTV via l'API Dino
    Cette fonction doit être adaptée selon la documentation de votre API Dino
    """
    # Déterminer la durée en jours selon le plan
    duration_days = {
        '3months': 90,
        '6months': 180,
        '12months': 365
    }
    
    days = duration_days.get(plan_id, 90)
    
    # Exemple de requête à l'API Dino (à adapter selon votre API)
    # Ceci est un exemple générique, vous devrez l'adapter
    try:
        # Format de données typique pour une API IPTV
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
        
        # Décommentez et adaptez cette section quand vous aurez les vraies infos API
        # response = requests.post(f'{DINO_API_URL}/create_user', json=payload, headers=headers)
        # if response.status_code == 200:
        #     data = response.json()
        #     return {
        #         'username': data.get('username'),
        #         'password': data.get('password'),
        #         'url': data.get('server_url'),
        #         'expires_at': datetime.now() + timedelta(days=days)
        #     }
        
        # Pour le moment, retourne des données de test
        # REMPLACEZ CECI par l'appel API réel
        return {
            'username': payload['username'],
            'password': payload['password'],
            'url': 'http://your-server.com:8080',
            'expires_at': datetime.now() + timedelta(days=days)
        }
        
    except Exception as e:
        print(f"Erreur lors de la création du compte IPTV: {str(e)}")
        return None

@subscription_bp.route('/subscribe', methods=['POST'])
def subscribe():
    """
    Endpoint pour créer un nouvel abonnement
    """
    try:
        data = request.get_json()
        
        # Validation des données
        required_fields = ['fullName', 'email', 'phone', 'contactMethod', 'plan']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Le champ {field} est requis'}), 400
        
        plan = data['plan']
        
        # Créer le compte IPTV via l'API Dino
        iptv_account = create_iptv_account(
            plan['id'],
            data['fullName'],
            data['email']
        )
        
        if not iptv_account:
            return jsonify({'error': 'Erreur lors de la création du compte IPTV'}), 500
        
        # Créer l'abonnement dans la base de données
        subscription = Subscription(
            full_name=data['fullName'],
            email=data['email'],
            phone=data['phone'],
            contact_method=data['contactMethod'],
            plan_id=plan['id'],
            plan_name=plan['name'],
            plan_price=plan['price'],
            plan_duration=plan['duration'],
            status='active',
            iptv_username=iptv_account['username'],
            iptv_password=iptv_account['password'],
            iptv_url=iptv_account['url'],
            expires_at=iptv_account['expires_at']
        )
        
        db.session.add(subscription)
        db.session.commit()
        
        # Envoyer l'email avec les informations de connexion
        send_subscription_email(
            recipient_email=data['email'],
            full_name=data['fullName'],
            plan_name=plan['name'],
            iptv_credentials={
                'username': iptv_account['username'],
                'password': iptv_account['password'],
                'url': iptv_account['url']
            }
        )
        
        return jsonify({
            'success': True,
            'message': 'Abonnement créé avec succès',
            'subscription_id': subscription.id,
            'credentials': {
                'username': iptv_account['username'],
                'password': iptv_account['password'],
                'url': iptv_account['url']
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Erreur: {str(e)}")
        return jsonify({'error': 'Une erreur est survenue'}), 500

@subscription_bp.route('/subscriptions', methods=['GET'])
def get_subscriptions():
    """
    Endpoint pour récupérer tous les abonnements
    """
    try:
        subscriptions = Subscription.query.order_by(Subscription.created_at.desc()).all()
        return jsonify({
            'success': True,
            'subscriptions': [sub.to_dict() for sub in subscriptions]
        }), 200
    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({'error': 'Une erreur est survenue'}), 500

@subscription_bp.route('/subscriptions/<int:subscription_id>', methods=['GET'])
def get_subscription(subscription_id):
    """
    Endpoint pour récupérer un abonnement spécifique
    """
    try:
        subscription = Subscription.query.get(subscription_id)
        if not subscription:
            return jsonify({'error': 'Abonnement non trouvé'}), 404
        
        return jsonify({
            'success': True,
            'subscription': subscription.to_dict()
        }), 200
    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({'error': 'Une erreur est survenue'}), 500

@subscription_bp.route('/subscriptions/expiring', methods=['GET'])
def get_expiring_subscriptions():
    """
    Endpoint pour récupérer les abonnements qui expirent bientôt (dans les 30 jours)
    Utile pour les relances automatiques
    """
    try:
        thirty_days_from_now = datetime.now() + timedelta(days=30)
        subscriptions = Subscription.query.filter(
            Subscription.expires_at <= thirty_days_from_now,
            Subscription.status == 'active'
        ).all()
        
        return jsonify({
            'success': True,
            'count': len(subscriptions),
            'subscriptions': [sub.to_dict() for sub in subscriptions]
        }), 200
    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({'error': 'Une erreur est survenue'}), 500

@subscription_bp.route('/subscriptions/<int:subscription_id>/renew', methods=['POST'])
def renew_subscription(subscription_id):
    """
    Endpoint pour renouveler un abonnement
    """
    try:
        subscription = Subscription.query.get(subscription_id)
        if not subscription:
            return jsonify({'error': 'Abonnement non trouvé'}), 404
        
        # Créer un nouveau compte IPTV
        iptv_account = create_iptv_account(
            subscription.plan_id,
            subscription.full_name,
            subscription.email
        )
        
        if not iptv_account:
            return jsonify({'error': 'Erreur lors du renouvellement'}), 500
        
        # Mettre à jour l'abonnement
        subscription.iptv_username = iptv_account['username']
        subscription.iptv_password = iptv_account['password']
        subscription.iptv_url = iptv_account['url']
        subscription.expires_at = iptv_account['expires_at']
        subscription.status = 'active'
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Abonnement renouvelé avec succès',
            'subscription': subscription.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Erreur: {str(e)}")
        return jsonify({'error': 'Une erreur est survenue'}), 500

@subscription_bp.route('/stats', methods=['GET'])
def get_stats():
    """
    Endpoint pour obtenir des statistiques sur les abonnements
    """
    try:
        total_subscriptions = Subscription.query.count()
        active_subscriptions = Subscription.query.filter_by(status='active').count()
        pending_subscriptions = Subscription.query.filter_by(status='pending').count()
        expired_subscriptions = Subscription.query.filter_by(status='expired').count()
        
        # Statistiques par plan
        plans_stats = db.session.query(
            Subscription.plan_name,
            db.func.count(Subscription.id)
        ).group_by(Subscription.plan_name).all()
        
        return jsonify({
            'success': True,
            'stats': {
                'total': total_subscriptions,
                'active': active_subscriptions,
                'pending': pending_subscriptions,
                'expired': expired_subscriptions,
                'by_plan': {plan: count for plan, count in plans_stats}
            }
        }), 200
    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({'error': 'Une erreur est survenue'}), 500

