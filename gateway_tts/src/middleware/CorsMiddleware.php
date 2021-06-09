<?php

namespace app\middleware;

use Psr\Http\Server\MiddlewareInterface;

class CorsMiddleware implements MiddlewareInterface
{

    public function process(\Psr\Http\Message\ServerRequestInterface $request, \Psr\Http\Server\RequestHandlerInterface $handler): \Psr\Http\Message\ResponseInterface
    {
        $response = $handler->handle($request);

        $response = $response
            ->withHeader('Origin', ['*'])
            ->withHeader('Access-Control-Allow-Origin', ['*'])
            ->withHeader('Access-Control-Allow-Headers', ['*'])
            ->withHeader('Access-Control-Expose-Headers', ['*'])
            ->withHeader('Access-Control-Allow-Methods', ['POST, PUT, OPTIONS, GET']);

        return $response;
    }
}