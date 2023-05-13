# SDO python code check microservice
Этот репозиторий содержит исполняемый код микросервиса для системы дистанционного обучения (СДО)

Запустить сервер можно несколькими способами:
- напрямую через python
- docker-образ
- docker-compose
- start.sh

## Запуск через python

Требования: 
- python версии 3.10 и выше
- ОС linux (запуск на ОС windows возможен только с использованием docker)
- установленный пакет python-virtualenv

Запуск:
- склонировать репозиторий в любую удобную директорию
```git clone https://github.com/sidecuter/sdo-python.git```
- перейти в директорию склонированного репозитория
- создать виртуальное окружение
```python -m venv venv```
- активировать окружение
```source venv/bin/activate```
- установить зависимости
```python -m pip install -r requirements.txt```
- запустить сервер командой:
```DB_CON="строка подключения" uvicorn main:app --reload```

P.S. строка подключения зависит от используемой базы данных. Более подробно на [сайте](https://docs.sqlalchemy.org/en/20/core/engines.html#backend-specific-urls)

## Запуск через docker

Требования:
- установленный докер на целевом устройстве

Запуск:
- скачиваем docker-образ микросервиса
```docker pull ghcr.io/sidecuter/sdo-python:latest```
- запускаем контейнер со следующими аргументами
```docker run -it -p 8000:8000 -v trash:/var/server/trash -e DB_CON="строка соединения" ghcr.io/sidecuter/sdo-python:latest python -m uvicorn main:app --reload```
- Не забываем указывать переменную окружения DB_CON согласно инструкции с [сайта](https://docs.sqlalchemy.org/en/20/core/engines.html#backend-specific-urls)

## Запуск через docker-compose

Требования:
- docker с установленным docker-compose не ниже третьей версии

Запуск:
- клонируйте репозиторий на целевое устройство и перейдите в корневую директорию репозитория
- установите переменные окружения SDOP_DB_NAME, SDOP_DB_USER и SDOP_DB_PASS
Пояснения: SDOP_DB_NAME - имя создаваемой базы данных; SDOP_DB_USER - имя пользователя, используемое сервером для подключения к бд; SDOP_DB_PASS - пароль пользователя
- выполните сборку командой
```docker compose build```
- Запустите микросервис командой
```docker compose up```

## Запуск через скрипт start.sh

Требования:
- ОС linux
- docker с установленным docker-compose не ниже третьей версии
- наличие bash в дистрибутиве

Запуск:
- клонируйте репозиторий на целевое устройство и перейдите в корневую директорию репозитория
- откройте скрипт в любом текстовом редакторе и после символа = укажите необходимые данные
- дайте скрипту права на выполнение
```chmod +x start.sh```
- запустите скрипт
```./start.x```

# Credentials

## Main developer
[Alexender Svobodov](https://github.com/sidecuter)
