#!/usr/bin/env bash
display $1.jpg &
pcl_viewer $1.pcd -ps 5 &
