docker-compose build
docker-compose up -d
docker-compose exec postgres pqsl -U admin ratingdb
docker-compose exec gateway vendor/bin/phinx migrate -e development

