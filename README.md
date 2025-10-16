🛍️ MusShop — Онлайн-магазин уникальных товаров

MusShop — это современная e-commerce платформа, разработанная на Django Framework, предназначенная для продажи эксклюзивных товаров (ароматов, аксессуаров, ковриков, предметов интерьера и др.). Проект ориентирован на создание эстетичного и функционального пользовательского опыта, объединяя удобство, скорость и минимализм дизайна.

🚀 Основные возможности

🧾 Каталог товаров — отображение товаров по категориям с фильтрацией по типу, цене и популярности

📦 Карточка товара — детальное описание, изображения, цена, кнопка “Добавить в корзину”

🛒 Корзина и оформление заказа

👤 Регистрация и авторизация пользователей

💬 Форма обратной связи (отправка сообщений администратору)

📱 Адаптивный дизайн — корректное отображение на мобильных устройствах

⚙️ Панель администратора Django для управления товарами и заказами

🌐 Деплой на сервер (Nginx + Gunicorn + Ubuntu)

🧠 Технологии
Категория	Технологии
Backend	Python 3.11, Django 5.x
Frontend	HTML5, CSS3, Bootstrap 5.3, JavaScript
База данных	SQLite (на dev), PostgreSQL (на продакшене)
Сервер	Nginx, Gunicorn, systemd
Развёртывание	Ubuntu 22.04, Hoster.kz
Контроль версий	Git + GitHub
Хранилище медиа	/media/ и /static/ каталоги, поддержка Cloudinary (опционально)
📂 Структура проекта
MusShop/
│
├── MusShop/                 # Главная конфигурация проекта (settings, urls, wsgi)
├── shop/                    # Приложение с логикой магазина
│   ├── models.py            # Модели товаров, категорий, заказов
│   ├── views.py             # Представления
│   ├── templates/shop/      # HTML шаблоны
│   ├── static/shop/         # Статические файлы (CSS, JS, изображения)
│
├── media/                   # Загруженные изображения
├── staticfiles/             # Скомпилированная статика для продакшена
├── manage.py                # Django CLI
└── requirements.txt         # Список зависимостей

⚙️ Установка и запуск
1️⃣ Клонирование репозитория
git clone https://github.com/Arlasha-prog/musshop.git
cd musshop

2️⃣ Создание виртуального окружения
python -m venv .venv
source .venv/bin/activate     # Linux/Mac
.venv\Scripts\activate        # Windows

3️⃣ Установка зависимостей
pip install -r requirements.txt

4️⃣ Применение миграций и создание суперпользователя
python manage.py migrate
python manage.py createsuperuser

5️⃣ Запуск локального сервера
python manage.py runserver


Открой: 👉 http://127.0.0.1:8000

🖥️ Деплой на сервер

Настрой Gunicorn

ExecStart=/srv/musshop/.venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8001 MusShop.wsgi:application


Настрой Nginx

server {
    listen 80;
    server_name musshop.asia www.musshop.asia;

    location /static/ { alias /srv/musshop/staticfiles/; }
    location /media/  { alias /srv/musshop/media/; }

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}


Запусти службы

sudo systemctl daemon-reload
sudo systemctl enable gunicorn-musshop
sudo systemctl start gunicorn-musshop
sudo systemctl restart nginx



🧩 Будущие обновления

✅ Оптимизация под SEO

🛍️ Интеграция онлайн-оплаты (Kaspi, Paybox, Stripe)

📊 Добавление панели аналитики продаж

📦 Раздел “Избранное” и “Отзывы покупателей”

👨‍💻 Автор

Arlasha Prog
📧 @Arlasha-prog

🌐 musshop.asia

📜 Лицензия

Проект распространяется под лицензией MIT License.
