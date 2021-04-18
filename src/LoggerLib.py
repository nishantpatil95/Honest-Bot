import logging
import logging.handlers as handlers
import time
import os 
import sys 


logger = logging.getLogger('HonestBot')
logger.setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s %(filename)s %(lineno)d %(levelname)s::%(message)s')


logfile=os.getenv('LOGS_DIR')
if logfile==None:
    sys.exit('Log file not found')
logfile=logfile+"/HonestBot.log"

logHandler = handlers.RotatingFileHandler(logfile, maxBytes=500000, backupCount=2)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

logger.info('info test')
logger.debug('debug test')
logger.warning('warning test')
logger.critical('critical test')
logger.error('error test')

def getlogger():
    global logger
    return logger


