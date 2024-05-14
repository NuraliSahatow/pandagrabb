import telebot
import requests
import json
import random
import schedule
import time
from threading import Thread

API_TOKEN = '7160651479:AAFJ2Pl6yuWoty3oReOjAHd-uO9ipi4mJp4'
CHAT_ID = '-1001158649839'  # Используйте здесь полученный chat ID
API_URL = "https://shadowmere.akiel.dev/api/proxies/?format=json&is_active=true&location_country_code=&port=&page=1"
UNSPLASH_ACCESS_KEY = '9dCgHjNsmy9iC3M244EpTzdu2ZrdZsujnlf_alh2-vg'  # Ваш Access Key от Unsplash
UNSPLASH_API_URL = "https://api.unsplash.com/photos/random?query=panda&count=1"
TOPIC_ID = 44429  # Используйте здесь полученный message_thread_id для топика "Need"

bot = telebot.TeleBot(API_TOKEN)
#@bot.message_handler(func=lambda message: True)
#def handle_all_messages(message):
 #   print(message)
def fetch_data():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Проверка на ошибки HTTP
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return None

def format_message(data):
    if not data or 'results' not in data:
        return "Нет данных для отображения."
    
    message = ""  # Инициализация переменной message
    c = 0

    for proxy in data['results']:
        message += f"IP: {proxy['ip_address']}\n"
        message += f"Порт: {proxy['port']}\n"
        message += f"Локация: {proxy['location']} ({proxy['location_country']})\n"
        message += f"URL: `{proxy['url']}`\n"  # Добавление моноширинного форматирования
        message += "---------------------------------Бот сделан @pandistt---------------------------------\n"  # Измененная строка
        c += 1
        if c == 1:
            break
    return message

def fetch_panda_image():
    headers = {
        'Authorization': f'Client-ID {UNSPLASH_ACCESS_KEY}'
    }
    try:
        response = requests.get(UNSPLASH_API_URL, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data:
            return data[0]['urls']['regular']
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return None

@bot.message_handler(commands=['panda'])
def send_panda_image(message):
    panda_image_url = fetch_panda_image()
    if panda_image_url:
        bot.send_photo(message.chat.id, panda_image_url,reply_to_message_id=TOPIC_ID)
    else:
        bot.send_message(message.chat.id, "Не удалось получить изображение панды.")

def main():
    data = fetch_data()
    message = format_message(data)
    panda_image_url = fetch_panda_image()
    if panda_image_url:
        print("Отправлено")
        bot.send_photo(CHAT_ID, panda_image_url, caption=message, reply_to_message_id=TOPIC_ID, parse_mode='Markdown')
    else:
        print("Не удалось получить изображение панды.")

def job():
    main()

# Планирование задачи каждые 1 час
schedule.every(1).minutes.do(job)

# Функция для запуска планировщика в отдельном потоке
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    # Запуск планировщика в отдельном потоке
    scheduler_thread = Thread(target=run_schedule)
    scheduler_thread.start()

    # Запуск бота
    bot.polling()
