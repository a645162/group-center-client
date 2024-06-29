#!/bin/bash

for username in $(ls /home); do
    if [ "$username" != "root" ]; then
        sudo cp -a /etc/skel/. /home/"$username"/
    fi
done
