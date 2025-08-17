import requests
import time
import logging
from datetime import datetime

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

def fetch_joke():
    """Получает случайный анекдот из API"""
    try:
        response = requests.get(JOKE_API_URL)
        response.raise_for_status()  # Проверка на ошибки HTTP
        joke_data = response.json()
        
        # Извлечение setup и punchline из ответа
        setup = joke_data.get('setup', 'Не удалось получить начало анекдота')
        punchline = joke_data.get('punchline', 'Не удалось получить конец анекдота')
        
        return setup, punchline
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе к API: {e}")
        return None, None
    except ValueError as e:
        logger.error(f"Ошибка при парсинге JSON: {e}")
        return None, None

def main():
    """Основная функция для периодического получения анекдотов"""
    logger.info("Запуск сервиса получения анекдотов")
    
    while True:
        try:
            logger.info("Получение случайного анекдота...")
            setup, punchline = fetch_joke()
            
            if setup and punchline:
                logger.info(f"Анекдот: {setup} - {punchline}")
            else:
                logger.warning("Не удалось получить анекдот")
            
            # Ждем 5 минут (300 секунд) перед следующим запросом
            logger.info("Ожидание 5 минут до следующего запроса...")
            time.sleep(300)
            
        except KeyboardInterrupt:
            logger.info("Сервис остановлен пользователем")
            break
        except Exception as e:
            logger.error(f"Неожиданная ошибка: {e}")
            # Ждем 1 минуту перед повторной попыткой
            time.sleep(60)

if __name__ == "__main__":
    main()