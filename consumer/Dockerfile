FROM php:7.4-cli
RUN docker-php-ext-install sockets && apt-get update \
    && apt-get install -y libcurl4-openssl-dev pkg-config libonig-dev libssl-dev libpq-dev curl zip unzip \
    && docker-php-ext-install mbstring pcntl
RUN docker-php-ext-install pgsql pdo_pgsql
RUN docker-php-ext-configure pgsql -with-pgsql=/usr/local/pgsql && docker-php-ext-configure pdo_pgsql
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer
COPY . /usr/src/consumer
WORKDIR /usr/src/consumer
RUN composer install
CMD ["php", "./src/receive.php"]