## Описание

Foodgram - это сервис, который позволяет пользователям публиковать рецепты, подписываться на других пользователей, добавлять любимые рецепты в список "Избранное" и скачивать сводный список продуктов перед походом в магазин для приготовления выбранных блюд. Foodgram предоставляет удобную платформу для обмена рецептами и вдохновения в кулинарной области. Это место, где пользователи могут делиться своими любимыми блюдами, находить новые идеи для готовки и наслаждаться кулинарным опытом в сообществе единомышленников.


## Основной стек технологий

- #### Django
- #### DRF
- #### Postgres
- #### Nginx
- #### Docker Compose
- #### React

## Инструкция для запуска

#### Перейдите в директорию infra и выполните команду
```
docker-compose -f docker-compose.yml up -d
```

#### Выполните миграции, соберите статику, создайте админа и загрузите данные в базу данных
```
docker exec -it <имя> python manage.py migrate
docker exec -it <имя> python manage.py collectstatic
docker exec -it <имя> python manage.py createsuperuser
docker exec -it <имя> python manage.py load_db
```
#### Foodgram
```
localhost
```
#### Докементация по API
```
localhost/api/docs/
```
#### Админка
```
localhost/admin/
```

## Сайт доступен по адресу: http://158.160.29.155/

### Автор:
[Сенягин Сергей](https://github.com/Senyagin)