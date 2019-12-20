<?php

require_once __DIR__ . "/lib/brain.php";
require_once __DIR__ . "/lib/lib.php";


$status = Brain::status ();

json_response ("Good", [
    "message" => $status,
    "active" => !!$status
]);


?>