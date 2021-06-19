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

1. В папку _t2s/tts/audio/backend/_ распакуйте [архив data](https://drive.google.com/file/d/1BmC1c6B4jJJ92b3kupahOujLwtoxkW3p/view?usp=sharing)
2. Проверьте, что путь до распакованных моделей совпадает с путями прописанными в файле _t2s/tts/saved_models.yaml_ 


### Install with Docker
 

    docker-compose build
    docker-compose up -d
    docker-compose exec postgres createdb -U postgres ratingdb
    docker-compose exec gateway vendor/bin/phinx migrate -e development
