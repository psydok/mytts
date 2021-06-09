<?php

namespace consumers\repositories;

use PDO;
use PDOException;

require_once __DIR__ . '/Database.php';

class RatingRepository extends Database
{
    public function __construct()
    {
        parent::__construct();
    }

    private function execute($statement, array $input_parameters, $msgError = null)
    {
        $db = $this->getConnection();
        try {
            if (!$query = $db->prepare($statement)) {
                echo 'prepare: ' . $msgError . '. ' . var_export($db->errorInfo(), true);
                return false;
            }

            if (!$query->execute($input_parameters)) {
                echo 'execute: ' . $msgError . '. ' . var_export($input_parameters, true);
                return false;
            }
            return $query;
        } catch (PDOException $e) {
            $db->rollback();
        }
        return false;
    }

    public function addModel($name, $vocoder)
    {
        $stat = "INSERT INTO models(generator, vocoder) VALUES(?,?)";
        $this->execute($stat, [$name, $vocoder], 'insert models');
    }

    private function getContent($stat)
    {
        $query = $this->getConnection()->query($stat);
        if (!$query)
            return false;
        $arr = $query->fetch(PDO::FETCH_ASSOC);
        if (!$arr)
            return false;
        return $arr;
    }

    public function getRequestsByModelId($models_id)
    {
        $stat = "SELECT generator FROM models;";
        $result = $this->getContent($stat);
        return $result;
    }

    private function getModelIdByFilename($filename)
    {
        $models_id = $this->execute(
            "SELECT rq.models_id FROM requests rq INNER JOIN responses rs ON rs.requests_id=rq.id WHERE rs.filename=?;",
            [$filename], 'get models_id by filename'
        );
        return $models_id->fetch(PDO::FETCH_ASSOC)['models_id'];
    }

    public function addResponse($filename, $speed, $len_text, $requests_id)
    {
        $stat = "INSERT INTO responses(filename, speed, len_text, requests_id) VALUES(?, ?,?,?);";
        $this->execute($stat, [$filename, $speed, $len_text, $requests_id],
            'insert response');
        //рейтинг
        $models_id = $this->getModelIdByFilename($filename);
        $this->updateRating($models_id);
    }

    public function updateResponse($filename, $rate)
    {
        $stat = "UPDATE responses SET rate=? WHERE filename=?;";
        $this->execute($stat, [$rate, $filename], 'update response');
        //рейтинг
        $models_id = $this->getModelIdByFilename($filename);
        $this->updateRating((int)$models_id, true);
    }

    public function updateRating(int $models_id, $flagRate=false)
    {
        $result_avg = $this->execute(
            "SELECT AVG(rate) AS avg_rate, AVG(speed) AS avg_speed, AVG(len_text) AS avg_len_text, COUNT(rate) AS count_rate FROM responses rs INNER JOIN requests rq ON rs.requests_id=rq.id WHERE rq.models_id=?;",
            [$models_id],
            'calc avg response by model');
        $arrResult = $result_avg->fetch(PDO::FETCH_ASSOC);
        $stat = "UPDATE rating SET avg_speed=?, avg_len_text=?";
        $stat_rate = ", count_rate=?, avg_rate=?";
        $stat_where = " WHERE models_id=?;";

        $avg_rate = $arrResult['avg_rate'];
        if ($flagRate && !is_null($avg_rate)) {
            $query = $this->execute($stat . $stat_rate . $stat_where, [
                $arrResult['avg_speed'],
                $arrResult['avg_len_text'],
                $arrResult['count_rate'],
                $arrResult['avg_rate'],
                $models_id],
                'update rating');
        } else {
            $query = $this->execute($stat . $stat_where, [
                $arrResult['avg_speed'],
                $arrResult['avg_len_text'],
                $models_id],
                'update rating');
        }
    }
}