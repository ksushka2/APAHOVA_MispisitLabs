# IT-Школа — лабораторная работа №3

Информационная система детской IT-школы с сохранением данных.

## Запуск

Репозиторий: https://github.com
Ветка: lab3  
Pull Request: еще не сделала, сделаю
Образ: ksushkaap/mispisit-lab1:0.0.3  

```bash
git clone -b lab3 https://github.com
cd APAHOVA_MispisitLabs
docker compose up -d
```

Откройте в браузере: http://localhost:8080


## Сборка образа 0.0.3
```bash
docker buildx build --platform linux/amd64,linux/arm64 -t ksushkaap/mispisit-lab1:0.0.3 --push .
```
