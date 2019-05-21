<?php
  /* Given a row from a SQL
  table and a connection to the Database
  create an HTML table entry. */
  function createTableEntry($row, $conn)
  {
    $imgRow = $conn->query("SELECT img FROM images
      WHERE images.gid = '$row->gid' ORDER BY images.imgId LIMIT 1")->fetch();

	//echo "<img src = $imgRow->img></img>";

    echo
      "<tr>"
          ."<td>"
            ."<a href=listing.php?id={$row->gid}>"
              .$row->name
            ."</a>"
            ."<td>$$row->price</td>"
            ."<td>" .$row->minP ."-" .$row->maxP ."</td>"
            ."<td>$row->play_time Min</td>"
            ."<td>$row->age+</td>"
            ."<td>"
                ."<a href=listing.php?id={$row->gid}>"
                    .'<img class="tableImage" src= ' . $imgRow->img
                        .' alt = ' . $row->name
                        .' OnMouseOver = "previewImage(this)"'
                        .' OnMouseOut = "revertImage(this)">'
                ."</a>"
            ."</td>"
          ."</td>"
      ."</tr>";
  }
?>
