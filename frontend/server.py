#!/usr/bin/env python3
"""
Simple HTTP server to serve the frontend
Run this file to start the frontend server
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

# Configuration
PORT = 3000
FRONTEND_DIR = Path(__file__).parent

class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP Request Handler with CORS enabled"""
    
    def end_headers(self):
        """Add CORS headers"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_OPTIONS(self):
        """Handle preflight requests"""
        self.send_response(200)
        self.end_headers()

def start_server():
    """Start the frontend server"""
    # Change to frontend directory
    os.chdir(FRONTEND_DIR)
    
    # Create server
    with socketserver.TCPServer(("", PORT), CORSHTTPRequestHandler) as httpd:
        print(f"🚀 Frontend server starting...")
        print(f"📱 Server running at: http://localhost:{PORT}")
        print(f"📁 Serving files from: {FRONTEND_DIR}")
        print(f"🔗 API expected at: http://localhost:8000")
        print()
        print("💡 Instructions:")
        print("1. Make sure your API server is running on port 8000")
        print("2. Open http://localhost:3000 in your browser")
        print("3. Use Ctrl+C to stop the server")
        print()
        
        # Try to open browser automatically
        try:
            webbrowser.open(f'http://localhost:{PORT}')
            print("🌐 Opening browser...")
        except Exception:
            print("⚠️ Could not open browser automatically")
        
        print(f"✅ Server ready! Press Ctrl+C to stop.")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")

if __name__ == "__main__":
    start_server()
