import http.server
import socketserver
import os
import threading

# Настройки портов
WEB_PORT = 8888  # Для загрузки самого сайта (index.html)
API_PORT = 9999  # Для передачи сообщений (API)
DB_FILE = "messages.txt"

class WebHandler(http.server.BaseHTTPRequestHandler):
    """Сервер только для раздачи HTML"""
    def log_message(self, format, *args): return
    def do_GET(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, 'index.html')
        try:
            with open(file_path, 'rb') as f:
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(f.read())
        except: self.send_error(404)

class ApiHandler(http.server.BaseHTTPRequestHandler):
    """Сервер только для сообщений"""
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

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        data = self.rfile.read(length).decode('utf-8')
        if data:
            with open(DB_FILE, "a", encoding="utf-8") as f:
                f.write(data + "\n")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_web():
    with socketserver.TCPServer(("0.0.0.0", WEB_PORT), WebHandler) as httpd:
        print(f"[WEB] Слушает на порту {WEB_PORT}")
        httpd.serve_forever()

def run_api():
    with socketserver.TCPServer(("0.0.0.0", API_PORT), ApiHandler) as httpd:
        print(f"[API] Слушает на порту {API_PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    # Запускаем два сервера в разных потоках
    threading.Thread(target=run_web, daemon=True).start()
    run_api()
