. ../EnvirVars.sh


PID=`./IsBotRunning.sh`


echo $PID

if [ -z "$PID" ]
then
	echo 'Not Runnnig'
else
	echo $PID
fi


