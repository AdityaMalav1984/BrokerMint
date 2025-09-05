#!/usr/bin/env python3
"""
Complete BrokerMint Debug Script
"""
import os
import sys
import subprocess
import requests
import sqlite3
from pathlib import Path

def check_backend():
    print("🔍 Checking Backend...")
    print("=" * 50)
    
    # Check if backend folder exists
    backend_path = Path("backend")
    if not backend_path.exists():
        print("❌ Backend folder missing!")
        return False
    
    # Check requirements
    req_path = backend_path / "requirements.txt"
    if not req_path.exists():
        print("❌ requirements.txt missing!")
        return False
    
    # Check main app file
    app_path = backend_path / "app.py"
    if not app_path.exists():
        print("❌ app.py missing!")
        return False
    
    print("✅ Backend structure: OK")
    return True

def check_frontend():
    print("\n🔍 Checking Frontend...")
    print("=" * 50)
    
    frontend_path = Path("frontend")
    if not frontend_path.exists():
        print("❌ Frontend folder missing!")
        return False
    
    # Check essential files
    essential_files = [
        "package.json",
        "public/index.html",
        "src/App.js",
        "src/index.js"
    ]
    
    for file in essential_files:
        if not (frontend_path / file).exists():
            print(f"❌ {file} missing!")
            return False
    
    print("✅ Frontend structure: OK")
    return True

def check_database():
    print("\n🔍 Checking Database...")
    print("=" * 50)
    
    shared_data = Path("shared_data")
    if not shared_data.exists():
        print("❌ shared_data folder missing!")
        return False
    
    db_path = shared_data / "brokermint.db"
    if not db_path.exists():
        print("❌ Database file missing!")
        return False
    
    # Check database content
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        expected_tables = ['users', 'audit_trail', 'anomalies', 'ekyc_verifications']
        
        print(f"📊 Tables found: {tables}")
        
        for table in expected_tables:
            if table not in tables:
                print(f"❌ Missing table: {table}")
        
        # Check admin user
        cursor.execute("SELECT * FROM users WHERE username = 'admin'")
        admin = cursor.fetchone()
        if admin:
            print("✅ Admin user: EXISTS")
        else:
            print("❌ Admin user: MISSING")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_backend_server():
    print("\n🔍 Testing Backend Server...")
    print("=" * 50)
    
    try:
        # Try to start backend temporarily
        process = subprocess.Popen(
            [sys.executable, "backend/app.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Give it a moment to start
        import time
        time.sleep(3)
        
        # Test health endpoint
        try:
            response = requests.get("http://localhost:5000/api/health", timeout=5)
            print(f"✅ Backend server: RUNNING (Status: {response.status_code})")
            process.terminate()
            return True
        except:
            print("❌ Backend server: NOT RESPONDING")
            process.terminate()
            return False
            
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return False

def main():
    print("🚀 BrokerMint Complete Debug")
    print("=" * 60)
    
    # Check basic structure
    backend_ok = check_backend()
    frontend_ok = check_frontend()
    database_ok = check_database()
    
    print("\n📊 Summary:")
    print(f"Backend: {'✅ OK' if backend_ok else '❌ ISSUES'}")
    print(f"Frontend: {'✅ OK' if frontend_ok else '❌ ISSUES'}")
    print(f"Database: {'✅ OK' if database_ok else '❌ ISSUES'}")
    
    if backend_ok:
        test_backend_server()
    
    print("\n" + "=" * 60)
    print("Next steps:")
    print("1. Share the output of this debug script")
    print("2. Share your HTML file content")
    print("3. Share browser console errors (F12 → Console)")
    print("4. Describe which functionalities are broken")

if __name__ == "__main__":
    main()