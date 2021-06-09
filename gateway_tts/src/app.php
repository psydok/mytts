<?php
declare(strict_types=1);
require_once __DIR__ . '/../vendor/autoload.php';


use app\controllers\DefaultController;
use app\controllers\DeferredController;
use Comet\Comet;

$app = new Comet([
    'host' => '0.0.0.0',
    'port' => getenv('GATEWAY_PORT')
]);

$app->addBodyParsingMiddleware();
$app->add(\app\middleware\CorsMiddleware::class);
$app->addRoutingMiddleware();

$app->options('/{routes:.+}', function ($request, $response, $args) {
    return $response;
});

$app->get('/api/models', 'app\controllers\DefaultController:getModels');
$app->get('/api/rating', 'app\controllers\DefaultController:getRating');
$app->get('/static/wavs/{routes:.+}', 'app\controllers\DefaultController:getMedia');
$app->post('/synth', 'app\controllers\DefaultController:synth');

$app->put('/api/rating',
    'app\controllers\DeferredController:evaluateModel');

$app->run();
