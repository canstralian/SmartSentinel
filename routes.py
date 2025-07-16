from flask import render_template, request, redirect, url_for, flash, session, jsonify
from app import app, db
from models import User, Camera, Alert, Event
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
import json
from mock_data import get_mock_cameras, get_mock_alerts, get_mock_events, get_analytics_data

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            
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
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
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
def cameras():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    cameras = get_mock_cameras()
    return render_template('cameras.html', cameras=cameras)

@app.route('/analytics')
def analytics():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if session.get('role') not in ['it', 'executive']:
        flash('Access denied. Insufficient permissions.', 'error')
        return redirect(url_for('dashboard'))
    
    analytics_data = get_analytics_data()
    events = get_mock_events()
    
    return render_template('analytics.html', 
                         analytics=analytics_data,
                         events=events)

@app.route('/alerts')
def alerts():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    all_alerts = get_mock_alerts()
    return render_template('alerts.html', alerts=all_alerts)

@app.route('/forensic')
def forensic():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if session.get('role') not in ['it', 'executive']:
        flash('Access denied. Insufficient permissions.', 'error')
        return redirect(url_for('dashboard'))
    
    cameras = get_mock_cameras()
    events = get_mock_events()
    
    return render_template('forensic.html', 
                         cameras=cameras,
                         events=events)

@app.route('/acknowledge_alert/<int:alert_id>')
def acknowledge_alert(alert_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    flash(f'Alert {alert_id} acknowledged', 'success')
    return redirect(url_for('alerts'))

@app.context_processor
def inject_user():
    return dict(
        current_user=session.get('username'),
        user_role=session.get('role')
    )
