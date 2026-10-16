# IT-Школа — лабораторная работа №3

Информационная система детской IT-школы с сохранением данных.

## Запуск

Репозиторий: https://github.com/ksushka2/APAHOVA_MispisitLabs

Ветка: lab3

Pull: https://github.com/ksushka2/APAHOVA_MispisitLabs/pull/3

Образ: ksushkaap/mispisit-lab1:0.0.3

Страница образа: https://hub.docker.com/r/ksushkaap/mispisit-lab1


### Страницы

| Адрес | Назначение |
|-------|------------|
| `/` | Главная |
| `/requests` | Список заявок |
| `/requests/new` | Создание заявки |
| `/requests/1` | Карточка заявки |
| `/access-denied` | Отказ / ошибочный сценарий |
 

```bash
git clone -b lab3 https://github.com/ksushka2
cd APAHOVA_MispisitLabs
docker compose up -d
```

Откройте в браузере: http://localhost:8080


## Сборка образа 0.0.3
```bash
docker buildx build --platform linux/amd64,linux/arm64 -t ksushkaap/mispisit-lab1:0.0.3 --push .
```
