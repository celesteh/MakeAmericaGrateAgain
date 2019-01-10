#!/bin/bash

# get the system ready
# keep the screen lit brightly (on AC power)
xbacklight -set 100 || echo xbacklight not installed
gsettings set org.gnome.desktop.session idle-delay 0 || echo not on gnome
gsettings set org.gome.settings-daemon.plugins.power sleep-display-battery 0 || echo not on gnome
gsettings set org.gome.settings-daemon.plugins.power sleep-display-ac 30 || echo not on gnome

# hide the mouse
unclutter -idle 0.01 -root &


cd  /home/celesteh/Dropbox/debbie

while :
    do

        sleep 5

      
        python ./MakeAmerica.py


    done
