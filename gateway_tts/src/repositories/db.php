<?php

return [
    "pgsql:host=" . getenv('POSTGRES_HOST')
    . ";dbname=" . getenv('POSTGRES_DB')
    . ";user=" . getenv('POSTGRES_USER')
    . ";password=" . getenv('POSTGRES_PASSWORD')
];