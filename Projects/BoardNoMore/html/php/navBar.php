<?php

/* This function takes a boolean
value isHome. If true, it will bold
the home value. If false, it will
bold the Board Games value. If null,
it will bold neither */
function makeNavBar($isHome)
{
  if (isset($isHome))
  {
    if ($isHome)
    {
      echo
      '<div class="topnav">
          <a href="#index"><b>Home</b></a>
          <a href="boardGames.php">Board Games</a>
      </div>';
    }
    else
    {
      echo
      '<div class="topnav">
          <a href="index.php">Home</a>
          <a href="#boardGames"><b>Board Games</b></a>
      </div>';
    }
  }
  else
  {
    echo
    '<div class="topnav">
        <a href="index.php">Home</a>
        <a href="boardGames.php">Board Games</a>
    </div>';
  }

}
?>
