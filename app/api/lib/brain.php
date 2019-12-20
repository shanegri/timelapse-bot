<?php

class Brain {

    // Returns pid or 0
    public static function getPid () 
    {
        $pid = intval (file_get_contents("/home/pi/hyperlapse/app/api/pid"));
        $running = $pid != 0
            ? intval (exec ("ps $pid | wc -l")) - 1 != 0
            : false;
        return $running ? $pid : 0;
    }

    public static function start ($args = "")
    {
        if (static::getPid()) static::stop();
        $pid = intval (exec ("nohup python /home/pi/hyperlapse/brain.py $args > /home/pi/hyperlapse/app/api/log 2>&1 & echo $!"));
        $pid_file = fopen ("/home/pi/hyperlapse/app/api/pid", "w");
        fwrite ($pid_file, $pid);
        fclose ($pid_file);
        return true;
    }

    public static function stop ()
    {
        $pid = static::getPid ();
        if (!$pid) return true;
        exec ("kill $pid");
        $pid_file = fopen ("/home/pi/hyperlapse/app/api/pid", "w");
        fwrite ($pid_file, "0");
        fclose ($pid_file);
        return true;
    }

    public static function status ()
    {
        $pid = static::getPid ();
        if (!$pid) return false;
        return exec ("tail /home/pi/hyperlapse/app/api/log -n 1");
    }

    // Return args from running hyperlapse if active
    public static function getArgs ()
    {
        $pid = static::getPid ();
        if (!$pid) return false;
        $p = exec ("ps ax | grep brain | head -n 1");
        $split = explode (" ", $p);
        return $split;
    }


}


?>