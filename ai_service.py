
import os
import json
import base64
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import requests
from anthropic import Anthropic
import google.generativeai as genai

class AIService:
    def __init__(self):
        self.anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        self.google_key = os.getenv('GOOGLE_AI_KEY')
        
        # Initialize clients if keys are available
        self.anthropic_client = None
        self.gemini_model = None
        
        if self.anthropic_key:
            try:
                self.anthropic_client = Anthropic(api_key=self.anthropic_key)
                logging.info("Anthropic client initialized successfully")
            except Exception as e:
                logging.error(f"Failed to initialize Anthropic client: {e}")
        
        if self.google_key:
            try:
                genai.configure(api_key=self.google_key)
                self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
                logging.info("Google AI client initialized successfully")
            except Exception as e:
                logging.error(f"Failed to initialize Google AI client: {e}")
    
    def analyze_security_image(self, image_data: bytes, camera_name: str) -> Dict:
        """Analyze security camera image for threats and objects"""
        if not self.gemini_model:
            return self._fallback_analysis()
        
        try:
            # Encode image for API
            image_b64 = base64.b64encode(image_data).decode()
            
            prompt = """Analyze this security camera image for:
1. People count and behavior (suspicious activity, loitering, unauthorized access)
2. Vehicles (license plates, unusual parking, blocked exits)
3. Objects (weapons, packages, tools, equipment)
4. Environmental hazards (smoke, fire, water damage)
5. Security concerns (broken windows, open doors, tampering)

Provide a JSON response with:
- threat_level: "low", "medium", "high", "critical"
- confidence: 0.0-1.0
- objects_detected: list of objects with confidence scores
- threat_description: brief description of any threats
- recommended_action: suggested response
"""
            
            response = self.gemini_model.generate_content([
                prompt,
                {"mime_type": "image/jpeg", "data": image_b64}
            ])
            
            # Parse JSON response
            analysis = json.loads(response.text)
            analysis['analyzed_by'] = 'gemini'
            analysis['timestamp'] = datetime.utcnow().isoformat()
            analysis['camera'] = camera_name
            
            return analysis
            
        except Exception as e:
            logging.error(f"Image analysis failed: {e}")
            return self._fallback_analysis()
    
    def enhance_alert_description(self, alert_data: Dict) -> Dict:
        """Use Claude to enhance alert descriptions with context"""
        if not self.anthropic_client:
            return alert_data
        
        try:
            prompt = f"""
Security Alert Enhancement:

Camera: {alert_data.get('camera_name', 'Unknown')}
Alert Type: {alert_data.get('alert_type', 'Unknown')}
Time: {alert_data.get('created_at', 'Unknown')}
Severity: {alert_data.get('severity', 'Unknown')}
Description: {alert_data.get('description', 'No description')}

Please provide:
1. Enhanced description with security context
2. Potential escalation scenarios
3. Recommended immediate actions
4. Risk assessment for this specific alert type

Format as JSON with keys: enhanced_description, escalation_risks, immediate_actions, risk_assessment
"""
            
            message = self.anthropic_client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            enhancement = json.loads(message.content[0].text)
            alert_data.update(enhancement)
            alert_data['ai_enhanced'] = True
            
            return alert_data
            
        except Exception as e:
            logging.error(f"Alert enhancement failed: {e}")
            return alert_data
    
    def generate_security_report(self, events: List[Dict], time_period: str) -> str:
        """Generate comprehensive security report using Claude"""
        if not self.anthropic_client:
            return "AI reporting not available - API key not configured"
        
        try:
            events_summary = json.dumps(events[:20], default=str, indent=2)
            
            prompt = f"""
Generate a comprehensive security report for the {time_period} period.

Events Data:
{events_summary}

Please provide:
1. Executive Summary
2. Key Security Incidents
3. Threat Pattern Analysis
4. System Performance Metrics
5. Recommendations for Security Improvements
6. Risk Mitigation Strategies

Format as a professional security report suitable for executive review.
"""
            
            message = self.anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=2000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            return message.content[0].text
            
        except Exception as e:
            logging.error(f"Report generation failed: {e}")
            return f"Report generation failed: {str(e)}"
    
    def predict_threat_patterns(self, historical_data: List[Dict]) -> Dict:
        """Analyze patterns to predict potential security threats"""
        if not self.anthropic_client:
            return {"prediction": "AI prediction not available"}
        
        try:
            data_summary = json.dumps(historical_data, default=str, indent=2)
            
            prompt = f"""
Analyze this historical security data to identify patterns and predict potential threats:

{data_summary}

Provide predictions for:
1. High-risk time periods
2. Vulnerable locations/cameras
3. Recurring threat types
4. Seasonal patterns
5. Recommended preventive measures

Format as JSON with actionable insights.
"""
            
            message = self.anthropic_client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1500,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            predictions = json.loads(message.content[0].text)
            predictions['generated_at'] = datetime.utcnow().isoformat()
            
            return predictions
            
        except Exception as e:
            logging.error(f"Threat prediction failed: {e}")
            return {"prediction": f"Analysis failed: {str(e)}"}
    
    def _fallback_analysis(self) -> Dict:
        """Fallback analysis when AI services are unavailable"""
        return {
            "threat_level": "medium",
            "confidence": 0.5,
            "objects_detected": [],
            "threat_description": "Standard motion detection - AI analysis unavailable",
            "recommended_action": "Manual review recommended",
            "analyzed_by": "fallback",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def is_available(self) -> Dict[str, bool]:
        """Check which AI services are available"""
        return {
            "anthropic": self.anthropic_client is not None,
            "google_ai": self.gemini_model is not None
        }

# Global AI service instance
ai_service = AIService()
