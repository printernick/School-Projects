<?php

function connect(){
        include $_SERVER['DOCUMENT_ROOT'].'/../dbconfig.php';
        $hostname = DB_HOST;
        $username = DB_USER;
        $password = DB_PASSWORD;
        $dbname = DB_DATABASE;

        try{
                $conn = new PDO("mysql:host=$hostname;dbname=$dbname", $username, $password);
                // set the PDO error mode to exception
                $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
                $conn->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_OBJ);
                return $conn;
        }
        catch(PDOException $e) {
                echo "Connection failed: " . $e->getMessage();
        }
}
?>
