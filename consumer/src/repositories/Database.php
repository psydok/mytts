<?php

namespace consumers\repositories;

use PDO;
use PDOException;

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