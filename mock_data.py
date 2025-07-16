from datetime import datetime, timedelta
import random
import json

def get_mock_cameras():
    """Generate mock camera data for the surveillance system"""
    cameras = [
        {
            'id': 1,
            'name': 'Main Entrance',
            'location': 'Building A - Front Door',
            'ip_address': '192.168.1.101',
            'status': 'online',
            'stream_url': 'rtsp://192.168.1.101:554/stream',
            'last_activity': datetime.utcnow() - timedelta(seconds=random.randint(1, 300))
        },
        {
            'id': 2,
            'name': 'Parking Lot North',
            'location': 'Parking Area - North Side',
            'ip_address': '192.168.1.102',
            'status': 'online',
            'stream_url': 'rtsp://192.168.1.102:554/stream',
            'last_activity': datetime.utcnow() - timedelta(seconds=random.randint(1, 300))
        },
        {
            'id': 3,
            'name': 'Warehouse Floor',
            'location': 'Building B - Main Floor',
            'ip_address': '192.168.1.103',
            'status': 'maintenance',
            'stream_url': 'rtsp://192.168.1.103:554/stream',
            'last_activity': datetime.utcnow() - timedelta(hours=2)
        },
        {
            'id': 4,
            'name': 'Emergency Exit',
            'location': 'Building A - Rear Exit',
            'ip_address': '192.168.1.104',
            'status': 'online',
            'stream_url': 'rtsp://192.168.1.104:554/stream',
            'last_activity': datetime.utcnow() - timedelta(seconds=random.randint(1, 300))
        },
        {
            'id': 5,
            'name': 'Loading Dock',
            'location': 'Building C - Loading Area',
            'ip_address': '192.168.1.105',
            'status': 'offline',
            'stream_url': 'rtsp://192.168.1.105:554/stream',
            'last_activity': datetime.utcnow() - timedelta(hours=1)
        },
        {
            'id': 6,
            'name': 'Reception Area',
            'location': 'Building A - Lobby',
            'ip_address': '192.168.1.106',
            'status': 'online',
            'stream_url': 'rtsp://192.168.1.106:554/stream',
            'last_activity': datetime.utcnow() - timedelta(seconds=random.randint(1, 300))
        }
    ]
    return cameras

def get_mock_alerts():
    """Generate mock alert data with AI enhancement"""
    alert_types = ['motion', 'object', 'boundary', 'loitering']
    severities = ['low', 'medium', 'high', 'critical']
    statuses = ['active', 'acknowledged', 'resolved']
    
    ai_enhanced_descriptions = {
        'motion': [
            'Unauthorized person detected in restricted area - potential security breach',
            'Multiple individuals moving in formation - coordinated activity detected',
            'Rapid movement pattern suggests fleeing behavior - investigate immediately'
        ],
        'object': [
            'Unattended package detected - potential security risk, recommend EOD assessment',
            'Tool/weapon-like object identified - enhanced threat level, notify security',
            'Vehicle blocking emergency exit - immediate removal required'
        ],
        'boundary': [
            'Perimeter breach detected with cutting tool signature - physical security compromise',
            'Fence climbing activity with extended duration - persistent intrusion attempt',
            'Multiple boundary violations in coordinated pattern - organized breach attempt'
        ],
        'loitering': [
            'Extended presence in sensitive area - surveillance/reconnaissance behavior',
            'Repetitive movement pattern suggests casing activity - potential pre-attack behavior',
            'Group gathering in non-public area - unauthorized assembly detected'
        ]
    }
    
    alerts = []
    for i in range(20):
        alert_type = random.choice(alert_types)
        is_ai_enhanced = random.choice([True, False, False])  # 33% chance of AI enhancement
        
        alert = {
            'id': i + 1,
            'camera_id': random.randint(1, 6),
            'camera_name': f'Camera {random.randint(1, 6)}',
            'alert_type': alert_type,
            'severity': random.choice(severities),
            'status': random.choice(statuses),
            'created_at': datetime.utcnow() - timedelta(hours=random.randint(0, 72)),
            'acknowledged_by': 'admin' if random.choice([True, False]) else None,
            'ai_enhanced': is_ai_enhanced,
            'confidence': round(random.uniform(0.6, 0.99), 2) if is_ai_enhanced else None
        }
        
        if is_ai_enhanced:
            alert['description'] = random.choice(ai_enhanced_descriptions[alert_type])
            alert['threat_analysis'] = {
                'risk_level': random.choice(['medium', 'high', 'critical']),
                'objects_detected': random.choice([
                    ['person', 'backpack'], 
                    ['vehicle', 'license_plate'], 
                    ['tool', 'cutting_implement'],
                    ['multiple_persons', 'coordination_pattern']
                ]),
                'recommended_action': random.choice([
                    'Immediate security response required',
                    'Deploy additional surveillance units',
                    'Notify law enforcement',
                    'Initiate lockdown protocol'
                ])
            }
        else:
            alert['description'] = f'Alert {i + 1} - {alert_type} detected'
        
        alerts.append(alert)
    
    # Sort by created_at descending
    alerts.sort(key=lambda x: x['created_at'], reverse=True)
    return alerts

def get_mock_events():
    """Generate mock event data for forensic search"""
    event_types = ['person', 'vehicle', 'object', 'motion']
    
    events = []
    for i in range(50):
        event = {
            'id': i + 1,
            'camera_id': random.randint(1, 6),
            'camera_name': f'Camera {random.randint(1, 6)}',
            'event_type': random.choice(event_types),
            'confidence': round(random.uniform(0.6, 0.99), 2),
            'timestamp': datetime.utcnow() - timedelta(hours=random.randint(0, 168)),
            'bounding_box': f'[{random.randint(10, 300)}, {random.randint(10, 200)}, {random.randint(400, 600)}, {random.randint(300, 400)}]',
            'event_metadata': f'Event {i + 1} metadata'
        }
        events.append(event)
    
    # Sort by timestamp descending
    events.sort(key=lambda x: x['timestamp'], reverse=True)
    return events

def get_analytics_data():
    """Generate mock analytics data"""
    now = datetime.utcnow()
    
    # Generate hourly data for the last 24 hours
    hourly_data = []
    for i in range(24):
        hour = now - timedelta(hours=i)
        hourly_data.append({
            'timestamp': hour.strftime('%H:%M'),
            'person_count': random.randint(5, 50),
            'vehicle_count': random.randint(0, 20),
            'alerts': random.randint(0, 5)
        })
    
    hourly_data.reverse()
    
    # Object detection summary
    object_summary = {
        'person': random.randint(150, 300),
        'vehicle': random.randint(50, 150),
        'bicycle': random.randint(10, 50),
        'other': random.randint(20, 80)
    }
    
    # Camera performance metrics
    camera_metrics = []
    for i in range(1, 7):
        camera_metrics.append({
            'camera_id': i,
            'name': f'Camera {i}',
            'uptime': round(random.uniform(85, 99.5), 1),
            'events_today': random.randint(20, 200),
            'alerts_today': random.randint(0, 10)
        })
    
    return {
        'hourly_data': hourly_data,
        'object_summary': object_summary,
        'camera_metrics': camera_metrics,
        'total_events_today': sum(c['events_today'] for c in camera_metrics),
        'total_alerts_today': sum(c['alerts_today'] for c in camera_metrics)
    }
