# IT-Школа — лабораторная работа №3

Информационная система детской IT-школы. Версия 0.0.3. Курсы и заявки хранятся в PostgreSQL 18.

## Демонстрация на компьютере автора

Восстановленный образ mispisit-it-school-lab3-local:0.0.3 уже собран на этом компьютере из исходников третьей работы. Для запуска выполните в CMD:

```cmd
cd /d "C:\Users\Ксюня\Documents\ChatGPT\мисписит\lab3-restored"
docker compose -f docker-compose.yml -f docker-compose.local.yml up -d --force-recreate app
```

Адрес: http://localhost:8080. На странице должна отображаться версия 0.0.3. Том с прежними заявками сохраняется.

## Запуск

Репозиторий: https://github.com/ksushka2/APAHOVA_MispisitLabs

Ветка: lab3

Pull Request: https://github.com/ksushka2/APAHOVA_MispisitLabs/pull/3

Образ: ksushkaap/mispisit-lab1:0.0.3

Состояние на 11.11.2026: опубликованный тег 0.0.3 ошибочно содержит код версии 0.0.4. Следующий блок предназначен для запуска после восстановления правильного образа в Docker Hub. До этого для демонстрации третьей работы используйте локальный запуск выше.

Требуются Git и Docker с поддержкой Docker Compose. На Windows запустите Docker Desktop и дождитесь его готовности.

Первый запуск на другом компьютере:

```cmd
git clone -b lab3 https://github.com/ksushka2/APAHOVA_MispisitLabs APAHOVA_MispisitLabs-lab3
cd APAHOVA_MispisitLabs-lab3
docker compose pull
docker compose up -d
```

Команда pull скачивает приложение и PostgreSQL, команда up запускает их совместно. Отдельный docker run после Compose не требуется. Откройте http://localhost:8080 и проверьте версию 0.0.3.

## Страницы

| Адрес | Назначение |
| --- | --- |
| / | Главная и версия |
| /requests/ | Список сохранённых заявок |
| /requests/new/ | Подача заявки на курс |
| /requests/<id>/ | Карточка заявки |
| /access-denied/ | Причина отказа |

## Остановка

Для восстановленной локальной копии:

```cmd
docker compose -f docker-compose.yml -f docker-compose.local.yml stop
```

Для запуска скачанного образа:

```cmd
docker compose stop
```

Том dbdata и заявки сохраняются.

## Подготовка правильного образа третьей работы

Восстановленные исходники находятся в папке lab3-restored. В них добавлена начальная миграция прежних моделей Course и StudentRequest, чтобы таблицы создавались и на новом компьютере с пустой базой. Существующие таблицы и записи не удаляются.

Следующая команда публикует правильный код третьей работы под ошибочно перезаписанным тегом 0.0.3. Её выполняет автор после согласования восстановления тега:

```cmd
cd /d "C:\Users\Ксюня\Documents\ChatGPT\мисписит\lab3-restored"
docker buildx build --platform linux/amd64,linux/arm64 -t ksushkaap/mispisit-lab1:0.0.3 --push .
docker buildx imagetools inspect ksushkaap/mispisit-lab1:0.0.3
```

Файлы и миграция восстановленной копии также должны попасть в ветку lab3 перед передачей репозитория преподавателю. В ходе подготовки README публикация не выполнялась.
