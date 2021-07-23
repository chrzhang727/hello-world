import sys
import getpass
import logging.config
from logging import Filter
if sys.version_info.major == 2:
    from  StringIO import StringIO
elif sys.version_info.major == 3:
    from io import StringIO


log_file = "/var/opt/oss/log/xxx.log" % getpass.getuser()

loggerConf = '''
[loggers]
keys=root, activity

[handlers]  
keys=consoleHandler, fileHandler

[formatters]  
keys=simpleFormatter, consoleFormatter

[logger_root]
level=INFO
handlers=consoleHandler
qualname=activity

[logger_activity]
level=DEBUG
handlers=fileHandler
qualname=activity

[handler_consoleHandler]
class=StreamHandler  
level=INFO
formatter=consoleFormatter  
args=(sys.stdout,) 

[handler_fileHandler]
class=logging.handlers.RotatingFileHandler 
formatter=simpleFormatter
args=('<log_file>','a',10486786,4,) # maximum size 11M

[formatter_simpleFormatter]
format=%(asctime)s | %(levelname)s | %(module)s |%(log_id)s%(message)s
datefmt=%Y-%m-%d-T%H:%M:%S %Z

[formatter_consoleFormatter]
format=%(levelname)s | %(message)s
'''.replace('<log_file>', log_file)




class LogFilter(Filter, object):
    def __init__(self, log_id):
        super(LogFilter, self).__init__()
        self.log_id = log_id

    def filter(self, record):
        record.log_id = self.log_id
        return True


logging.config.fileConfig(StringIO(loggerConf))
log = logging.getLogger('activity')
log.addFilter(LogFilter(''))
logging.getLogger('requests').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)

