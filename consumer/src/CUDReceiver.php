<?php

namespace consumers;

use consumers\repositories\RatingRepository;
use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Exception\AMQPTimeoutException;
require_once __DIR__ . '/repositories/RatingRepository.php';

class CUDReceiver
{
    public function listen()
    {
        try {
            $queue = $_ENV['RABBIT_QUEUE'];
            $connection = new AMQPStreamConnection(
                $_ENV['RABBIT_HOST'],
                $_ENV['RABBIT_PORT'],
                $_ENV['RABBIT_USER'],
                $_ENV['RABBIT_PASSWORD']
            );

            $repository = new RatingRepository();
        } catch (\Exception $e) {
            echo $e->getMessage();
            die;
        }
        $channel = $connection->channel();

        $channel->queue_declare(
            $queue,
            false,
            true, # чтобы не потерять сообщения
            false,
            false);

        $callback = function ($json) use ($repository) {
            echo "\n", '[x] Received ', $json->body, "\n";
            $object = json_decode($json->body, true);
            if (empty($object)) {
                echo "[x] !!!THIS IS NOT JSON ON RECEIVER!!! ";
                $json->delivery_info['channel']->basic_cancel('');
                return;
            }
            var_dump($object);
            switch ($object['method']) {
                case 'POST':
                    if ($object['table'] == 'responses') {
                        $repository->addResponse(
                            $object['filename'],
                            $object['speed'],
                            $object['len_text'],
                            $object['requests_id']);
                    }
                    break;
                case 'PUT':
                    if ($object['table'] == 'responses') {
                        $repository->updateResponse($object['filename'], $object['rate']);
                    }
                    break;
                default:
                    break;
            }

            $json->delivery_info['channel']->basic_ack($json->delivery_info['delivery_tag']);
        };
        $channel->basic_consume(
            $queue,
            '',
            false,
            false,
            false,
            false,
            $callback);

        while (count($channel->callbacks)) {
            try {
                $channel->wait();
            } catch
            (AMQPTimeoutException $exception) {
                echo $exception->getMessage();
            }
        }
        $channel->close();
        $connection->close();
    }
}