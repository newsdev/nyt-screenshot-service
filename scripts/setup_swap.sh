#!/bin/bash

sudo umount -l /dev/shm
sudo umount -l /tmp

sudo mount -t tmpfs -o size=1280m tmpfs /dev/shm
sudo mount -t tmpfs -o size=768m tmpfs /tmp
