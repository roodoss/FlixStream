from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    contact_method = db.Column(db.String(20), nullable=False)  # whatsapp or telegram
    plan_id = db.Column(db.String(50), nullable=False)  # 3months, 6months, 12months
    plan_name = db.Column(db.String(50), nullable=False)
    plan_price = db.Column(db.String(20), nullable=False)
    plan_duration = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, active, expired
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)
    iptv_username = db.Column(db.String(100), nullable=True)
    iptv_password = db.Column(db.String(100), nullable=True)
    iptv_url = db.Column(db.String(200), nullable=True)
    
    def __repr__(self):
        return f'<Subscription {self.full_name} - {self.plan_name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'contact_method': self.contact_method,
            'plan_id': self.plan_id,
            'plan_name': self.plan_name,
            'plan_price': self.plan_price,
            'plan_duration': self.plan_duration,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'iptv_username': self.iptv_username,
            'iptv_password': self.iptv_password,
            'iptv_url': self.iptv_url
        }

