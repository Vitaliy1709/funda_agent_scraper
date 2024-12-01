# funda_agent_scraper

**Funda Agent Scraper** — это проект для веб-скрейпинга, который собирает подробную информацию о риелторских агентствах с платформы Funda. Полученные данные сохраняются в базу данных PostgreSQL для дальнейшего анализа и обработки.

## Основные возможности

- Сбор подробной информации о риелторских агентствах, включая:
  - Имя риелтора
  - Контактные данные (телефон, email, веб-сайт)
  - Адрес
  - Рейтинги и отзывы
  - Сертификаты и языки
  - Ссылки на социальные сети
- Сохранение данных в базе PostgreSQL с использованием Django ORM.
- Поддержка извлечения динамического контента с помощью BeautifulSoup.
- Безопасное обращение к данным через вспомогательные функции.

## Используемые технологии

- **Python**: Основной язык программирования.
- **Django**: Для взаимодействия с базой данных.
- **BeautifulSoup**: Для веб-скрейпинга.
- **Requests**: Для выполнения HTTP-запросов.
- **PostgreSQL**: База данных для хранения информации.

## Настройка и установка

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/your-username/funda-agent-scraper.git
   cd funda-agent-scraper
   
2. **Создайте и активируйте виртуальное окружение:**
python3 -m venv venv
source venv/bin/activate  # Для Linux/Mac
venv\Scripts\activate  # Для Windows

3. **Установите зависимости:**
pip install -r requirements.txt

4. **Настройте базу данных PostgreSQL**

5. **Примените миграции базы данных:**
python manage.py makemigrations
python manage.py migrate

6. **Запустите скрейпинг:**
python modules/parse_agent.py






