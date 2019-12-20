<?php

require_once __DIR__ . "/lib/brain.php";
require_once __DIR__ . "/lib/lib.php";


$status = Brain::stop ();

json_response ("Good");


?>