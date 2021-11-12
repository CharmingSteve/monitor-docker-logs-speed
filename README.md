# monitor-docker-logs-speed
Monitor the speed that docker logs output, This can be used to see how many hits you are getting in realtime without paying for a subscritpion service

This script will restart your docker containers when you get more than 10 visits a minute it's based on counting the log entries as they are made with the pv bash tool . 

It takes the log from  docker logs -f proxy ,  you can edit as you like 

run "./liveoutput.py" or "python3 ./liveoutput"

to test it, run "watch  -n 6  curl localhost" use higher then 6 to run it more than 10 times a minutes and higher to run it less.

when I copied the scripts to a different dir it needed to be given exec, so if you see /bin/sh: 1: ./parse-docker-logs.sh: Permission denied

This uses the pv bash command to measure the speed of lines going through. pv is usually use to measure the speed of file transfer, often with a percentage bar accross the screen, but adding --line-mode sets it to measure line speed.

I tested this on my laptop, I am not sure if the number defined as maxrate line 57 inside the liveoutput.py script will  be perfectly correct on a another server. running curl faster than every 6 seconds will cause it to reatart all docker containers. I have found that exactly every 6 seconds sometimes does not cause docker restart, but the next minute it totally works. All should continue to function fine when curl is run every 7 seconds, or totally left without activity.

You can DDOS by running  "watch -n .1 curl localhost" in several windows
