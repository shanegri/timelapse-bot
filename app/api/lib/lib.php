<?php

function json_response ($status, $args = []) {
    header ('Content-Type: application/json');
    $response = [
        "status" => $status
    ] + $args;
    echo json_encode ($response);
    die();
}

?>