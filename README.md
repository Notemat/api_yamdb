# api_yamdb
api_yamdb

Проект YaMDb собирает отзывы пользователей на произведения.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка».
Произведению может быть присвоен жанр.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку.
Пользователи могут оставлять комментарии к отзывам.

### Стек используемых технологий:
Python, Django Rest Framework, SQLite

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Notemat/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3.9 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

```
cd api_yamdb
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Когда запустите проект, по адресу
``` 
http://127.0.0.1:8000/redoc/ 
```
будет доступна документация

### Как выполнить импорт из csv файлов в бд:
```
python3 manage.py users_import
```
```
python3 manage.py category_import
```
```
python3 manage.py genre_import
```
```
python3 manage.py titles_import
```
```
python3 manage.py genre_title_import
```
```
python3 manage.py review_import
```
```
python3 manage.py comments_import
```
### Запросы:
запросы к API начинаются с /api/v1/
/auth/signup/ : Регистрация нового пользователя
/auth/token/ : Получение JWT-токена
/categories/ : Получение списка всех категорий (GET) / Добавление новой категории (POST)
/categories/{slug}/ : Удаление категории
/genres/ : Получение списка всех жанров (GET) / Добавление жанра (POST)
/genres/{slug}/ : Удаление жанра
/titles/ : Получение списка всех произведений (GET) / Добавление произведения (POST)
/titles/{title_id}/ : Получение информации о произведении (GET) / Частичное обновление информации о произведении (PATCH) / Удаление произведения (DELETE)
/titles/{title_id}/reviews/ : Получение списка всех отзывов (GET) / Добавление нового отзыва (POST)
/titles/{title_id}/reviews/{review_id}/ : Полуение отзыва по id (GET) / Частичное обновление отзыва по id (PATCH) / Удаление отзыва по id (DELETE)
/titles/{title_id}/reviews/{review_id}/comments/ : Получение списка всех комментариев к отзыву (GET) / Добавление комментария к отзыву (POST)
/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/ : Получение комментария к отзыву (GET) / Частичное обновление комментария к отзыву (PATCH) / Удаление комментария к отзыву (DELETE)
/users/ : Получение списка всех пользователей (GET) / Добавление пользователя (POST)
/users/{username}/ : Получение пользователя по username (GET) / Изменение данных пользователя по username (PATCH) / Удаление пользователя по username (DELETE)
/users/me/ : Получение данных своей учетной записи (GET) / Изменение данных своей учетной записи (PATCH)

Более подробная информация в документации:
``` 
http://127.0.0.1:8000/redoc/ 
```



### Авторы:
Козлов Никита, Маркелова Татьяна, Зарифуллин Рафик