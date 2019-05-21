<!DOCTYPE html>

<?php
    include_once "php/dbconnect.php";
    include_once "php/dbCreateTableEntry.php";
    include_once "php/navBar.php";
    $conn = connect();

    $stmt = $conn->query("SELECT * FROM games");
?>

<html>
    <head>
        <title>Board Games | Board No More</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel ="stylesheet" href="styles.css">

      	<script type = "text/JavaScript" src = "javascripts/imagePreview.js"> </script>
    </head>
    <body>
        <?php makeNavBar(FALSE) ?>

        <div class="boardGameTable">
            <table>
                <tr>
                    <th>Name</th>
                    <th>Price</th>
                    <th>Players</th>
                    <th>Playing Time</th>
                    <th>Age</th>
                    <th>Image</th>
                </tr>
                <?php
                  while($row = $stmt->fetch())
                  {
                      createTableEntry($row, $conn);
                  }
                ?>
            </table>
        </div>

    </body>
</html>

<?php $conn = null; ?>
