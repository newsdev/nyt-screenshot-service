#!/bin/bash

umount -l /dev/shm
umount -l /tmp

mount -t tmpfs -o size=1280m tmpfs /dev/shm
mount -t tmpfs -o size=768m tmpfs /tmp
