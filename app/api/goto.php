<?php

require_once __DIR__ . "/lib/brain.php";
require_once __DIR__ . "/lib/lib.php";

$pan = intval ($_GET["pan"]);
$tilt = intval ($_GET["tilt"]);

if ($pan > 45) $pan = 45;
if ($pan < -45) $pan = -45;

if ($tilt > 45) $tilt = 45;
if ($tilt < -45) $tilt = -45;

Brain::start ("-pt $pan $tilt");

json_response ("Good")

?>