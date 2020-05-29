from os.path import join, dirname, abspath
import datetime


class Log:
    def __init__(self):
        self.logfile = join(dirname(dirname(abspath(__file__))), 'Logs/LogFile.txt')
        self.now = datetime.datetime.now()

    def error(self, e):
        with open(self.logfile, 'a') as log:
            log.write('\n' + str(self.now) + ' - ' + str(e))
