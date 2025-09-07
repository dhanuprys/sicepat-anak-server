#!/usr/bin/env python3
"""
Script untuk setup database dan menjalankan migration
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} berhasil")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} gagal")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setup Database Stunting Checking App")
    print("=" * 50)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ File .env tidak ditemukan!")
        print("📝 Silakan copy env.example ke .env dan edit konfigurasi database")
        return False
    
    # Check if alembic is installed
    try:
        import alembic
    except ImportError:
        print("❌ Alembic tidak terinstall!")
        print("💡 Jalankan: pip install -r requirements.txt")
        return False
    
    # Initialize alembic if not already done
    if not os.path.exists('alembic/versions'):
        print("🔄 Inisialisasi Alembic...")
        if not run_command("alembic init alembic", "Inisialisasi Alembic"):
            return False
    
    # Create initial migration
    print("🔄 Membuat migration awal...")
    if not run_command("alembic revision --autogenerate -m 'Initial migration'", "Membuat migration"):
        return False
    
    # Run migration
    print("🔄 Menjalankan migration...")
    if not run_command("alembic upgrade head", "Menjalankan migration"):
        return False
    
    print("\n🎉 Setup database berhasil!")
    print("📊 Database tables telah dibuat")
    print("🚀 Aplikasi siap dijalankan dengan: python run.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
