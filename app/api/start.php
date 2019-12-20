<?php

require_once __DIR__ . "/lib/brain.php";
require_once __DIR__ . "/lib/lib.php";

function getBoundedAngle($name) {
    return max(min(intval ($_GET[$name]), 45), -45);
}

$start_pan = getBoundedAngle ("start_pan");
$start_tilt = getBoundedAngle ("start_tilt");

$end_pan = getBoundedAngle ("end_pan");
$end_tilt = getBoundedAngle ("end_tilt");

$length = intval($_GET["time"]) * 60;
$distance = intval($_GET["distance"]) * 10;
$direction = intval($_GET["direction"]);

$reversed = $_GET["reversed"] == "true" ? 1 : 0;

$args = "--start $start_pan $start_tilt $end_pan $end_tilt $length $distance $direction $reversed";

Brain::start ($args);


json_response ("Good", ["pid" => Brain::getPid (), "args" => $args])

?>
