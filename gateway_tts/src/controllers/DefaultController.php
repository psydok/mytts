<?php
declare(strict_types=1);

namespace app\controllers;

use app\models\RequestTTSEntity;
use app\models\ResponseTTSEntity;
use app\repositories\RatingRepository;
use app\services\SenderRabbit;
use Comet\Request;
use Comet\Response;
use Symfony\Component\Config\Definition\Exception\Exception;

require_once __DIR__ . '/../../vendor/autoload.php';

/**
 * Class DefaultController, где ответ необходим сразу
 * @package app\controllers
 */
class DefaultController
{
    /**
     * POST synth - получить аудиозапись
     * @param Request $request
     * @param Response $response
     * @param $args
     */
    public function synth(Request $request, Response $response, $args)
    {
        $tts = getenv('TTS_SERVER');
        if (!$this->isSiteAvailible($tts)) {
            return $this->newResponse($response,
                [
                    "status_code" => 503,
                    "message" => "sorry, server is not available"
                ], 503);
        }
        $requests_id = -1;
        $data = $request->getParsedBody();
        try {
            $requestEntity = new RequestTTSEntity(
                $data['model'],
                $data['text']
            );
            $requestEntity->setMethod('POST');
            $repository = new RatingRepository();
            $requests_id = $repository->addRequest(
                $requestEntity->getModelsId(),
                $requestEntity->getText());
        } catch (Exception $e) {
            var_dump('error save request: ' . $e);
        }

        $newResp = $this->sendOnServer($tts, $request);
//        var_dump('response: ' . $newResp . "\n");
        $result = json_decode($newResp);
        try {
            if ($result->status_code >= 400) {
                return $this->newResponse($response, $newResp);
            }
            $responseEntity = new ResponseTTSEntity(
                $result->filename
            );
            $responseEntity->setMethod('POST');
            $responseEntity->setLenText($result->len_text);
            $responseEntity->setSpeed($result->speed);
            if ($requests_id != -1)
                $responseEntity->setRequestsId($requests_id);
            $sender = new SenderRabbit();
            $sender->execute((string)json_encode($responseEntity));
        } catch (Exception $e) {
            var_dump('error save response: ' . $e);
        }
        return $this->newResponse($response, $result);
    }

    public function getMedia(Request $request, Response $response, $args)
    {
        $tts = getenv('TTS_SERVER');
        if (!$this->isSiteAvailible($tts)) {
            return $this->newResponse($response,
                [
                    "status_code" => 503,
                    "message" => "sorry, server is not available"
                ], 503);
        }
        $newResp = $this->sendOnServer($tts, $request);
        return $newResp;
    }

    /**
     * GET rating - получить рейтинг моделей
     * @param Request $request
     * @param Response $response
     * @param $args
     */
    public function getRating(Request $request, Response $response, $args)
    {
        $repository = new RatingRepository();
        $result = $repository->getRating();
        return $this->newResponse($response, $result);
    }

    /**
     * GET models - получить рейтинг моделей
     * @param Request $request
     * @param Response $response
     * @param $args
     */
    public function getModels(Request $request, Response $response, $args)
    {
        $repository = new RatingRepository();
        $result = $repository->getModels();
        return $this->newResponse($response, $result);
    }

    private function newResponse($response, $bodyArr, $status_code = 200)
    {
        $newResponse = $response
            ->withHeader('Content-Type', 'application/json');
        $newResponse->getBody()->write(json_encode($bodyArr));
        return $newResponse->withStatus($status_code);
    }

    /**
     * Отправка запроса на сервер и получение ответа
     * @param $requestServer
     * @param $request
     * @return mixed
     */
    private function sendOnServer($requestServer, $request)
    {
        $response1 = $this->sendRequest(
            $requestServer,
            $request->getUri()->getPath(),
            $request->getMethod(),
            $request->getParsedBody()
        );
        return $response1;
    }

    /**
     * Формирование запроса на сервер
     * @param $server
     * @param $path
     * @param $method
     * @param $body
     * @param $header
     * @return bool|string
     */
    private function sendRequest($server, $path, $method, $body)
    {
        $newHeader = array(
            "Content-Type: application/json"
        );
        $curl = curl_init();
        curl_setopt_array($curl, array(
            CURLOPT_URL => $server . $path,
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_ENCODING => "",
            CURLOPT_MAXREDIRS => 10,
            CURLOPT_TIMEOUT => 0,
            CURLOPT_FOLLOWLOCATION => true,
            CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
            CURLOPT_CUSTOMREQUEST => $method,
            CURLOPT_POSTFIELDS => json_encode($body),
            CURLOPT_HTTPHEADER => $newHeader,
        ));
        $response = curl_exec($curl);
        curl_close($curl);
        return $response;
    }

    function isSiteAvailible($url)
    {
        // Проверка правильности URL
        if (!filter_var($url, FILTER_VALIDATE_URL)) {
            return false;
        }

        $curlInit = curl_init($url);
        curl_setopt($curlInit, CURLOPT_CONNECTTIMEOUT, 20);
        curl_setopt($curlInit, CURLOPT_HEADER, true);
        curl_setopt($curlInit, CURLOPT_NOBODY, true);
        curl_setopt($curlInit, CURLOPT_RETURNTRANSFER, true);
        $response = curl_exec($curlInit);
        curl_close($curlInit);

        return $response ? true : false;
    }
}