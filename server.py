import http.server
import socketserver
import os

# Порт берется из настроек Render или 8888 локально
PORT = int(os.environ.get("PORT", 8888))
DB_FILE = "messages.txt"

# Создаем файл базы, если его нет
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        f.write("--- [胡耶塔] PROTOCOL INITIALIZED ---\n")

class HuyetaHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args): return

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        if self.path == '/api':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            if os.path.exists(DB_FILE):
                with open(DB_FILE, "r", encoding="utf-8") as f:
                    data = f.read().encode('utf-8')
                self.send_header('Content-Length', len(data))
                self.end_headers()
                self.wfile.write(data)
        else:
            # Отдача фронтенда
            base_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(base_dir, 'index.html')
            try:
                with open(file_path, 'rb') as f:
                    content = f.read()
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(content)
            except FileNotFoundError:
                self.send_error(404, "index.html not found")

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        data = self.rfile.read(length).decode('utf-8')
        if data:
            with open(DB_FILE, "a", encoding="utf-8") as f:
                f.write(data + "\n")
            print(f"[STORED]: {data}")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

socketserver.TCPServer.allow_reuse_address = True
print(f"--- [SERVER ONLINE ON PORT {PORT}] ---")
with socketserver.TCPServer(("0.0.0.0", PORT), HuyetaHandler) as httpd:
    httpd.serve_forever()
