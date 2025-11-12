from http.server import HTTPServer, BaseHTTPRequestHandler
import json


class SimpleAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {
                "status": "OK",
                "message": "Сервер работает!",
                "students_online": 15
            }
            self.wfile.write(json.dumps(response_data).encode())
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == '/api/login':
            # 1. Получаем длину тела запроса из заголовков
            content_length = int(self.headers.get('Content-Length', 0))
            # 2. Читаем сами данные (тело запроса)
            post_data = self.rfile.read(content_length)
            # 3. Парсим JSON из полученных данных
            try:
                data = json.loads(post_data)
                username = data.get('username', '')
                password = data.get('password', '')

                # 4. Простейшая "проверка" (НЕ ДЕЛАЙТЕ ТАК В РЕАЛЬНОСТИ!)
                if username == "admin" and password == "1234":
                    response_data = {"success": True, "token": "fake_token_12345"}
                    self.send_response(200)
                else:
                    response_data = {"success": False, "error": "Wrong credentials"}
                    self.send_response(401)

            except:
                response_data = {"success": False, "error": "Invalid JSON"}
                self.send_response(400)

            # 5. Отправляем ответ
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())


print("Запускаем сервер на http://localhost:8000")

server = HTTPServer(('0.0.0.0', 8000), SimpleAPIHandler)
server = HTTPServer(('localhost', 8000), SimpleAPIHandler)
server.serve_forever()
