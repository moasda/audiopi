#!/bin/bash
##################################################################################
# Provides: AudioPI (by CSC)
# Required-Start: $syslog
# Required-Stop: $syslog
# Description: This script starts/stops all necessary programs to launch AudioPI.
##################################################################################
 
case "$1" in
    start)
        echo "mocp server is starting"
        #start mocp as server
        mocp -S
        ;;
    stop)
        echo "mocp server is ending"
        # Ending mocp server
        mocp -x
        ;;
    *)
        echo "Use: /etc/init.d/audiopi {start|stop}"
        exit 1
        ;;
esac
 
exit 0
