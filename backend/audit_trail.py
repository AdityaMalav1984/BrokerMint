# backend/audit_trail.py - FIXED
from datetime import datetime
import json
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_db_connection

class AuditTrail:
    def record_action(self, user_id, action_type, details=None):
        conn = get_db_connection()
        try:
            conn.execute('''
                INSERT INTO audit_trail (user_id, action_type, details)
                VALUES (?, ?, ?)
            ''', (user_id, action_type, json.dumps(details) if details else None))
            conn.commit()
        finally:
            conn.close()
    
    def get_audit_log(self, limit=100):
        conn = get_db_connection()
        try:
            results = conn.execute('''
                SELECT a.*, u.username 
                FROM audit_trail a 
                LEFT JOIN users u ON a.user_id = u.id 
                ORDER BY a.timestamp DESC 
                LIMIT ?
            ''', (limit,)).fetchall()
            return [dict(row) for row in results]
        finally:
            conn.close()

audit_trail = AuditTrail()