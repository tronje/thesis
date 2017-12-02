#!/bin/bash

if [ $(hostname) = "duchess" ]; then
    tar czf /home/tronje/storage/backups/thesis-$(date +"%y-%m-%d-%H%M").tar.gz .
fi
