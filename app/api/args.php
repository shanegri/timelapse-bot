<?php

require_once __DIR__ . "/lib/brain.php";
require_once __DIR__ . "/lib/lib.php";



json_response ("Good", [
    "args" => Brain::getArgs ()
]);


?>