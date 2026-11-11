# IT-Школа — лабораторная работа №3

Информационная система детской IT-школы. Версия 0.0.3.

В работе реализовано постоянное хранение курсов и заявок в PostgreSQL 18. Приложение позволяет подать заявку на курс, посмотреть сохранённые заявки и получить отказ при неподходящем возрасте ребёнка.

Используются Python 3.11, Django 4.2.16, PostgreSQL 18 и Docker Compose.

## Запуск

Репозиторий: https://github.com/ksushka2/APAHOVA_MispisitLabs

Ветка: lab3

Pull Request: https://github.com/ksushka2/APAHOVA_MispisitLabs/pull/3

Образ: ksushkaap/mispisit-lab1:0.0.3

Для запуска необходимы Git и Docker с поддержкой Docker Compose. На Windows запустите Docker Desktop и дождитесь его готовности. Порт 8080 должен быть свободен.

Откройте CMD или терминал и выполните команды по очереди:

```cmd
git clone -b lab3 https://github.com/ksushka2/APAHOVA_MispisitLabs APAHOVA_MispisitLabs-lab3
cd APAHOVA_MispisitLabs-lab3
docker compose pull
docker compose up -d
```

Команда `docker compose pull` скачивает образы приложения и PostgreSQL. Команда `docker compose up -d` запускает оба сервиса.

Откройте в браузере: http://localhost:8080

На главной странице должна отображаться версия 0.0.3.

## Повторный запуск

Из папки третьей лабораторной работы выполните:

```cmd
docker compose up -d
```

## Остановка

Из той же папки выполните:

```cmd
docker compose stop
```

Данные PostgreSQL сохраняются в томе dbdata и остаются доступными после перезапуска контейнеров.

## Страницы приложения

| Адрес | Назначение |
| --- | --- |
| / | Главная страница |
| /requests/ | Список заявок |
| /requests/new/ | Создание заявки |
| /requests/<id>/ | Карточка заявки |
| /access-denied/ | Страница отказа |
