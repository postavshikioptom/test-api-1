# Test API Project - Анекдоты каждые 5 минут

## Описание проекта
Этот проект автоматически получает случайный анекдот из публичного API каждые 5 минут и выводит его в логи. Проект представляет собой веб-приложение на Flask, которое можно развернуть на платформе Leapcell.

## Функциональность
- Получение случайного анекдота каждые 5 минут
- Вывод анекдотов в логи с временной меткой
- Обработка ошибок сети и API
- Веб-интерфейс с API endpoints

## Технические детали

### Используемый API
Проект использует [Official Joke API](https://official-joke-api.appspot.com/) для получения анекдотов.

Пример ответа от API:
```json
{
  "id": 1,
  "type": "general",
  "setup": "Why did the scarecrow win an award?",
  "punchline": "Because he was outstanding in his field!"
}
```

### Endpoints приложения
- `GET /` - Главная страница с информацией о сервисе
- `GET /joke` - Получить последний анекдот
- `GET /health` - Проверка здоровья сервиса (для Leapcell)
- `GET /kaithhealthcheck` - Специальный endpoint для проверки здоровья Leapcell

### Структура проекта
```
test-api-1/
├── joke_fetcher.py          # Основной скрипт с веб-сервером Flask
├── requirements.txt         # Зависимости проекта
├── leapcell.yaml           # Конфигурационный файл для Leapcell
└── README.md               # Документация проекта
```

## Установка и запуск локально

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/ваш_логин/test-api-1.git
   cd test-api-1
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Запустите скрипт:
   ```bash
   python joke_fetcher.py
   ```

4. Откройте в браузере:
   - http://localhost:8080/ - главная страница
   - http://localhost:8080/joke - последний анекдот
   - http://localhost:8080/health - проверка здоровья
   - http://localhost:8080/kaithhealthcheck - проверка здоровья для Leapcell

## Развертывание на Leapcell

Следуйте инструкциям в файле [human_instruction.md](human_instruction.md) для развертывания проекта на платформе Leapcell.

## Логирование
Все анекдоты и события записываются в логи с временной меткой. В панели управления Leapcell вы можете просматривать логи в реальном времени.

## Лицензия
Этот проект распространяется под лицензией MIT.