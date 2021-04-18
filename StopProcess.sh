. ../EnvirVars.sh

PID=`./IsBotRunning.sh`

echo $PID

if [ -z "$PID" ]
then
        echo 'Process Not Runnning'
else
        echo terminating $PID
	kill -9 $PID
fi





