. ../EnvirVars.sh
$PYTHON_EXE -m compileall $SRC_DIR 

cp $SRC_DIR/__pycache__/*.pyc $BIN_DIR

for file in $BIN_DIR/*.cpython-38.pyc
do
  mv "$file" "${file/.cpython-38.pyc/.pyc}"
done

PID=`./IsBotRunning.sh`


echo $PID

if [ -z "$PID" ]
then
	echo "Starting Process..."
	if [ -z "$1" ]
	then
		$PYTHON_EXE $BIN_DIR/main.pyc  
	else
		$PYTHON_EXE $BIN_DIR/main.pyc > $LOGS_DIR/HonestLogs.log  2>&1  & 
	fi
else
        echo 'Already Running'
fi





