import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
TELEGRAM_BOT_TOKEN = ''
# Замените 'CHAT_ID' на ID вашего чата в Telegram
TELEGRAM_CHAT_ID = ''

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        self.send_telegram_message(f"Файл изменен или открыт: {event.src_path}")

    def on_deleted(self, event):
        if event.is_directory:
            return
        self.send_telegram_message(f"Файл удален: {event.src_path}")

    def on_moved(self, event):
            if event.is_directory:
                return
            self.send_telegram_message(f"Файл переименнован: {event.src_path}")

    def send_telegram_message(self, message):
        telegram_api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        params = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message,
        }
        requests.post(telegram_api_url, params=params)

if __name__ == "__main__":
    path = '.'  # Текущая директория, можно изменить на нужный путь

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)

    print("Наблюдение начато. Ожидание изменений...")

    try:
        observer.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()