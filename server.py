import http.server
import socketserver
import os

PORT = int(os.environ.get("PORT", 8888)) # Render сам назначит порт
DB_FILE = "messages.txt"

if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        f.write("--- [胡耶塔] СИСТЕМА ОНЛАЙН ---\n")

class HuyetaHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args): return

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_GET(self):
        if self.path == '/api':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            with open(DB_FILE, "r", encoding="utf-8") as f:
                data = f.read().encode('utf-8')
            self.send_header('Content-Length', len(data))
            self.end_headers()
            self.wfile.write(data)
        else:
            file_path = os.path.join(os.path.dirname(__file__), 'index.html')
            try:
                with open(file_path, 'rb') as f:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(f.read())
            except:
                self.send_error(404)

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        data = self.rfile.read(length).decode('utf-8')
        if data:
            with open(DB_FILE, "a", encoding="utf-8") as f:
                f.write(data + "\n")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

with socketserver.TCPServer(("0.0.0.0", PORT), HuyetaHandler) as httpd:
    print(f"ONLINE ON PORT {PORT}")
    httpd.serve_forever()
