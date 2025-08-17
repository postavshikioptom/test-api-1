import requests
import time
import logging
import threading
from datetime import datetime
from flask import Flask, jsonify
import os

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# URL для получения случайного анекдота
JOKE_API_URL = "https://official-joke-api.appspot.com/jokes/random"

# Flask приложение
app = Flask(__name__)

# Глобальная переменная для хранения последнего анекдота
last_joke = None
last_joke_time = None

def fetch_joke():
    """Получает случайный анекдот из API"""
    global last_joke, last_joke_time
    
    try:
        response = requests.get(JOKE_API_URL)
        response.raise_for_status()  # Проверка на ошибки HTTP
        joke_data = response.json()
        
        # Извлечение setup и punchline из ответа
        setup = joke_data.get('setup', 'Не удалось получить начало анекдота')
        punchline = joke_data.get('punchline', 'Не удалось получить конец анекдота')
        
        joke = f"{setup} - {punchline}"
        last_joke = joke
        last_joke_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        logger.info(f"Анекдот: {joke}")
        return joke
    except requests.exceptions.RequestException as e:
        error_msg = f"Ошибка при запросе к API: {e}"
        logger.error(error_msg)
        return error_msg
    except ValueError as e:
        error_msg = f"Ошибка при парсинге JSON: {e}"
        logger.error(error_msg)
        return error_msg

def joke_worker():
    """Фоновый поток для периодического получения анекдотов"""
    logger.info("Запуск фонового сервиса получения анекдотов")
    
    # Получаем первый анекдот сразу при запуске
    fetch_joke()
    
    while True:
        try:
            logger.info("Ожидание 5 минут до следующего запроса...")
            # Ждем 5 минут (300 секунд) перед следующим запросом
            time.sleep(300)
            
            logger.info("Получение случайного анекдота...")
            fetch_joke()
            
        except Exception as e:
            logger.error(f"Неожиданная ошибка в фоновом потоке: {e}")
            # Ждем 1 минуту перед повторной попыткой
            time.sleep(60)

# Маршруты Flask
@app.route('/')
def index():
    """Главная страница с информацией о сервисе"""
    return jsonify({
        "message": "Joke Fetcher Service",
        "status": "running",
        "last_joke": last_joke,
        "last_joke_time": last_joke_time,
        "next_fetch_in_seconds": 300
    })

@app.route('/joke')
def get_joke():
    """Получить последний анекдот"""
    return jsonify({
        "joke": last_joke,
        "timestamp": last_joke_time
    })

@app.route('/health')
def health_check():
    """Проверка здоровья сервиса для Leapcell"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

def start_background_thread():
    """Запуск фонового потока"""
    thread = threading.Thread(target=joke_worker, daemon=True)
    thread.start()
    logger.info("Фоновый поток запущен")

if __name__ == "__main__":
    # Запуск фонового потока для получения анекдотов
    start_background_thread()
    
    # Получаем порт из переменной окружения или используем 8080 по умолчанию
    port = int(os.environ.get('PORT', 8080))
    
    # Запуск Flask приложения
    logger.info(f"Запуск веб-сервера на порту {port}")
    app.run(host='0.0.0.0', port=port, debug=False)