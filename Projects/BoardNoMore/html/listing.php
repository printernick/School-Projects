<?php
  if(isset($_GET['id']))
  {
    require_once "php/dbconnect.php";
    include_once "php/navBar.php";
    include_once "php/createSlideShowImg.php";
    include_once "php/createOptions.php";

    $conn = connect();

    //should be one row because id should be unique
    $row = $conn->query("SELECT * FROM games WHERE gid={$_GET["id"]}")->fetch();

    makeNavBar(NULL);
  }
  else //redirect to board games page
  {
    header("Location: boardGames.php");
  }
?>

<html>
  <head>
    <title><?php echo $row->name ?> | Board No More</title>
    <meta charset="UTF-8">
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <link rel="stylesheet" href="styles.css">

    <script src="javascripts/slideshow.js"></script>
    <script type = "text/JavaScript" src = "javascripts/getPlace.js"> </script>
    <script type = "text/JavaScript" src = "javascripts/getTotal.js"> </script>
    <script src='lib/d3.js'></script>

  </head>
  <body>
    <div class=gridContainer>
      <div class="slideShowContainer">
        <?php
          //generate all imgs for slideshow
          $imgs = $conn->query("SELECT * FROM images WHERE gid={$row->gid}");
          while($imgRow = $imgs->fetch())
          {
            createSlideShowImg($imgRow);
          }
        ?>

        <button class = "back" OnClick="updateSlide(-1)">&#10094;</button>
        <button class = "next" OnClick="updateSlide(+1)">&#10095;</button>
      </div>

      <div class = "productInfoContainer">
        <h2>
          <?php echo $row->name ?>
        </h2>

        <table>
          <tr>
            <th>Price</th>
            <th>Players</th>
            <th>Playing Time</th>
            <th>Age</th>
          </tr>
          <tr>
            <td id="price">$<?php echo $row->price ?></td>
            <td><?php echo $row->minP .'-' .$row->maxP ?></td>
            <td><?php echo $row->play_time?> Min</td>
            <td><?php echo $row->age?>+</td>
          </tr>
        </table>

        <p>
          <?php echo $row->description ?>
        </p>
      </div>

      <div class = "formContainer">
        <b>Purchase Below</b>
        <br>

        <form name="purchaseForm" action="confirmation.php"
          method = "post">

          Board Game:
          <select name="boardgame">
            <?php
              $allGamesStmt = $conn->query("SELECT gid, name FROM games");
              createGameOptions($allGamesStmt, $row->gid);
            ?>

          </select>
          <br>

          Quantity:
          <input type="text" name="quantity" onblur="getTotal(this.value)" required/>
          <br>

          First Name:
          <input type="text" name="firstname" required/>
          <br>

          Last Name:
          <input type="text" name="lastname" required/>
          <br>

          Phone Number:
          <input type="tel" name="phone" pattern="[0-9]{3}-[0-9]{3}-[0-9]{4}"
            placeholder = "Format: 123-456-7890" required/>
          <br>

          Address:
          <input type="text" name="address" placeholder = "Street address" required/>
          <br>

          Zip:
          <input type="text" name="zip" pattern="[0-9]{5}"
            placeholder = "Format: 12345" onblur="getPlace(this.value)" required/>
          <br>

          City:
          <input type="text" name="city" required/>
          <br>

          State/Province/Region:
          <input type="text" name="state" required/>
          <br>

          Delivery Option:
          <select name="delivery">
            <option selected value="standard">$5.00 Standard Shipping</option>
            <option value="ground">$3.00 6-day Ground Shipping</option>
            <option value="expedited">$8.00 2-day Expedited Shipping</option>
            <option value="overnight">$12.00 Overnight Shipping</option>
          </select>
          <br>

          Credit Card Number:
          <input type="text" name="credit" pattern="[0-9]{4}-[0-9]{4}-[0-9]{4}"
            placeholder = "Format: 1234-5678-9012" required/>
          <br>

          <input type="submit" value="Purchase"/>
          <p><b>TOTAL:</b></p>
          <p id="total"></p>


        </form>
      </div>

    </div>

    <script>

        var slideIndex = 0;
        displaySlide(slideIndex);

    </script>

  </body>

</html>

<?php $conn = null; ?>
