# client.py
import requests
import json

BASE_URL = "http://localhost:8000"


def test_api():
    print("=== 1. Тестируем GET /api/status ===")
    try:
        response = requests.get(f"{BASE_URL}/api/status")
        print(f"Код статуса: {response.status_code}")

        # Проверяем успешность запроса перед парсингом JSON
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Успех! Ответ сервера: {data}")
            print(f"Сообщение: {data['message']}")
        else:
            print(f"❌ Ошибка! Сервер вернул: {response.text}")

    except requests.exceptions.ConnectionError:
        print("❌ Не удалось подключиться к серверу. Убедитесь, что server.py запущен")
    except requests.exceptions.JSONDecodeError:
        print(f"❌ Сервер вернул не JSON ответ: {response.text}")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")

    print()

    print("=== 2. Тестируем POST /api/login ===")
    try:
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

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Логин успешен! Ответ: {data}")
        elif response.status_code == 401:
            data = response.json()
            print(f"❌ Ошибка авторизации: {data['error']}")
        else:
            print(f"⚠️ Неожиданный ответ: {response.text}")

    except requests.exceptions.ConnectionError:
        print("❌ Не удалось подключиться к серверу")
    except Exception as e:
        print(f"❌ Ошибка: {e}")


if __name__ == "__main__":
    test_api()