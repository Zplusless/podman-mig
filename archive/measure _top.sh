echo "%CPU_user,%CPU_sys,%MEM" > /tmp/csv_data/cpu_test.csv
pid=1    #Can be change by yourself
while true              
    do
        cpu_user=`top -b -n 1 | grep Cpu | awk '{print $2}' | cut -f 1 -d "%"`
        cpu_system=`top -b -n 1 | grep Cpu | awk '{print $4}' | cut -f 1 -d "%"`
        mem_sys_used=`free | grep Mem | awk '{print $3}'`
	time=`date +"%T.%6N"`
        echo $cpu_user,$cpu_system,$mem_sys_used,$time >> /tmp/csv_data/cpu_test.csv
        sleep 0.2    #delay time
done



