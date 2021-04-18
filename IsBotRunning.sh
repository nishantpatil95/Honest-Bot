. ../EnvirVars.sh

output=`ps aux|grep "[p]ython3 $BIN_DIR/main.py"`
#echo $output
set -- $output
echo $2


