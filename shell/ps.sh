cpu=`ps --no-heading --pid=$PID -o pcpu`
mem=`ps --no-heading --pid=$PID -o pmem`
echo -n `date +'%Y-%m-%d %H:%M:%S'`
echo "\t$cpu\t$mem"
