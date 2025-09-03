# backend/app.py - COMPLETE FIXED VERSION
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from datetime import datetime, timedelta
import json
import logging
import io
import sqlite3
from functools import wraps

# Import local modules
from config import config
from database import get_db_connection, init_database
from auth import auth_system
from anomaly_detection import anomaly_detector
from audit_trail import audit_trail
from ekyc import ekyc_verifier

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Authentication decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({'error': 'Token is missing'}), 401
        
        token = token[7:]
        user_data = auth_system.verify_token(token)
        if not user_data:
            return jsonify({'error': 'Token is invalid'}), 401
        
        request.user = user_data
        return f(*args, **kwargs)
    return decorated

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'BrokerMint API'
    })

@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        user_id = auth_system.create_user(
            data['username'],
            data['email'],
            data['password'],
            data.get('full_name', ''),
            data.get('role', 'user')
        )
        
        if user_id:
            user = get_db_connection().execute(
                'SELECT id, username, email, full_name, role FROM users WHERE id = ?',
                (user_id,)
            ).fetchone()
            
            token = auth_system.generate_token(dict(user))
            audit_trail.record_action(user_id, 'user_registration')
            
            return jsonify({
                'message': 'User created successfully',
                'token': token,
                'user': dict(user)
            })
        else:
            return jsonify({'error': 'User already exists'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = auth_system.authenticate_user(data['username'], data['password'])
        
        if user:
            token = auth_system.generate_token(user)
            audit_trail.record_action(user['id'], 'user_login')
            
            return jsonify({
                'message': 'Login successful',
                'token': token,
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email'],
                    'full_name': user['full_name'],
                    'role': user['role']
                }
            })
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dashboard', methods=['GET'])
@token_required
def get_dashboard():
    try:
        # Generate sample anomalies
        sample_data = anomaly_detector.generate_sample_data()
        anomalies_data = anomaly_detector.detect_anomalies(sample_data)
        
        # Get recent anomalies
        recent_anomalies = anomalies_data[anomalies_data['is_anomaly']].nlargest(5, 'anomaly_score')
        
        # Prepare response
        anomalies = []
        for _, row in recent_anomalies.iterrows():
            anomalies.append({
                'ticker': row['ticker'],
                'anomaly_score': round(row['anomaly_score'], 4),
                'risk_level': anomaly_detector.get_risk_level(row['anomaly_score']),
                'timestamp': datetime.now().isoformat()
            })
        
        audit_trail.record_action(request.user['user_id'], 'dashboard_view')
        
        return jsonify({
            'alerts': [
                {
                    'id': 1,
                    'title': 'Quarterly Compliance Report Due',
                    'description': 'SEBI quarterly report submission in 7 days',
                    'severity': 'high',
                    'deadline': (datetime.now() + timedelta(days=7)).isoformat()
                }
            ],
            'anomalies': anomalies,
            'stats': {
                'total_checks': len(sample_data),
                'anomalies_found': len(anomalies),
                'high_risk_count': sum(1 for a in anomalies if a['risk_level'] in ['High', 'Critical'])
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/anomalies/detect', methods=['POST'])
@token_required
def detect_anomalies():
    try:
        data = request.get_json()
        tickers = data.get('tickers', ['AAPL', 'GOOGL', 'MSFT'])
        
        # Generate sample data for requested tickers
        sample_data = anomaly_detector.generate_sample_data()
        sample_data = sample_data[sample_data['ticker'].isin(tickers)]
        
        anomalies_data = anomaly_detector.detect_anomalies(sample_data)
        anomalies = anomalies_data[anomalies_data['is_anomaly']]
        
        results = []
        for _, row in anomalies.iterrows():
            results.append({
                'ticker': row['ticker'],
                'anomaly_score': round(row['anomaly_score'], 4),
                'risk_level': anomaly_detector.get_risk_level(row['anomaly_score']),
                'price': row['price'],
                'volume': row['volume'],
                'timestamp': datetime.now().isoformat()
            })
        
        audit_trail.record_action(request.user['user_id'], 'anomaly_detection', {
            'tickers': tickers,
            'anomalies_found': len(results)
        })
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ekyc/verify', methods=['POST'])
@token_required
def verify_identity():
    try:
        data = request.get_json()
        result = ekyc_verifier.verify_document(
            request.user['user_id'],
            data['document_type'],
            data.get('document_data', {})
        )
        
        audit_trail.record_action(request.user['user_id'], 'ekyc_verification', {
            'document_type': data['document_type'],
            'status': result.get('status'),
            'success': result.get('success', False)
        })
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/audit/trail', methods=['GET'])
@token_required
def get_audit_trail():
    try:
        limit = request.args.get('limit', 50, type=int)
        logs = audit_trail.get_audit_log(limit)
        return jsonify({'entries': logs, 'total': len(logs)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports/compliance', methods=['GET'])
@token_required
def generate_report():
    try:
        # Generate a simple text report
        report_content = f"""
        BROKERMINT COMPLIANCE REPORT
        Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        Generated by: {request.user['username']}
        
        SUMMARY:
        - Total compliance checks: 150
        - Anomalies detected: 12
        - High-risk transactions: 3
        - Pending actions: 2
        
        RECOMMENDATIONS:
        1. Review high-risk transactions
        2. Complete pending compliance actions
        3. Schedule next audit cycle
        """
        
        audit_trail.record_action(request.user['user_id'], 'report_generated')
        
        return jsonify({
            'report': report_content,
            'filename': f'compliance_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# In backend/app.py, change the last few lines:
if __name__ == '__main__':
    init_database()
    print("Starting BrokerMint Compliance Server...")
    print(f"API URL: http://{config.API_HOST}:{config.API_PORT}")
    print("Default admin credentials: admin/admin")
    app.run(
        host=config.API_HOST,
        port=config.API_PORT,
        debug=config.DEBUG
    )