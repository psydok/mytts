<?php

return
    [
        'paths' => [
            'migrations' => '%%PHINX_CONFIG_DIR%%/db/migrations',
            'seeds' => '%%PHINX_CONFIG_DIR%%/db/seeds'
        ],
        'environments' => [
            'default_migration_table' => 'phinxlog',
            'default_environment' => 'development',
            'production' => [
                'adapter' => 'pgsql',
                'host' => getenv('POSTGRES_HOST'),
                'name' => getenv('POSTGRES_DB'),
                'user' => getenv('POSTGRES_USER'),
                'pass' => getenv('POSTGRES_PASSWORD'),
                'port' => getenv('POSTGRES_PORT'),
                'charset' => 'utf8',
            ],
            'development' => [
                'adapter' => 'pgsql',
                'host' => getenv('POSTGRES_HOST'),
                'name' => getenv('POSTGRES_DB'),
                'user' => getenv('POSTGRES_USER'),
                'pass' => getenv('POSTGRES_PASSWORD'),
                'port' => getenv('POSTGRES_PORT'),
                'charset' => 'utf8',
            ],
            'testing' => [
                'adapter' => 'mysql',
                'host' => 'localhost',
                'name' => 'testing_db',
                'user' => 'root',
                'pass' => '',
                'port' => '3306',
                'charset' => 'utf8',
            ]
        ],
        'version_order' => 'creation'
    ];