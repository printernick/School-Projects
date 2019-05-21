<?php
  include_once "php/navBar.php";
  include_once "php/testinput.php";
  require_once "php/dbconnect.php";

  $conn = connect();

  //not necessary to run test_input on selected options
  $boardgameGid = $_POST ["boardgame"];
  $quantity = test_input($_POST ['quantity']);
  $firstName = test_input($_POST ["firstname"]);
  $lastName = test_input($_POST ["lastname"]);
  $phone = test_input($_POST["phone"]);
  $address = test_input($_POST["address"]);
  $city = test_input($_POST['city']);
  $state = test_input($_POST["state"]);
  $zip = test_input($_POST["zip"]);
  $delivery = $_POST["delivery"];
  $credit = test_input($_POST ["credit"]);

  $gameRow = $conn->query("SELECT name FROM games WHERE games.gid='{$boardgameGid}'")->fetch();

  $conn->exec("INSERT INTO orders (oid, gid, quantity, fname, lname, phone_num, address, city,
    state, zip, delivery, credit) VALUES (NULL, '{$boardgameGid}', '{$quantity}', '{$firstName}', '{$lastName}',
    '{$phone}', '{$address}', '{$city}', '{$state}', '{$zip}', '{$delivery}', '{$credit}')");


  makeNavBar(NULL);
?>

<html>
  <head>
    <title>Board No More Confirmation Page</title>
    <meta charset="UTF-8">
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <link rel="stylesheet" href="styles.css">

  </head>
  <h1>Board No More Confirmation Page</h1>

  <p>
    Thank you for shopping with Board No More!
    We have received your order and hope you find
    everything satisfactory.
    <br><br>
    You can find the details of your order below.

  </p>

</html>

<?php
  echo 'Board Game: ' . $gameRow->name . '<br>';
  echo 'Quantity: ' . $quantity . '<br>';
  echo 'First Name: ' . $firstName . '<br>';
  echo 'Last Name: ' . $lastName . '<br>';
  echo 'Phone Number: ' . $phone . '<br>';
  echo 'Address: ' . $address .'<br>';
  echo 'Zip: ' . $zip .'<br>';
  echo 'City: ' . $city .'<br>';
  echo 'State/Province/Region: ' . $state .'<br>';
  echo 'Delivery Option: ' . $delivery . '<br>';
  echo 'Credit Card Number: ' . $credit . '<br>';
?>
