# yamdb_final
![workflow](https://github.com/nnigromontan/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
### Описание
Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles).  
Произведения делятся на категории: «Книги», «Фильмы», «Музыка».  
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.  
В каждой категории есть конкретные произведения: книги, фильмы или музыка.  
Произведению может быть присвоен жанр (Genre) из списка предустановленных  
(например, «Сказка», «Рок» или «Артхаус»).  
Пользователи оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку  
в диапазоне от одного до десяти (целое число);  
из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число).  
**Предусмотрены следующие пользовательские роли:**  
**Аноним** — может просматривать описания произведений, читать отзывы и комментарии.  
**Аутентифицированный пользователь (user)** — может, как и Аноним, читать всё,  
дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам),  
может комментировать чужие   отзывы; может редактировать и удалять свои отзывы и комментарии.  
Эта роль присваивается по умолчанию каждому новому пользователю.  
**Модератор (moderator)** — те же права, что и у Аутентифицированного пользователя плюс право удалять  
любые отзывы и комментарии.  
**Администратор (admin)** — полные права на управление всем контентом проекта.  
Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.  
**Суперюзер Django** — обладет правами администратора (admin)  
### Технологии
- **Python 3.7**
- **Django 2.2.16**
- **Django Rest Framework 3.12.4**
- **SimpleJWT 4.8.0**
- **Nginx 1.21.6**
- **Docker v20.10.21**
- **Gunicorn 20.0.4**
- **PostgreSQL Psycopg 2.8.6**

### Как запустить проект
Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:nnigromontan/yamdb_final.git
```

```
cd yamdb_final/infra/
```

Запустить композицию контейнеров Docker:

```
docker-compose up -d --build

```

Выполнить миграции и собрать статику:

```
docker-compose exec web python manage.py migrate

```

```
docker-compose exec web python manage.py collectstatic --no-input

```

Существует возможность заполнения базы данных тестовыми данными, находящимися в файлах csv в директории `static/data`.
Создать фикстуры из файлов:

```
docker-compose exec web python manage.py create_fixtures
```
Заполнить базу данных из фикстур:

```
docker-compose exec web python manage.py populate_fixtures
```
### Примеры работы с проектом
**Алгоритм регистрации пользователей**  
1.Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами email и username на эндпоинт /api/v1/auth/signup/.
2.YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес email.
3.Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен).
4.При желании пользователь отправляет PATCH-запрос на эндпоинт /api/v1/users/me/ и заполняет поля в своём профайле.  
*Примеры:*
*При POST запросе на эндпоинт /api/v1/auth/signup/ с таким содержимым:*  
*{*  
*"email": "string",*  
*"username": "string"*  
*}*  
*Будет отправлен confirmation_code на адрес email и получен ответ со статусом 200.*  
*Далее необходимо подтвердить регистрацию. При POST запросе на эндпоинт /api/v1/auth/token/ с таким содержимым:*  
*{*  
*"username": "string",*  
*"confirmation_code": "string"*  
*}*  
*В ответ будет получен jwt-токен:*  
*{*  
*"token": "string",*  
*}*  
**Работа с категориями**  
Любой пользователь может посмотреть список категорий, отправив GET-запрос на эндпоинт /api/v1/categories/  
В ответ придет *пагинированный* перечень:  
*{*  
*"name": "string",*  
*"slug": "string"*  
*}*  
Добавить категорию может только администратор, отправив следующий POST-запрос на эндпоинт /api/v1/categories/:  
*{*  
*"name": "string",*  
*"slug": "string"*  
*}*  
Администратор также может удалить категорию, отправив соответствующий запрос на эндпоинт /api/v1/categories/{slug}/  
**Работа с жанрами**  
Любой пользователь может посмотреть список жанров, отправив GET-запрос на эндпоинт /api/v1/genres/  
В ответ придет *пагинированный* перечень:  
*{*  
*"name": "string",*  
*"slug": "string"*  
*}*  
Добавить жанр может только администратор, отправив следующий POST-запрос на эндпоинт /api/v1/genres/:  
*{*  
*"name": "string",*  
*"slug": "string"*  
*}*  
Администратор также может удалить жанр, отправив соответствующий запрос на эндпоинт /api/v1/genres/{slug}/  
**Для более подробного описания запустите сервер и перейдите по ссылке http://127.0.0.1/redoc/**  
**Или по внешнему адресу проекта: http://62.84.127.162/redoc/**
### Авторы
Валентин Корзюк, Александр Богус и Динеев Артур под чутким руководством команды ЯП
