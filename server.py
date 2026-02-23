import http.server
import socketserver
import os
import sys

# Настройка кодировки для Windows CMD, чтобы не было ошибок вывода
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

PORT = 1080
CHAT_HISTORY = "--- [胡耶塔] СИСТЕМА ОНЛАЙН ---\n"

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
        global CHAT_HISTORY
        # Определяем путь к файлу index.html в той же папке
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, 'index.html')

        if self.path == '/api':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            data = CHAT_HISTORY.encode('utf-8')
            self.send_header('Content-Length', len(data))
            self.end_headers()
            self.wfile.write(data)
        else:
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    content = f.read()
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.send_header('Content-Length', len(content))
                    self.end_headers()
                    self.wfile.write(content)
            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                msg = f"ОШИБКА: Файл index.html не найден в папке: {base_dir}".encode('utf-8')
                self.wfile.write(msg)

    def do_POST(self):
        global CHAT_HISTORY
        try:
            length = int(self.headers.get('Content-Length', 0))
            data = self.rfile.read(length).decode('utf-8')
            if data:
                CHAT_HISTORY += data + "\n"
                print(f"[RECV]: {data}")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        except Exception as e:
            print(f"Ошибка POST: {e}")
            self.send_error(500)

socketserver.TCPServer.allow_reuse_address = True
try:
    with socketserver.TCPServer(("0.0.0.0", PORT), HuyetaHandler) as httpd:
        print(f"--- [CORE HUYETA ACTIVE ON PORT {PORT}] ---")
        print(f"Папка сервера: {os.path.dirname(os.path.abspath(__file__))}")
        httpd.serve_forever()
except Exception as e:
    print(f"Критическая ошибка запуска: {e}")