import os
import random
from PIL import Image, ImageDraw, ImageFont
import pygame
import time


class MusicCollage:
    def __init__(self):
        self.music_folder = "music"
        self.images_folder = "images"
        self.output_folder = "collages"
        self.setup_folders()

        # Инициализируем pygame для музыки
        pygame.mixer.init()

    def setup_folders(self):
        """Создает необходимые папки если их нет"""
        for folder in [self.music_folder, self.images_folder, self.output_folder]:
            if not os.path.exists(folder):
                os.makedirs(folder)
                print(f"📁 Создана папка: {folder}")

    def get_music_files(self):
        """Получает список музыкальных файлов"""
        music_extensions = ['.mp3', '.wav']
        music_files = []

        for file in os.listdir(self.music_folder):
            if any(file.lower().endswith(ext) for ext in music_extensions):
                music_files.append(file)

        return music_files

    def get_image_files(self):
        """Получает список изображений"""
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
        image_files = []

        for file in os.listdir(self.images_folder):
            if any(file.lower().endswith(ext) for ext in image_extensions):
                image_files.append(file)

        return image_files

    def play_random_music(self):
        """Воспроизводит случайную музыку"""
        music_files = self.get_music_files()

        if not music_files:
            print("❌ В папке 'music' нет музыкальных файлов!")
            print("   Добавьте несколько MP3 или WAV файлов")
            return None

        random_music = random.choice(music_files)
        music_path = os.path.join(self.music_folder, random_music)

        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play()
            print(f"🎵 Сейчас играет: {random_music}")
            return random_music
        except:
            print(f"❌ Не удалось воспроизвести: {random_music}")
            return None

    def create_collage(self, music_name):
        """Создает коллаж из случайных изображений"""
        image_files = self.get_image_files()

        if not image_files:
            print("❌ В папке 'images' нет изображений!")
            print("   Добавьте несколько JPG или PNG файлов")
            return

        # Создаем холст для коллажа
        collage = Image.new('RGB', (800, 600), 'black')
        draw = ImageDraw.Draw(collage)

        # Пробуем добавить шрифт (если доступно)
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()

        # Добавляем 4 случайных изображения на коллаж
        used_positions = []
        for i in range(min(4, len(image_files))):
            img_name = random.choice(image_files)
            image_files.remove(img_name)  # Убираем чтобы не повторяться

            try:
                img = Image.open(os.path.join(self.images_folder, img_name))
                img = img.resize((300, 200))

                # Случайная позиция на холсте
                x = random.randint(50, 450)
                y = random.randint(50, 350)

                # Проверяем чтобы изображения не сильно перекрывались
                while any(abs(x - px) < 100 and abs(y - py) < 100 for px, py in used_positions):
                    x = random.randint(50, 450)
                    y = random.randint(50, 350)

                used_positions.append((x, y))
                collage.paste(img, (x, y))

            except Exception as e:
                print(f"❌ Ошибка при обработке {img_name}: {e}")

        # Добавляем название музыки на коллаж
        draw.text((400, 500), f"Музыка: {music_name}", fill='white', font=font, anchor="mm")
        draw.text((400, 530), "Создано в Музыкальном Коллаже", fill='yellow', font=font, anchor="mm")

        # Сохраняем коллаж
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_folder, f"collage_{timestamp}.png")
        collage.save(output_path)

        print(f"🎨 Коллаж сохранен: {output_path}")
        return output_path

    def show_folder_info(self):
        """Показывает информацию о файлах в папках"""
        print(f"\n📊 Информация о файлах:")
        print(f"🎵 Музыкальных файлов: {len(self.get_music_files())}")
        print(f"🖼️ Изображений: {len(self.get_image_files())}")
        print(f"🎨 Создано коллажей: {len(os.listdir(self.output_folder))}")

    def main_menu(self):
        """Главное меню программы"""
        print("""
        🎵🖼️ Добро пожаловать в МУЗЫКАЛЬНЫЙ КОЛЛАЖ! 🖼️🎵

        Эта программа создает уникальные коллажи из ваших изображений
        под случайную музыку из вашей коллекции!
        """)

        while True:
            print("\n" + "=" * 50)
            print("Что вы хотите сделать?")
            print("1 - 🎵 Слушать музыку и создать коллаж")
            print("2 - 📊 Показать информацию о файлах")
            print("3 - ❌ Остановить музыку")
            print("4 - 🚪 Выйти")

            choice = input("\nВаш выбор (1-4): ")

            if choice == '1':
                # Воспроизводим музыку и создаем коллаж
                music_name = self.play_random_music()
                if music_name:
                    self.create_collage(music_name)

            elif choice == '2':
                self.show_folder_info()

            elif choice == '3':
                pygame.mixer.music.stop()
                print("⏹️ Музыка остановлена")

            elif choice == '4':
                pygame.mixer.music.stop()
                print("👋 До свидания! Ваши коллажи ждут в папке 'collages'")
                break
            else:
                print("❌ Неверный выбор, попробуйте снова")


def check_dependencies():
    """Проверяет установлены ли необходимые библиотеки"""
    try:
        import pygame
        from PIL import Image
        return True
    except ImportError as e:
        print("❌ Необходимо установить библиотеки:")
        print("   pip install pygame pillow")
        print(f"   Ошибка: {e}")
        return False


# Запуск программы
if __name__ == "__main__":
    if check_dependencies():
        app = MusicCollage()
        app.main_menu()