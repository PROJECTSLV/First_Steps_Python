import datetime
import random
import os
import json

# Файлы для хранения данных
DIARY_FILE = "my_diary.txt"
QUOTES_FILE = "quotes.txt"
CONFIG_FILE = "config.json"

# Настроения с эмодзи и цветами
MOODS = {
    "1": {"name": "😊 Радостное", "color": "🟡"},
    "2": {"name": "😢 Грустное", "color": "🔵"},
    "3": {"name": "❤️ Влюбленное", "color": "🔴"},
    "4": {"name": "😠 Злое", "color": "🟠"},
    "5": {"name": "😐 Нейтральное", "color": "⚪"},
    "6": {"name": "😨 Тревожное", "color": "🟣"},
    "7": {"name": "💪 Энергичное", "color": "🟢"}
}


def load_quotes():
    """Загружает цитаты из файла, если файла нет - создает стандартные"""
    default_quotes = [
        "Сегодня лучший день, чтобы начать что-то новое!",
        "Не откладывай на завтра то, что можешь сделать сегодня!",
        "Каждая маленькая победа - это шаг к большой цели!",
        "Ты способен на большее, чем думаешь!",
        "Плохой день - это не плохая жизнь!"
    ]

    try:
        with open(QUOTES_FILE, 'r', encoding='utf-8') as file:
            quotes = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        # Создаем файл с цитатами по умолчанию
        with open(QUOTES_FILE, 'w', encoding='utf-8') as file:
            for quote in default_quotes:
                file.write(quote + "\n")
        quotes = default_quotes

    return quotes


def show_random_quote():
    """Показывает случайную мотивирующую цитату"""
    quotes = load_quotes()
    if quotes:
        print(f"\n💫 Случайная цитата: {random.choice(quotes)}")


def setup_password():
    """Настройка пароля для дневника"""
    if os.path.exists(CONFIG_FILE):
        return True

    print("\n🔐 Давайте настроим защиту вашего дневника!")
    password = input("Придумайте пароль: ")

    config = {"password": password}
    with open(CONFIG_FILE, 'w', encoding='utf-8') as file:
        json.dump(config, file)

    print("✅ Пароль установлен!")
    return True


def check_password():
    """Проверяет правильность введенного пароля"""
    if not os.path.exists(CONFIG_FILE):
        return True

    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
            config = json.load(file)

        attempts = 3
        while attempts > 0:
            password_attempt = input("🔐 Введите пароль: ")
            if password_attempt == config["password"]:
                return True
            else:
                attempts -= 1
                print(f"❌ Неверный пароль! Осталось попыток: {attempts}")

        print("🚫 Доступ запрещен!")
        return False
    except:
        return True


def write_entry():
    """Функция для создания новой записи в дневнике"""
    print("\n--- Новая запись ---")

    # Показываем доступные настроения
    print("\nВыберите настроение:")
    for key, mood in MOODS.items():
        print(f"{key} - {mood['color']} {mood['name']}")

    # Выбор настроения
    mood_choice = input("\nВаш выбор (1-7): ")
    mood = MOODS.get(mood_choice, MOODS["5"])  # По умолчанию нейтральное

    # Получаем текущую дату и время
    now = datetime.datetime.now()
    date_str = now.strftime("%d.%m.%Y %H:%M")
    day_of_week = now.strftime("%A")

    # Русские названия дней недели
    days = {
        "Monday": "Понедельник",
        "Tuesday": "Вторник",
        "Wednesday": "Среда",
        "Thursday": "Четверг",
        "Friday": "Пятница",
        "Saturday": "Суббота",
        "Sunday": "Воскресенье"
    }

    text = input("\nРасскажите, что у вас нового: ")

    # Формируем запись с дополнительной информацией
    entry = f"""[{date_str}, {days.get(day_of_week, day_of_week)}]
    Настроение: {mood['color']} {mood['name']}
    Запись: {text}
    {'─' * 50}
    """

    # Открываем файл в режиме ДОБАВЛЕНИЯ
    with open(DIARY_FILE, 'a', encoding='utf-8') as file:
        file.write(entry)

    print("✅ Запись успешно сохранена!")


def read_entries():
    """Функция для чтения всех прошлых записей"""
    print("\n--- Ваши прошлые записи ---")

    try:
        with open(DIARY_FILE, 'r', encoding='utf-8') as file:
            content = file.read()

        if content:
            print(content)
            print(f"📊 Всего записей: {content.count('─' * 50)}")
        else:
            print("В вашем дневнике пока нет записей.")

    except FileNotFoundError:
        print("В вашем дневнике пока нет ни одной записи. Создайте первую!")


def search_entries():
    """Поиск записей по ключевым словам или настроению"""
    print("\n--- Поиск записей ---")
    print("1 - Поиск по ключевому слову")
    print("2 - Поиск по настроению")

    choice = input("Выберите тип поиска: ")

    try:
        with open(DIARY_FILE, 'r', encoding='utf-8') as file:
            entries = file.read().split('─' * 50)
    except FileNotFoundError:
        print("Дневник пуст!")
        return

    found_entries = []

    if choice == '1':
        keyword = input("Введите слово для поиска: ").lower()
        for entry in entries:
            if keyword in entry.lower():
                found_entries.append(entry)

    elif choice == '2':
        print("\nВыберите настроение для поиска:")
        for key, mood in MOODS.items():
            print(f"{key} - {mood['name']}")

        mood_choice = input("Ваш выбор: ")
        mood_name = MOODS.get(mood_choice, {}).get("name", "")

        if mood_name:
            for entry in entries:
                if mood_name in entry:
                    found_entries.append(entry)

    # Показываем результаты поиска
    if found_entries:
        print(f"\n🔍 Найдено записей: {len(found_entries)}")
        for entry in found_entries:
            if entry.strip():
                print(entry)
                print('─' * 50)
    else:
        print("❌ Записей не найдено.")


def add_quote():
    """Добавление новой цитаты"""
    print("\n--- Добавление новой цитаты ---")
    new_quote = input("Введите новую мотивирующую цитату: ")

    with open(QUOTES_FILE, 'a', encoding='utf-8') as file:
        file.write(new_quote + "\n")

    print("✅ Цитата добавлена!")


def diary_statistics():
    """Показывает статистику дневника"""
    try:
        with open(DIARY_FILE, 'r', encoding='utf-8') as file:
            content = file.read()

        total_entries = content.count('─' * 50)

        # Анализ настроений
        mood_stats = {}
        for mood in MOODS.values():
            count = content.count(mood["name"])
            if count > 0:
                mood_stats[mood["name"]] = count

        print("\n--- Статистика дневника ---")
        print(f"📈 Всего записей: {total_entries}")

        if mood_stats:
            print("\n📊 Статистика настроений:")
            for mood, count in mood_stats.items():
                percentage = (count / total_entries) * 100
                print(f"   {mood}: {count} зап. ({percentage:.1f}%)")

        # Самая длинная запись
        entries = content.split('─' * 50)
        if entries:
            longest_entry = max(entries, key=len)
            lines = longest_entry.strip().split('\n')
            if len(lines) >= 3:
                print(f"\n📝 Самая длинная запись: {len(longest_entry)} символов")
                print(f"   {lines[2][:50]}...")

    except FileNotFoundError:
        print("Дневник пуст!")


def main():
    """Основная функция программы"""

    # Настройка пароля при первом запуске
    if not setup_password():
        return

    # Проверка пароля
    if not check_password():
        return

    print("""
    ✨ Добро пожаловать в ваш расширенный дневник настроения! ✨
    """)

    # Показываем случайную цитату при запуске
    show_random_quote()

    while True:
        print("\n" + "=" * 50)
        print("Что вы хотите сделать?")
        print("1 - 📝 Сделать новую запись")
        print("2 - 📖 Прочитать все записи")
        print("3 - 🔍 Поиск по записям")
        print("4 - 💫 Добавить свою цитату")
        print("5 - 📊 Статистика дневника")
        print("6 - 🚪 Выйти")

        choice = input("\nВаш выбор (1-6): ")

        if choice == '1':
            write_entry()
        elif choice == '2':
            read_entries()
        elif choice == '3':
            search_entries()
        elif choice == '4':
            add_quote()
        elif choice == '5':
            diary_statistics()
        elif choice == '6':
            print("\nДо свидания! Хорошего дня! 🌟")
            break
        else:
            print("❌ Неверный выбор, попробуйте снова.")


# Запускаем программу
if __name__ == "__main__":
    main()