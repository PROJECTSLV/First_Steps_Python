import requests


def test_remote_server():
    server_ip = input("Введите IP-адрес сервера (192.168.1.35): ").strip()
    BASE_URL = f"http://{server_ip}:8000"

    print(f"🔗 Подключаемся к серверу: {BASE_URL}")
    print()

    # Остальной код такой же, но с улучшенными сообщениями
    print("=== 1. Тестируем GET /api/status ===")
    try:
        response = requests.get(f"{BASE_URL}/api/status", timeout=5)
        print(f"Код статуса: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Успешное подключение к серверу!")
            print(f"📊 Ответ сервера: {data}")
        else:
            print(f"❌ Сервер ответил ошибкой: {response.text}")

    except requests.exceptions.ConnectionError:
        print("❌ Не удалось подключиться к серверу. Проверьте:")
        print("   • Запущен ли сервер на удаленном компьютере")
        print("   • Правильный ли IP-адрес")
        print("   • Разрешен ли доступ через брандмауэр")
    except requests.exceptions.Timeout:
        print("❌ Таймаут соединения. Сервер не отвечает")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")


if __name__ == "__main__":
    test_remote_server()