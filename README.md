Исследование в области синтеза речи
===================

Структура проекта
-------------------

      consumer/             слушатель очереди RabbitMQ
      frontend/             веб-интерфейс решения и балансировщик
      gateway_tts/          сервер обработки запросов
      t2s/                  API модуль синтеза речи (можно запускать отдельно)

Установка
------------

### Install with Docker
 

    docker-compose build
    docker-compose up -d
    docker-compose exec postgres createdb -U postgres ratingdb
    docker-compose exec gateway vendor/bin/phinx migrate -e development
