from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("?")[0]
        
        routes = {
            "/": {
                "api": "Clipador Studio",
                "version": "1.0.0",
                "status": "online",
                "endpoints": [
                    "GET  /api/v1/cut",
                    "GET  /api/v1/subtitles",
                    "GET  /api/v1/analyze",
                    "GET  /api/v1/convert",
                    "GET  /api/v1/auto-edit",
                    "GET  /api/v1/publish",
                    "GET  /api/v1/thumbnail",
                    "GET  /api/v1/transcribe",
                    "GET  /api/v1/analytics",
                    "GET  /api/v1/shorts"
                ]
            },
            "/api/v1/cut": {
                "success": True,
                "message": "Corte de vídeo gerado com sucesso!",
                "clip_url": "https://storage.clipador.studio/clips/exemplo.mp4",
                "duration": 60
            },
            "/api/v1/subtitles": {
                "success": True,
                "message": "Legendas geradas com sucesso!",
                "style": "kinetic",
                "subtitles": [
                    {"start": 0, "end": 3, "text": "ESSE MOMENTO", "animation": "pop", "color": "#6C5CE7"},
                    {"start": 3, "end": 6, "text": "É INCRÍVEL", "animation": "zoom", "color": "#FF6B6B"},
                    {"start": 6, "end": 10, "text": "NÃO DÁ PRA ACREDITAR!", "animation": "bounce", "color": "#FFD700"}
                ]
            },
            "/api/v1/analyze": {
                "success": True,
                "message": "Análise concluída!",
                "virality_score": 88,
                "rating": "🔥 ALTAMENTE VIRAL",
                "criteria": {
                    "gancho_inicial": 95,
                    "curiosidade": 88,
                    "emocao": 82,
                    "humor": 75,
                    "retencao": 90,
                    "compartilhamento": 85
                },
                "suggested_hashtags": ["#viral", "#fyp", "#shorts"]
            },
            "/api/v1/convert": {
                "success": True,
                "message": "Vídeo convertido para 9:16!",
                "original_format": "16:9",
                "target_format": "9:16",
                "resolution": "1080x1920"
            },
            "/api/v1/auto-edit": {
                "success": True,
                "message": "5 cortes editados automaticamente!",
                "clips": [
                    {"id": 1, "title": "🔥 MELHOR MOMENTO #1", "duration": 60},
                    {"id": 2, "title": "😱 REVELAÇÃO #2", "duration": 60},
                    {"id": 3, "title": "💡 DICA #3", "duration": 60},
                    {"id": 4, "title": "🤫 SEGREDO #4", "duration": 60},
                    {"id": 5, "title": "🥹 EMOÇÃO #5", "duration": 60}
                ]
            },
            "/api/v1/publish": {
                "success": True,
                "message": "Vídeo publicado com sucesso!",
                "platforms": {
                    "youtube": "https://youtube.com/shorts/abc123",
                    "tiktok": "https://tiktok.com/@user/video/123"
                }
            },
            "/api/v1/thumbnail": {
                "success": True,
                "message": "Thumbnail gerada!",
                "thumbnail_url": "https://storage.clipador.studio/thumbnails/exemplo.png",
                "ctr_prediction": "8.5%"
            },
            "/api/v1/transcribe": {
                "success": True,
                "message": "Transcrição concluída!",
                "language": "pt",
                "segments": [
                    {"start": 0, "end": 5, "speaker": "Pessoa 1", "text": "Bem-vindos!"},
                    {"start": 5, "end": 10, "speaker": "Pessoa 2", "text": "Hoje temos um tema incrível."}
                ]
            },
            "/api/v1/analytics": {
                "success": True,
                "message": "Analytics carregados!",
                "metrics": {
                    "total_views": 125000,
                    "engagement": "8.5%",
                    "avg_watch_time": "35s",
                    "shares": 2500
                }
            },
            "/api/v1/shorts": {
                "success": True,
                "message": "5 shorts criados com IA!",
                "shorts": [
                    {"id": 1, "title": "🔥 VIRAL #1", "score": "95/100"},
                    {"id": 2, "title": "😱 VIRAL #2", "score": "92/100"},
                    {"id": 3, "title": "💡 VIRAL #3", "score": "89/100"},
                    {"id": 4, "title": "🤫 VIRAL #4", "score": "86/100"},
                    {"id": 5, "title": "🥹 VIRAL #5", "score": "83/100"}
                ]
            }
        }
        
        response = routes.get(path, {"error": "Rota não encontrada", "available_routes": list(routes.keys())})
        
        self.send_response(200 if path in routes else 404)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response, ensure_ascii=False, indent=2).encode('utf-8'))
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length else b'{}'
        
        try:
            data = json.loads(body)
        except:
            data = {}
        
        path = self.path.split("?")[0]
        
        response = {
            "success": True,
            "message": f"POST recebido em {path}",
            "data_received": data,
            "result": "Processado com sucesso!"
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response, ensure_ascii=False, indent=2).encode('utf-8'))
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()
