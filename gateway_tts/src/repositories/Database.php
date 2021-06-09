<?php

namespace app\repositories;

use PDO;
use PDOException;

require_once __DIR__ . '/../../vendor/autoload.php';

class Database
{
    private $dbConnection;

    public function __construct()
    {
        $db = require __DIR__ . '/db.php';
        try {
            $this->dbConnection = new PDO($db[0]);
        } catch (PDOException $exception) {
            echo "Connection error: " . $exception->getMessage();
            die;
        }
    }

    protected function getConnection()
    {
        return $this->dbConnection;
    }
}