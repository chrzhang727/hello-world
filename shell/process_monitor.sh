#!/bin/bash

interval=5
log_dir='./monitor_log'

mkdir -p $log_dir

# system cpu, io, memory
nohup vmstat  -t -n 3 > $log_dir/0_sys_overview 2>&1 &
nohup iostat -xdkt  3 > $log_dir/0_disk_io 2>&1 &


proc_names=(
      "/usr/bin/mongod"
      "/usr/sbin/mysqld"
)
d_pid=`docker inspect -f '{{.State.Pid}}'  omc18`
i=1
for proc in "${proc_names[@]}"
do
  pid=`ps -ef |grep $proc |grep -v grep | grep -v ${d_pid}| awk '{print $2}'`

  if [ $pid ]
  then
    nohup pidstat -ruh -p $pid $interval > $log_dir/${i}_${proc##*/}${pid}_stat 2>&1 &
  else
    echo "Failed to get pid of $proc"
  fi
  i=`expr $i + 1`
done

while true
do
  uptime >> $log_dir/0_sys_load
  sleep $interval
done



