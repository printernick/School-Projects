<?php

  /* Given a SQL statement of all the games
  in the game table, create all the options available
  for purchase. The id parameter is the id to be
  selected by default */
  function createGameOptions($allGamesStmt, $id)
  {
    while ($row = $allGamesStmt->fetch())
    {
      if ($row->gid == $id)
      {
        echo '<option selected value=' .$row->gid .'>' .$row->name .'</option>';
      }
      else
      {
        echo '<option value=' .$row->gid .'>' .$row->name .'</option>';
      }
    }
  }
?>
