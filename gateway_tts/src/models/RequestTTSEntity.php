<?php

namespace app\models;

use JsonSerializable;
use ValueError;

class RequestTTSEntity implements JsonSerializable
{
    private $modelsId;
    private $text;
    private $method;

//    private $created;

    public function __construct(int $model, string $text)
    {
        $this->modelsId = $model;
        $this->text = $text;
    }

    /**
     * @return string
     */
    public function getModelsId(): int
    {
        return $this->modelsId;
    }

    /**
     * @return string
     */
    public function getText(): string
    {
        return $this->text;
    }


    /**
     * @return mixed
     */
    public function getMethod()
    {
        return $this->method;
    }

    /**
     * @param mixed $method
     */
    public function setMethod($method)
    {
        $this->method = $method;
    }


    public function jsonSerialize()
    {
        return [
            'method' => $this->method,
            'table' => 'requests',
            'text' => $this->text,
            'models_id' => $this->modelsId
        ];
    }
}