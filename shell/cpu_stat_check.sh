#!/bin/bash
#
CPU_us=$(vmstat | awk '{print $13}' | sed -n '$p')
CPU_sy=$(vmstat | awk '{print $14}' | sed -n '$p')
CPU_id=$(vmstat | awk '{print $15}' | sed -n '$p')
CPU_wa=$(vmstat | awk '{print $16}' | sed -n '$p')
CPU_st=$(vmstat | awk '{print $17}' | sed -n '$p')

CPU1=`cat /proc/stat | grep 'cpu ' | awk '{print $2" "$3" "$4" "$5" "$6" "$7" "$8}'`
sleep 5
CPU2=`cat /proc/stat | grep 'cpu ' | awk '{print $2" "$3" "$4" "$5" "$6" "$7" "$8}'`
IDLE1=`echo $CPU1 | awk '{print $4}'`
IDLE2=`echo $CPU2 | awk '{print $4}'`
CPU1_TOTAL=`echo $CPU1 | awk '{print $1+$2+$3+$4+$5+$6+$7}'`
CPU2_TOTAL=`echo $CPU2 | awk '{print $1+$2+$3+$4+$5+$6+$7}'`
IDLE=`echo "$IDLE2-$IDLE1" | bc`
CPU_TOTAL=`echo "$CPU2_TOTAL-$CPU1_TOTAL" | bc`
#echo -e "IDLE2:$IDLE2\nIDLE1:$IDLE1\nCPU2:$CPU2_TOTAL\nCPU1:$CPU1_TOTAL"
#echo -e        "IDLE:$IDLE\nCPU:$CPU_TOTAL"
RATE=`echo "scale=4;($CPU_TOTAL-$IDLE)/$CPU_TOTAL*100" | bc | awk '{printf "%.2f",$1}'`

echo -e "us=$CPU_us\tsy=$CPU_sy\tid=$CPU_id\twa=$CPU_wa\tst=$CPU_st"
echo "CPU_RATE:${RATE}%"
CPU_RATE=`echo $RATE | cut -d. -f1`
#echo   "CPU_RATE:$CPU_RATE"
if      [ $CPU_RATE -ge 80 ]
then    echo "CPU Warn"
        ps aux | grep -v USER | sort -rn -k3 | head
fi