from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import socket


class SimpleAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {
                "status": "OK",
                "message": "Сервер работает в сети!",
                "client_ip": self.client_address[0],
                "students_online": 15
            }
            self.wfile.write(json.dumps(response_data).encode())
        else:
            self.send_error(404)

    def do_POST(self):

        pass


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


local_ip = get_local_ip()
print("=" * 50)
print("🎯 СЕРВЕР ЗАПУЩЕН В ЛОКАЛЬНОЙ СЕТИ!")
print(f"📡 Ваш IP адрес: {local_ip}")
print(f"🌐 Другие могут подключиться по: http://{local_ip}:8000")
print("=" * 50)

server = HTTPServer(('0.0.0.0', 8000), SimpleAPIHandler)
server.serve_forever()
