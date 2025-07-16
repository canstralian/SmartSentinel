from app import db
from flask_login import UserMixin
from datetime import datetime
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from sqlalchemy import UniqueConstraint

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=True)
    first_name = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String, nullable=True)
    profile_image_url = db.Column(db.String, nullable=True)
    
    # Legacy fields for backwards compatibility
    username = db.Column(db.String(64), unique=True, nullable=True)
    password_hash = db.Column(db.String(256), nullable=True)
    role = db.Column(db.String(32), default='operations')  # operations, it, executive
    
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    last_login = db.Column(db.DateTime)

class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.String, db.ForeignKey(User.id))
    browser_session_key = db.Column(db.String, nullable=False)
    user = db.relationship(User)

    __table_args__ = (UniqueConstraint(
        'user_id',
        'browser_session_key',
        'provider',
        name='uq_user_browser_session_key_provider',
    ),)

class Camera(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200))
    ip_address = db.Column(db.String(45))
    status = db.Column(db.String(20), default='online')  # online, offline, maintenance
    stream_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    camera_id = db.Column(db.Integer, db.ForeignKey('camera.id'), nullable=False)
    alert_type = db.Column(db.String(50), nullable=False)  # motion, object, boundary, loitering
    severity = db.Column(db.String(20), default='medium')  # low, medium, high, critical
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')  # active, acknowledged, resolved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    acknowledged_by = db.Column(db.String, db.ForeignKey('users.id'))
    
    camera = db.relationship('Camera', backref='alerts')
    acknowledger = db.relationship('User', backref='acknowledged_alerts')

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    camera_id = db.Column(db.Integer, db.ForeignKey('camera.id'), nullable=False)
    event_type = db.Column(db.String(50), nullable=False)  # person, vehicle, object, motion
    confidence = db.Column(db.Float, default=0.0)
    bounding_box = db.Column(db.Text)  # JSON string for coordinates
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    event_metadata = db.Column(db.Text)  # JSON string for additional data
    
    camera = db.relationship('Camera', backref='events')
