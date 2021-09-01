#!/bin/bash

exp_swap=0
while true
do

  stat=`vmstat -t |grep -v -E 'memory|free'`
  swap=`echo $stat | awk '{print $3}'`
  cpu=`echo $stat | awk '{print $13+$14}'`

  if [ $cpu -gt 85 ]
  then
          echo "############################## CPU: $cpu%"
          echo "vmstat: $stat"
          ps aux | grep -v USER | sort -rn -k3 | head
  fi

  if [ $swap -ge $exp_swap ]
  then
          echo "############################## Swap: $swap"
          echo "vmstat: $stat"
          pidstat -ruh |grep -vE '^$|ubuntu|CPU' |sort -rn -k 15|head -n 10
          exp_swap=$swap
  fi
  sleep 60
done
