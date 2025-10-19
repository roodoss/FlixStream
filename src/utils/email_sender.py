import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_subscription_email(recipient_email, full_name, plan_name, iptv_credentials):
    """
    Envoie un email avec les informations d'abonnement IPTV
    
    Args:
        recipient_email: Email du destinataire
        full_name: Nom complet du client
        plan_name: Nom du plan d'abonnement
        iptv_credentials: Dictionnaire contenant username, password, url
    """
    
    # Configuration SMTP (à adapter selon votre fournisseur)
    smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('SMTP_PORT', '587'))
    smtp_username = os.environ.get('SMTP_USERNAME', '')
    smtp_password = os.environ.get('SMTP_PASSWORD', '')
    sender_email = os.environ.get('SENDER_EMAIL', smtp_username)
    
    # Si les variables d'environnement ne sont pas configurées, on simule l'envoi
    if not smtp_username or not smtp_password:
        print(f"[SIMULATION] Email envoyé à {recipient_email}")
        print(f"Nom: {full_name}")
        print(f"Plan: {plan_name}")
        print(f"Credentials: {iptv_credentials}")
        return True
    
    try:
        # Créer le message
        message = MIMEMultipart("alternative")
        message["Subject"] = f"🎬 Votre abonnement FlixStream - {plan_name}"
        message["From"] = sender_email
        message["To"] = recipient_email
        
        # Contenu texte brut
        text_content = f"""
Bonjour {full_name},

Merci d'avoir choisi FlixStream !

Votre abonnement {plan_name} a été activé avec succès.

Voici vos informations de connexion :

URL du serveur : {iptv_credentials['url']}
Nom d'utilisateur : {iptv_credentials['username']}
Mot de passe : {iptv_credentials['password']}

COMMENT UTILISER VOS CODES :

1. Téléchargez une application IPTV sur votre appareil :
   - IPTV Smarters Pro (Recommandée)
   - TiviMate
   - Perfect Player

2. Ouvrez l'application et sélectionnez "Login with Xtream Codes API"

3. Entrez les informations ci-dessus

4. Profitez de votre contenu !

BESOIN D'AIDE ?

Si vous rencontrez des difficultés, n'hésitez pas à nous contacter via WhatsApp ou Telegram.

Cordialement,
L'équipe FlixStream

---
© 2025 FlixStream - Service IPTV Premium
"""
        
        # Contenu HTML
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background: linear-gradient(135deg, #1e3a8a 0%, #7c3aed 100%);
            color: white;
            padding: 30px;
            text-align: center;
            border-radius: 10px 10px 0 0;
        }}
        .content {{
            background: #f8fafc;
            padding: 30px;
            border-radius: 0 0 10px 10px;
        }}
        .credentials {{
            background: white;
            border-left: 4px solid #3b82f6;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
        }}
        .credentials-item {{
            margin: 10px 0;
            padding: 10px;
            background: #f1f5f9;
            border-radius: 5px;
        }}
        .credentials-label {{
            font-weight: bold;
            color: #1e40af;
        }}
        .credentials-value {{
            font-family: monospace;
            color: #0f172a;
            font-size: 14px;
        }}
        .steps {{
            background: white;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
        }}
        .step {{
            margin: 15px 0;
            padding-left: 30px;
            position: relative;
        }}
        .step::before {{
            content: "✓";
            position: absolute;
            left: 0;
            color: #10b981;
            font-weight: bold;
            font-size: 18px;
        }}
        .footer {{
            text-align: center;
            color: #64748b;
            font-size: 12px;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #e2e8f0;
        }}
        .button {{
            display: inline-block;
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            color: white;
            padding: 12px 30px;
            text-decoration: none;
            border-radius: 5px;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎬 FlixStream</h1>
        <p>Votre abonnement est activé !</p>
    </div>
    
    <div class="content">
        <h2>Bonjour {full_name},</h2>
        
        <p>Merci d'avoir choisi <strong>FlixStream</strong> !</p>
        
        <p>Votre abonnement <strong>{plan_name}</strong> a été activé avec succès.</p>
        
        <div class="credentials">
            <h3 style="margin-top: 0; color: #1e40af;">🔑 Vos informations de connexion</h3>
            
            <div class="credentials-item">
                <div class="credentials-label">URL du serveur :</div>
                <div class="credentials-value">{iptv_credentials['url']}</div>
            </div>
            
            <div class="credentials-item">
                <div class="credentials-label">Nom d'utilisateur :</div>
                <div class="credentials-value">{iptv_credentials['username']}</div>
            </div>
            
            <div class="credentials-item">
                <div class="credentials-label">Mot de passe :</div>
                <div class="credentials-value">{iptv_credentials['password']}</div>
            </div>
        </div>
        
        <div class="steps">
            <h3 style="margin-top: 0; color: #1e40af;">📱 Comment utiliser vos codes</h3>
            
            <div class="step">
                Téléchargez une application IPTV sur votre appareil :<br>
                <strong>IPTV Smarters Pro</strong> (Recommandée), TiviMate, ou Perfect Player
            </div>
            
            <div class="step">
                Ouvrez l'application et sélectionnez<br>
                <strong>"Login with Xtream Codes API"</strong>
            </div>
            
            <div class="step">
                Entrez les informations de connexion ci-dessus
            </div>
            
            <div class="step">
                Profitez de votre contenu en qualité HD/4K !
            </div>
        </div>
        
        <p style="background: #dbeafe; padding: 15px; border-radius: 5px; border-left: 4px solid #3b82f6;">
            <strong>💡 Besoin d'aide ?</strong><br>
            Si vous rencontrez des difficultés, n'hésitez pas à nous contacter via WhatsApp ou Telegram.
        </p>
    </div>
    
    <div class="footer">
        <p>© 2025 FlixStream - Service IPTV Premium</p>
        <p>Service de streaming professionnel • Support technique disponible</p>
    </div>
</body>
</html>
"""
        
        # Attacher les deux versions
        part1 = MIMEText(text_content, "plain")
        part2 = MIMEText(html_content, "html")
        message.attach(part1)
        message.attach(part2)
        
        # Envoyer l'email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        
        print(f"Email envoyé avec succès à {recipient_email}")
        return True
        
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {str(e)}")
        return False


def send_renewal_reminder_email(recipient_email, full_name, plan_name, expires_at):
    """
    Envoie un email de rappel pour le renouvellement d'abonnement
    
    Args:
        recipient_email: Email du destinataire
        full_name: Nom complet du client
        plan_name: Nom du plan d'abonnement
        expires_at: Date d'expiration
    """
    
    smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('SMTP_PORT', '587'))
    smtp_username = os.environ.get('SMTP_USERNAME', '')
    smtp_password = os.environ.get('SMTP_PASSWORD', '')
    sender_email = os.environ.get('SENDER_EMAIL', smtp_username)
    
    if not smtp_username or not smtp_password:
        print(f"[SIMULATION] Email de relance envoyé à {recipient_email}")
        return True
    
    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = "⏰ Votre abonnement FlixStream expire bientôt"
        message["From"] = sender_email
        message["To"] = recipient_email
        
        text_content = f"""
Bonjour {full_name},

Votre abonnement FlixStream {plan_name} expire le {expires_at.strftime('%d/%m/%Y')}.

Pour continuer à profiter de nos services sans interruption, pensez à renouveler votre abonnement dès maintenant.

Contactez-nous pour renouveler !

Cordialement,
L'équipe FlixStream
"""
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background: linear-gradient(135deg, #dc2626 0%, #ea580c 100%);
            color: white;
            padding: 30px;
            text-align: center;
            border-radius: 10px 10px 0 0;
        }}
        .content {{
            background: #f8fafc;
            padding: 30px;
            border-radius: 0 0 10px 10px;
        }}
        .alert {{
            background: #fef2f2;
            border-left: 4px solid #dc2626;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>⏰ FlixStream</h1>
        <p>Votre abonnement expire bientôt</p>
    </div>
    
    <div class="content">
        <h2>Bonjour {full_name},</h2>
        
        <div class="alert">
            <p><strong>Votre abonnement {plan_name} expire le {expires_at.strftime('%d/%m/%Y')}.</strong></p>
        </div>
        
        <p>Pour continuer à profiter de nos services sans interruption, pensez à renouveler votre abonnement dès maintenant.</p>
        
        <p><strong>Contactez-nous pour renouveler !</strong></p>
        
        <p>Cordialement,<br>L'équipe FlixStream</p>
    </div>
</body>
</html>
"""
        
        part1 = MIMEText(text_content, "plain")
        part2 = MIMEText(html_content, "html")
        message.attach(part1)
        message.attach(part2)
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        
        print(f"Email de relance envoyé avec succès à {recipient_email}")
        return True
        
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email de relance : {str(e)}")
        return False

