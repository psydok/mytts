<?php

namespace app\repositories;

use PDO;
use PDOException;

require_once __DIR__ . '/../../vendor/autoload.php';

class RatingRepository extends Database
{
    public function __construct()
    {
        parent::__construct();
    }

    public function addRequest($models_id, $text)
    {
        $stat = "INSERT INTO requests(models_id, text) VALUES(?,?)";
        $db = $this->getConnection();
        try {
            if (!$query = $db->prepare($stat)) {
                echo 'prepare: insert request ' . var_export($db->errorInfo(), true);
                return -1;
            }
            if (!$query->execute([$models_id, $text])) {
                echo 'execute: insert request' . var_export($db->errorInfo(), true);
                return -1;
            }
            $requests_id = $db->lastInsertId();
            var_dump($requests_id);
            return $requests_id;
        } catch (PDOException $e) {
            $db->rollback();
            echo "error -> start rollback: " . $e->getMessage() . "\n";
        }
        return -1;
    }

    private function getContent($stat)
    {
        $query = $this->getConnection()->query($stat);
        if (!$query)
            return false;
        $arr = $query->fetchAll(PDO::FETCH_ASSOC);
        if (!$arr)
            return false;
        return $arr;
    }

    public function getModels()
    {
        return $this->getContent("SELECT * FROM models;");
    }

    public function getRating()
    {
        return $this->getContent("SELECT * FROM rating r INNER JOIN models m ON r.models_id=m.id;");
    }
}