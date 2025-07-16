
from flask import request, jsonify, flash, redirect, url_for, render_template
from app import app
from ai_service import ai_service
from replit_auth import require_login
from flask_login import current_user
from mock_data import get_mock_events, get_mock_alerts
import json
import base64

@app.route('/api/ai/analyze_image', methods=['POST'])
@require_login
def analyze_image():
    """Analyze uploaded security image using AI"""
    if current_user.role not in ['it', 'executive']:
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    image_file = request.files['image']
    camera_name = request.form.get('camera_name', 'Unknown Camera')
    
    try:
        image_data = image_file.read()
        analysis = ai_service.analyze_security_image(image_data, camera_name)
        
        return jsonify({
            'success': True,
            'analysis': analysis,
            'ai_available': ai_service.is_available()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/enhance_alert/<int:alert_id>')
@require_login
def enhance_alert(alert_id):
    """Enhance alert description using AI"""
    if current_user.role not in ['it', 'executive']:
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    try:
        # Get mock alert data (in real app, fetch from database)
        alerts = get_mock_alerts()
        alert = next((a for a in alerts if a['id'] == alert_id), None)
        
        if not alert:
            return jsonify({'error': 'Alert not found'}), 404
        
        enhanced_alert = ai_service.enhance_alert_description(alert)
        
        return jsonify({
            'success': True,
            'enhanced_alert': enhanced_alert,
            'ai_available': ai_service.is_available()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/security_report')
@require_login
def generate_security_report():
    """Generate AI-powered security report"""
    if current_user.role not in ['it', 'executive']:
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    try:
        time_period = request.args.get('period', 'last_24_hours')
        events = get_mock_events()
        
        report = ai_service.generate_security_report(events, time_period)
        
        return jsonify({
            'success': True,
            'report': report,
            'generated_at': ai_service.ai_service.datetime.utcnow().isoformat(),
            'ai_available': ai_service.is_available()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/threat_predictions')
@require_login
def get_threat_predictions():
    """Get AI-powered threat predictions"""
    if current_user.role not in ['it', 'executive']:
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    try:
        historical_data = get_mock_events()
        predictions = ai_service.predict_threat_patterns(historical_data)
        
        return jsonify({
            'success': True,
            'predictions': predictions,
            'ai_available': ai_service.is_available()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ai_dashboard')
@require_login
def ai_dashboard():
    """AI-enhanced dashboard for advanced users"""
    if current_user.role not in ['it', 'executive']:
        flash('Access denied. AI features require IT or Executive role.', 'error')
        return redirect(url_for('dashboard'))
    
    ai_status = ai_service.is_available()
    alerts = get_mock_alerts()
    ai_alerts = [a for a in alerts if a.get('ai_enhanced')]
    
    return render_template('ai_dashboard.html', 
                         ai_status=ai_status,
                         ai_alerts=ai_alerts[:10],
                         total_enhanced=len(ai_alerts))

@app.route('/api/ai/status')
@require_login
def ai_status():
    """Check AI service availability"""
    return jsonify({
        'ai_services': ai_service.is_available(),
        'anthropic_configured': bool(ai_service.anthropic_key),
        'google_ai_configured': bool(ai_service.google_key)
    })
