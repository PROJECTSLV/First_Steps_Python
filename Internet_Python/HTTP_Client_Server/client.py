import requests

BASE_URL = "http://localhost:8000"

print("=== 1. GET /api/status ===")
response = requests.get(f"{BASE_URL}/api/status")
print(f"Код статуса: {response.status_code}")
print(f"Тело ответа: {response.text}")

data = response.json()
print(f"Сообщение от сервера: {data['message']}")
print()

print("=== 2. POST /api/login ===")
login_data = {
    "username": "admin",
    "password": "1234"
}

headers = {'Content-Type': 'application/json'}
response = requests.post(
    f"{BASE_URL}/api/login",
    json=login_data,
    headers=headers
)

print(f"Код статуса: {response.status_code}")
print(f"Тело ответа: {response.text}")
