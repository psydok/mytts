<?php

namespace app\models;

use JsonSerializable;
use ValueError;

class ResponseTTSEntity implements JsonSerializable
{
    private $requests_id;
    private $filename;
    private $speed;
    private $len_text;
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
        return $this->requests_id;
    }

    /**
     * @param mixed $requests_id
     */
    public function setRequestsId($requests_id)
    {
        $this->requests_id = $requests_id;
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
        return $this->len_text;
    }

    /**
     * @param mixed $len_text
     */
    public function setLenText($len_text)
    {
        $this->len_text = $len_text;
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
            'len_text' => $this->len_text,
            'speed' => $this->speed,
            'filename' => $this->filename,
            'requests_id' => $this->requests_id
        ];
    }
}