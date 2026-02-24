import http.server
import socketserver
import os

PORT = int(os.environ.get("PORT", 8888))
DB_FILE = "messages.txt"

class ControlHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args): return

    def _set_headers(self, content_type='text/plain'):
        self.send_response(200)
        self.send_header('Content-type', f'{content_type}; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self): self._set_headers()

    def do_GET(self):
        # 1. API для сообщений
        if self.path == '/api':
            self._set_headers()
            if not os.path.exists(DB_FILE): open(DB_FILE, 'w').close()
            with open(DB_FILE, "r", encoding="utf-8") as f:
                self.wfile.write(f.read().encode('utf-8'))
        
        # 2. Страница дебага (Панель перехвата)
        elif self.path == '/debug':
            try:
                with open('debug.html', 'rb') as f:
                    self._set_headers('text/html')
                    self.wfile.write(f.read())
            except: self.send_error(404, "debug.html not found")
            
        # 3. Главная страница чата (любой другой путь)
        else:
            try:
                with open('index.html', 'rb') as f:
                    self._set_headers('text/html')
                    self.wfile.write(f.read())
            except: self.send_error(404, "index.html not found")

    def do_POST(self):
        if self.path == '/api':
            length = int(self.headers.get('Content-Length', 0))
            data = self.rfile.read(length).decode('utf-8')
            with open(DB_FILE, "a", encoding="utf-8") as f:
                f.write(data + "\n")
            self._set_headers()
            self.wfile.write(b"OK")

    def do_DELETE(self):
        if self.path == '/api':
            open(DB_FILE, 'w').close()
            self._set_headers()
            self.wfile.write(b"CLEARED")

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("0.0.0.0", PORT), ControlHandler) as httpd:
    httpd.serve_forever()
