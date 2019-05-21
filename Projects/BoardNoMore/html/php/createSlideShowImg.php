<?php
/* Given a SQL row for the images table,
create an img of class slideshow. */
function createSlideShowImg($row)
{
  echo
    "<img class='slideshow' src={$row->img}>";
}
?>
