from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            "api": "Clipador Studio",
            "version": "1.0.0",
            "status": "online",
            "endpoints": [
                "/api/v1/cut",
                "/api/v1/subtitles", 
                "/api/v1/analyze",
                "/api/v1/convert",
                "/api/v1/auto-edit",
                "/api/v1/publish",
                "/api/v1/thumbnail",
                "/api/v1/transcribe",
                "/api/v1/analytics",
                "/api/v1/shorts"
            ]
        }
        
        self.wfile.write(json.dumps(response).encode())
