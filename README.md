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

#### API Endpoints
##### Аутентификация
###### ```/auth/signup/```: Регистрация нового пользователя
Request sample (POST)
```
{
  "username": "^w\\Z",
  "confirmation_code": "string"
}
```
Response sample
```
{
  "token": "string"
}
```
###### ```/auth/token/```: Получение JWT-токена
##### Категории
###### ```/categories/```: Получение списка всех категорий (GET) / Добавление новой категории (POST)
Response sample (GET)
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "name": "string",
      "slug": "^-$"
    }
  ]
}
```
###### ```/categories/{slug}/```: Удаление категории
##### Жанры
###### ```/genres/```: Получение списка всех жанров (GET) / Добавление жанра (POST)
Request sample (POST)
```
{
  "name": "string",
  "slug": "^-$"
}
```
Response sample
```
{
  "name": "string",
  "slug": "string"
}
```
###### ```/genres/{slug}/```: Удаление жанра
##### Произведения
###### ```/titles/```: Получение списка всех произведений (GET) / Добавление произведения (POST)
Response sample (GET)
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "name": "string",
      "year": 0,
      "rating": 0,
      "description": "string",
      "genre": [
        {
          "name": "string",
          "slug": "^-$"
        }
      ],
      "category": {
        "name": "string",
        "slug": "^-$"
      }
    }
  ]
}
```
###### ```/titles/{title_id}/```: Получение информации о произведении (GET) / Частичное обновление информации о произведении (PATCH) / Удаление произведения (DELETE)
###### ```/titles/{title_id}/reviews/```: Получение списка всех отзывов (GET) / Добавление нового отзыва (POST)
###### ```/titles/{title_id}/reviews/{review_id}/```: Получение отзыва по id (GET) / Частичное обновление отзыва по id (PATCH) / Удаление отзыва по id (DELETE)
Response sample (GET)
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```
###### ```/titles/{title_id}/reviews/{review_id}/comments/```: Получение списка всех комментариев к отзыву (GET) / Добавление комментария к отзыву (POST)
Request sample (POST)
```
{
  "text": "string"
}
```
Response sample
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```
###### ```/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/```: Получение комментария к отзыву (GET) / Частичное обновление комментария к отзыву (PATCH) / Удаление комментария к отзыву (DELETE)
##### Пользователи
###### ```/users/```: Получение списка всех пользователей (GET) / Добавление пользователя (POST)
###### ```/users/{username}/```: Получение пользователя по username (GET) / Изменение данных пользователя по username (PATCH) / Удаление пользователя по username (DELETE)
Response sample (GET)
```
{
  "username": "^w\\Z",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
###### ```/users/me/```: Получение данных своей учетной записи (GET) / Изменение данных своей учетной записи (PATCH)

Более подробная информация в документации:
``` 
http://127.0.0.1:8000/redoc/ 
```



### Авторы:
Козлов Никита, Маркелова Татьяна, Зарифуллин Рафик
