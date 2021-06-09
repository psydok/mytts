<?php

namespace app\models;

use ValueError;

/**
 * Класс синтезатора или вокодера
 */
class ModelEntity
{
    /** @var string Название модели */
    private $synthesizer;
    /** @var string Название модели */
    private $vocoder;

    public function __construct(string $synthesizer, string $vocoder='griffinlim'
    )
    {
        $this->synthesizer = self::checkIsNull($synthesizer);
        $this->vocoder = self::checkIsNull($vocoder);
    }

    private static function checkIsNull(string $value)
    {
        if (empty($value)) {
            throw new ValueError('Value cannot be empty', 1);
        } else return $value;
    }


    /**
     * @return string
     */
    public function getSynthesizer(): string
    {
        return $this->synthesizer;
    }

}