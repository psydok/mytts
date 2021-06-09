<?php
namespace app\models;

class RateEntity
{
    private $model;
    private $avg_rate;
    private $avg_speed;
    private $count_rate;
    private $avg_len_text;

    public function __construct()
    {
    }

    /**
     * @return mixed
     */
    public function getModel()
    {
        return $this->model;
    }

    /**
     * @param mixed $model
     */
    public function setModel(ModelEntity $model)
    {
        $this->model = $model;
    }

    /**
     * @return mixed
     */
    public function getAvgRate()
    {
        return $this->avg_rate;
    }

    /**
     * @param mixed $avg_rate
     */
    public function setAvgRate($avg_rate)
    {
        $this->avg_rate = $avg_rate;
    }

    /**
     * @return mixed
     */
    public function getAvgSpeed()
    {
        return $this->avg_speed;
    }

    /**
     * @param mixed $avg_speed
     */
    public function setAvgSpeed($avg_speed)
    {
        $this->avg_speed = $avg_speed;
    }

    /**
     * @return mixed
     */
    public function getCountRate()
    {
        return $this->count_rate;
    }

    /**
     * @param mixed $count_rate
     */
    public function setCountRate($count_rate)
    {
        $this->count_rate = $count_rate;
    }

    /**
     * @return mixed
     */
    public function getAvgLenText()
    {
        return $this->avg_len_text;
    }

    /**
     * @param mixed $avg_len_text
     */
    public function setAvgLenText($avg_len_text)
    {
        $this->avg_len_text = $avg_len_text;
    }


}