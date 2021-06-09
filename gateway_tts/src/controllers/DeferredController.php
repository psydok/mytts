<?php
declare(strict_types=1);

namespace app\controllers;

use app\models\RequestTTSEntity;
use app\models\ResponseTTSEntity;
use app\services\SenderRabbit;
use Comet\Request;
use Comet\Response;

require_once __DIR__ . '/../../vendor/autoload.php';

class DeferredController
{
    /**
     * PUT rating - добавить оценку модели в Response
     * @param Request $request
     * @param Response $response
     * @param $args
     */
    public function evaluateModel(Request $request, Response $response, $args)
    {
        //filename, rate
        $data = $request->getParsedBody();
        $responseEntity = new ResponseTTSEntity(
            $data['filename']
        );
        $responseEntity->setRate($data['rate']);
        $responseEntity->setMethod('PUT');
        $sender = new SenderRabbit();
        $sender->execute((string)json_encode($responseEntity));
        return $response->withStatus(200);
    }
}