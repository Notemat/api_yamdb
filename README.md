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

### Авторы:
Козлов Никита, Маркелова Татьяна, Зарифуллин Рафик