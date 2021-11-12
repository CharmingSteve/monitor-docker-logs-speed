#!/usr/bin/env python3
import re
import sys
import subprocess
import shlex
from decimal import Decimal
import numpy as np
import docker 


# opens stream docker logs
def invoke_process_popen_poll_live(command, shellType=True, stdoutType=subprocess.PIPE):
    """runs subprocess with Popen/poll so that live stdout is shown"""
    try:
        process = subprocess.Popen(
            shlex.split(command), shell=shellType, stdout=stdoutType)
    except:
        print("ERROR {} while running {}".format(sys.exc_info()[1], command))
        return None
    while True:
        output = process.stdout.readline()
        if process.poll() is not None:
            break
        if output:
            client = docker.from_env()
            #print(output.strip().decode())
            stripped = (output.strip().decode())
            print("stripped number is:", stripped)
            print("type of stripped is:", type(stripped))
            
            speed = str(output.strip().decode())
            #define speeds for later, any speed without "m s" but only "s" at the end is too fast
            tooHigh = re.findall(r"\s\s+s\b", speed)
            #no traffic
            nothing = re.findall(r"0.00\s\s+s\b", speed)
            #speeds with "m s" are slower where the border between 10 visits lies 
            low = []
            high = []

            #this parses the numbers with "m s" , some have decimals
            #this regex is where I got stuck, 
            m = re.findall(r"(\d.*)m", speed)
            print("m is:", (m))
            nom = [y.replace('m', '') for y in m]
            #remove the "m" from the end of the number
            print("nom is:", nom)
            #change the number that is in a "list" to a floating number with  decimals
            list_of_floats = []
            for item in nom:
                list_of_floats.append(float(item))
                print("list_of_floats is:", list_of_floats)
                #deal with numbers that started off with "m s", 130 is around when 10 visits will have occurred 
                for item in list_of_floats:
                    print("type of item is:", type(item))
                    print("item", item)
                    maxrate = 135.0
                    if item < maxrate:
                        #print(item, "is toohlow")
                        low.append(item)
                for item in list_of_floats:
                    if item > maxrate:
                        #print(item, "is toohigh")
                        high.append(item)
            if nothing:
                print("nothing", stripped)
                continue 
            elif low:
                print("lownumber", item)
                continue
            elif high:
                print("high number", item)
            elif tooHigh:
                print("too high number", stripped)
            else:
                continue 

            if  high or tooHigh: 
                print("tooHigh Too busy, re-starting Docker")
                for container in client.containers.list():
                    container.restart()

            #if high:
            #    print("tooHigh", "Too busy, re-starting Docker")
            #    for container in client.containers.list():
            #        container.restart()


    rc = process.poll()
    return rc


def main(argv):
    while True:
        cmd = "./parse-docker-logs.sh"

        print("== invoke_process_popen_poll_live  ==============")
        invoke_process_popen_poll_live(cmd)

if __name__ == '__main__':
    main(sys.argv)