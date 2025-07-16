from flask import render_template, request, redirect, url_for, flash, session, jsonify
from app import app, db
from models import User, Camera, Alert, Event
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
import json
from mock_data import get_mock_cameras, get_mock_alerts, get_mock_events, get_analytics_data
from replit_auth import require_login, make_replit_blueprint
from flask_login import current_user, login_required, login_user

# Register the Replit Auth blueprint
app.register_blueprint(make_replit_blueprint(), url_prefix="/auth")

# Make session permanent
@app.before_request
def make_session_permanent():
    session.permanent = True

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('replit_auth.login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.password_hash and check_password_hash(user.password_hash, password):
            # Use Flask-Login for consistency
            login_user(user)
            
            # Update last login
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    return redirect(url_for('replit_auth.logout'))

@app.route('/dashboard')
@require_login
def dashboard():
    # Get mock data
    cameras = get_mock_cameras()
    recent_alerts = get_mock_alerts()[:5]  # Last 5 alerts
    analytics = get_analytics_data()
    
    # Calculate statistics
    total_cameras = len(cameras)
    online_cameras = len([c for c in cameras if c['status'] == 'online'])
    active_alerts = len([a for a in recent_alerts if a['status'] == 'active'])
    
    stats = {
        'total_cameras': total_cameras,
        'online_cameras': online_cameras,
        'offline_cameras': total_cameras - online_cameras,
        'active_alerts': active_alerts,
        'system_health': round((online_cameras / total_cameras) * 100, 1) if total_cameras > 0 else 0
    }
    
    return render_template('dashboard.html', 
                         cameras=cameras[:6],  # Show first 6 cameras
                         alerts=recent_alerts,
                         stats=stats,
                         analytics=analytics)

@app.route('/cameras')
@require_login
def cameras():
    cameras = get_mock_cameras()
    return render_template('cameras.html', cameras=cameras)

@app.route('/analytics')
@require_login
def analytics():
    if current_user.role not in ['it', 'executive']:
        flash('Access denied. Insufficient permissions.', 'error')
        return redirect(url_for('dashboard'))
    
    analytics_data = get_analytics_data()
    events = get_mock_events()
    
    return render_template('analytics.html', 
                         analytics=analytics_data,
                         events=events)

@app.route('/alerts')
@require_login
def alerts():
    all_alerts = get_mock_alerts()
    return render_template('alerts.html', alerts=all_alerts)

@app.route('/forensic')
@require_login
def forensic():
    if current_user.role not in ['it', 'executive']:
        flash('Access denied. Insufficient permissions.', 'error')
        return redirect(url_for('dashboard'))
    
    cameras = get_mock_cameras()
    events = get_mock_events()
    
    return render_template('forensic.html', 
                         cameras=cameras,
                         events=events)

@app.route('/acknowledge_alert/<int:alert_id>')
@require_login
def acknowledge_alert(alert_id):
    flash(f'Alert {alert_id} acknowledged', 'success')
    return redirect(url_for('alerts'))

@app.context_processor
def inject_user():
    user_name = None
    user_role = None
    
    if current_user.is_authenticated:
        # Use first name if available, otherwise use username or email
        if current_user.first_name:
            user_name = current_user.first_name
        elif current_user.username:
            user_name = current_user.username
        elif current_user.email:
            user_name = current_user.email.split('@')[0]
        else:
            user_name = f"User {current_user.id}"
        
        user_role = current_user.role
    
    return dict(
        current_user=user_name,
        user_role=user_role
    )
