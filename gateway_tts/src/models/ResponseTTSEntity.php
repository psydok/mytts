<?php

namespace app\models;

use JsonSerializable;
use ValueError;

class ResponseTTSEntity implements JsonSerializable
{
    private $requestsId;
    private $filename;
    private $speed;
    private $lenText;
    private $rate;
    private $method;

    public function __construct(string $filename)
    {
        $this->filename = $filename;
    }

    /**
     * @return mixed
     */
    public function getRequestsId()
    {
        return $this->requestsId;
    }

    /**
     * @param mixed $requestsId
     */
    public function setRequestsId($requestsId)
    {
        $this->requestsId = $requestsId;
    }

    /**
     * @return mixed
     */
    public function getFilename()
    {
        return $this->filename;
    }

    /**
     * @param mixed $filename
     */
    public function setFilename($filename)
    {
        $this->filename = $filename;
    }

    /**
     * @return mixed
     */
    public function getSpeed()
    {
        return $this->speed;
    }

    /**
     * @param mixed $speed
     */
    public function setSpeed($speed)
    {
        $this->speed = $speed;
    }

    /**
     * @return mixed
     */
    public function getLenText()
    {
        return $this->lenText;
    }

    /**
     * @param mixed $lenText
     */
    public function setLenText($lenText)
    {
        $this->lenText = $lenText;
    }

    /**
     * @return mixed
     */
    public function getRate()
    {
        return $this->rate;
    }

    /**
     * @param mixed $rate
     */
    public function setRate($rate)
    {
        $this->rate = self::checkRate($rate);
    }

    private function checkRate($rate)
    {
        if ($rate < 0 or $rate > 5) {
            throw new ValueError('Rate must be [1, 5]');
        }
        return $rate;
    }

    public function setMethod(string $method)
    {
        $this->method = $method;
    }

    public function jsonSerialize()
    {
        return [
            'method' => $this->method,
            'table' => 'responses',
            'rate' => $this->rate,
            'len_text' => $this->lenText,
            'speed' => $this->speed,
            'filename' => $this->filename,
            'requests_id' => $this->requestsId
        ];
    }
}