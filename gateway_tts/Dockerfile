FROM php:7.4-cli
RUN docker-php-ext-install sockets && apt-get update \
    && apt-get install -y libevent-dev libcurl4-openssl-dev pkg-config libssl-dev libonig-dev libpq-dev curl zip unzip \
    && pecl install event \
    && docker-php-ext-enable event \
    && docker-php-ext-install mbstring pcntl
RUN docker-php-ext-install pgsql pdo_pgsql
RUN docker-php-ext-configure pgsql -with-pgsql=/usr/local/pgsql && docker-php-ext-configure pdo_pgsql
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer
COPY . /var/www
WORKDIR /var/www
RUN composer install
CMD php ./src/app.php stop
CMD php ./src/app.php start