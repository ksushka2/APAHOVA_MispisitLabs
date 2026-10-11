IT-Школа — лабораторная работа №1

Информационная система детской IT-школы.  
В этой работе — стартовая страница в Docker-образе.

## Запуск готового образа

### Docker Hub

```bash
docker pull ksushkaap/mispisit-lab1:0.0.1
docker run --rm -p 8080:8080 ksushkaap/mispisit-lab1:0.0.1
```

Откройте в браузере: http://localhost:8080


## Локальная разработка

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver 8080
```

## Сборка и публикация образа

```bash
docker buildx build --platform linux/amd64,linux/arm64 -t ksushkaap/mispisit-lab1:0.0.1 --push .
```
