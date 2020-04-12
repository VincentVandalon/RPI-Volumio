#!/bin/bash

# What display to use: 
DISPL="/usr/bin/bw_tool -I -D /dev/i2c-1 -a 00"
#DISPL="echo"
GETSONG="cat /var/log/syslog | grep librespot_playback::player | grep loaded | tail -n 1 | cut \-d \< \-f2\- | cut \-d \> \-f1"

#clean the display
$DISPL -W 10:0:b
L0=00
L1=20
L2=40
L3=34

while true; do
       #print the current time 
       $DISPL -W 11:$L0:b
       $DISPL -t '                  '
       JSONSTATE=$(cat /var/log/volumio.log | grep 'STATE SERVICE' | tail -n1 | cut -d' ' -f6- )
       JSONSTATE=$(wget -qO- http://localhost:3000/api/v1/getState)
       CURRENT_SAMPLE=$(echo "$JSONSTATE" | jq -r '.samplerate')
       CURRENT_SAMPLE=$(cat /proc/asound/card1/pcm0p/sub0/hw_params | grep "rate" | cut -d':' -f2 | cut -d' ' -f2)
       CURRENT_SAMPLE="$(( CURRENT_SAMPLE/ 1000 )) kHz"
       CURRENT_BITS=$(echo "$JSONSTATE" | jq -r '.bitdepth' | cut -d'i' -f-1) 
       CURRENT_SONG_LOGTEXT=$(echo "$JSONSTATE" | jq -r '.title') 
       [ -z "$CURRENT_SAMPLE" ] && CURRENT_SAMPLE=" no audio info"

               #CURRENT_SAMPLE=$(cat /proc/asound/card1/pcm0p/sub0/hw_params | grep "rate" | cut -d':' -f2 | cut -d' ' -f2)
               #CURRENT_SONG_LOGTEXT=$(tail /var/log/syslog | grep 'spotifyd' | grep 'loaded' | tail -n1 | cut -d \< -f2- | cut -d \> -f1)

       L1String="$(date +%H:%M) $CURRENT_SAMPLE $CURRENT_BITS"
       $DISPL -W 11:$L1:b
       $DISPL -t $(printf '%-20s' "$L1String")
       #The song that was last played
       $DISPL -W 11:$L2:b
       L3TEXT=$( echo "$CURRENT_SONG_LOGTEXT" | head -c20)
       $DISPL -t $(printf '%-20s' "$L3TEXT")

       $DISPL -W 11:$L3:b
       L4TEXT=$( echo "$CURRENT_SONG_LOGTEXT" | tail -c+21 | head -c19)
       $DISPL -t " $(printf '%-20s' "$L4TEXT")"

       sleep 2
done
