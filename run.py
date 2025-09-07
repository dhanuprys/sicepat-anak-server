#!/usr/bin/env python3
"""
Run script untuk Stunting Checking App
"""

import uvicorn
import socket
import os
from app.config import settings

def get_local_ip():
    """Get local IP address for external access"""
    try:
        # Get local IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

if __name__ == "__main__":
    local_ip = get_local_ip()
    
    print("🌐 Network Configuration:")
    print(f"   Host: {settings.host}")
    print(f"   Port: {settings.port}")
    print(f"   Local IP: {local_ip}")
    print(f"   External Access: http://{local_ip}:{settings.port}")
    print(f"   Local Access: http://127.0.0.1:{settings.port}")
    print(f"   API Docs: http://{local_ip}:{settings.port}/docs")
    print("=" * 50)
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info",
        access_log=True
    )
