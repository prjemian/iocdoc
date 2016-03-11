'''
common routines for many modules
'''


import datetime
import logging
import sys

LOG_FILE = 'iocdoc.log'


def datenow():
    '''return date and time now as a string'''
    return str(datetime.datetime.now())


def logMessage(text):
    '''
    log a message
    '''
    global logging_started
    if not logging_started:
        logging.basicConfig(filename=LOG_FILE, filemode='w', level=logging.INFO)
        #logging.basicConfig(level=logging.INFO)
        logging_started = True
    logging.info(' ' + datenow() + ' ' + str(text))
    print text
    sys.stdout.flush()


class FileRef(object):
    '''records filename and linumber of an object'''
    
    def __init__(self, filename, linenumber, obj):
        self.filename = filename
        self.line_number = linenumber
        self.object = obj
