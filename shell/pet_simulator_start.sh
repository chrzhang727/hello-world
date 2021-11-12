#!/bin/bash
set -e

host_log_dir=$1
if [ ! -n $host_log_dir ]
then
  host_log_dir="`pwd`"
fi

simulator_image="gnbsimu:latest"
container_label="test=pet"
container_start_id=1
container_end_id=5
container_interval=10  #模拟器启动间隔

omc_sbi_url="http://10.252.0.48:8107/"
local_ip="10.252.0.82"
gnb_start_id=1
gnb_parallel_num=1000   #每个容器启动的gnb个数，总共启动gnb=gnb_parallel_num*(container_end_id-container_start_id)
gnb_start_interval=0.5  #每个gnb间启动间隔
alarm_interval=70       #alarm发送间隔,其它文件发送间隔由OMC设置

echo ">>>>>> Remove the container labeled with $container_label..."
docker rm -f $(docker ps -aq -f label=$container_label) || echo "No container was removed!"

#Remove simulator logs
find $host_log_dir -name '*simulator*' |xargs rm -f

for i in $(seq $container_start_id $container_end_id)
do
  log_path="$host_log_dir/log_$i"
  mkdir -p $log_path

  container_name="simulator_$i"
  port=`expr $i + 8000`
  gnb_end_id=`expr $gnb_start_id + $gnb_parallel_num - 1`



  echo ">>>>>> Start container $container_name at `date`"
  docker run -d -v $log_path:/home/gnb_simu/log -p $port:$port --name $container_name -l $container_label --privileged=true $simulator_image python gnb_batch_simulator.py --gnb.id.start $gnb_start_id --gnb.id.end $gnb_end_id --omc.sbi.url $omc_sbi_url -p $port --ip $local_ip --gnb.interval $gnb_start_interval --alarm.interval $alarm_interval

  #Check if the container is running
  state=`docker inspect --format '{{.State.Running}}' $container_name`
  if [ $state != "true" ]
  then
    echo ">>>>>> Failed to start $container_name!"
    break
  fi
  gnb_start_id=`expr $gnb_start_id + $gnb_parallel_num`

  # Start next batch after the previous finish
  while true
  do
    boot_num=`find ${log_path} -name 'simulator.log*' |xargs grep -E 'start to send ...0 BOOTSTRAP' |wc -l;`
    if [ $boot_num -ne $gnb_parallel_num ]
    then
      sleep 5
    else
      break
    fi
  done
  sleep $container_interval
done
