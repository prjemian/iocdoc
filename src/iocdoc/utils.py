'''
common routines for many modules

============================= ====================================================
support                       description
============================= ====================================================
:func:`chdir`                 change current IOC shell directory
:func:`datenow`               current date/time, as a str
:func:`detailedExceptionLog`  log the details of an exception
:class:`FileRef`              associate filename and line number of an object
:func:`logMessage`            log a message
:func:`strip_outer_pair`      remove outer symbols from text
:func:`strip_outer_quotes`    strip outer quotes (either single or double) from text
:func:`remove_c_comments`     strip out a C-style comment 
:const:`LOG_FILE`             default log file name (must be defined *before* logging is started)
:const:`LOGGING_DETAIL`       maximum level of detail to report in log (default=2, range: 0-5) 
:func:`strip_parentheses`     remove outer parentheses from text
:func:`strip_quotes`          strip outer double quotes from text
============================= ====================================================


..  rubric:: Values for :const:`LOGGING_DETAIL`

    When calling :func:`logMessage`, messages are assigned by the caller 
    (default value is 2) one of the following constants, describing
    the detail level of this message.  
    
    A message will be logged if it has an assigned level
    equal to or below :const:`LOGGING_DETAIL`.
    Except, of course if the level is :const:`LOGGING_DETAIL__NONE`.
    
    ===== =====================================
    value constant
    ===== =====================================
    -1    :const:`LOGGING_DETAIL__NONE`
    0     :const:`LOGGING_DETAIL__CERTAIN`
    1     :const:`LOGGING_DETAIL__IMPORTANT`
    2     :const:`LOGGING_DETAIL__MEDIUM`
    3     :const:`LOGGING_DETAIL__MINOR`
    4     :const:`LOGGING_DETAIL__NOISY`
    5     :const:`LOGGING_DETAIL__TRACEBACK`
    6     :const:`LOGGING_DETAIL__FULL_TRACEBACK`
    ===== =====================================

'''


import datetime
import logging
import os
import re
import sys


C_LANGUAGE_COMMENT_RE = r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"'
C_LANGUAGE_COMMENT_PATTERN = re.compile(
        C_LANGUAGE_COMMENT_RE,
        re.DOTALL | re.MULTILINE
    )

LOG_FILE = 'iocdoc.log'
logging_started = False
LOGGING_DETAIL__NONE = -1
LOGGING_DETAIL__CERTAIN = 0
LOGGING_DETAIL__IMPORTANT = 1
LOGGING_DETAIL__MEDIUM = 2
LOGGING_DETAIL__MINOR = 3
LOGGING_DETAIL__NOISY = 4
LOGGING_DETAIL__TRACEBACK = 5
LOGGING_DETAIL_LEVELS = (
    LOGGING_DETAIL__NONE,
    LOGGING_DETAIL__CERTAIN,
    LOGGING_DETAIL__IMPORTANT,
    LOGGING_DETAIL__MEDIUM,
    LOGGING_DETAIL__MINOR,
    LOGGING_DETAIL__NOISY,
    LOGGING_DETAIL__TRACEBACK,
)
LOGGING_DETAIL = LOGGING_DETAIL__MEDIUM


def chdir(newDir, nfsMounts={}):
    '''
    change the current working directory for the IOC shell

    :param newDir: name of new directory
    :return: success (True) or failure (False) 
    '''
    newDir = strip_quotes(newDir)
    if not os.path.exists(newDir):
        logMessage("cannot chdir(%s)" % newDir, LOGGING_DETAIL__CERTAIN)
        # FIXME: fails with chdir(''), , needs to know the default to be used
        # FIXME: fails with chdir('/xorApps/...'), need to check the nfsMount dictionary
        return False
    pwd = os.getcwd()
    if pwd != newDir:
        logMessage("leave: "+ pwd, LOGGING_DETAIL__NOISY)
        logMessage("enter: "+ newDir, LOGGING_DETAIL__MEDIUM)
    os.chdir(newDir)
    return True


def datenow():
    '''return date and time now as a string'''
    return str(datetime.datetime.now())


def detailedExceptionLog(title='', print_traceback=True):
    '''
    enter details of an exception to the log (developer tool)
    
    * always log that an exception was reported
    * the full traceback details are logged at a higher level
    '''
    import traceback
    if len(title) > 0:
        logMessage(title, LOGGING_DETAIL__CERTAIN)
    info = sys.exc_info()
    logMessage(str(info[0]), LOGGING_DETAIL__CERTAIN)
    logMessage(info[1], LOGGING_DETAIL__CERTAIN)
    if print_traceback:
        #traceback.print_exc()
        logMessage(traceback.format_exc(), LOGGING_DETAIL__TRACEBACK)


class FileRef(object):
    '''associate filename and line number of an object'''
    
    def __init__(self, filename, linenumber, colnumber, obj):
        self.filename = filename
        self.line_number = linenumber
        self.column_number = colnumber
        self.object = obj
    
    def __str__(self):
        # brief yet perhaps unambiguous
        fname = os.path.split(self.filename)[-1]
        return '(%s,%d,%d)' % (fname, self.line_number, self.column_number)


def setLogFile(logFile):
    '''
    define the log file name
    
    :param str logFile: name of log file to be used
    :raises RuntimeError: if called after logging has started
    '''
    global logging_started
    global LOG_FILE
    if logging_started:
        raise RuntimeError('Cannot change log file after logging has started. ' + LOG_FILE)
    LOG_FILE = logFile


def setLogDetailLevel(detail=2):
    '''
    define the logging (reporting) detail level
    
    :param int detail: interest level for logging items, must be <= LOGGING_DETAIL to be logged
    '''
    global LOGGING_DETAIL
    if detail not in LOGGING_DETAIL_LEVELS:
        msg = 'detail level must be one of these values: ' + str(LOGGING_DETAIL_LEVELS)
        raise ValueError(msg)
    LOGGING_DETAIL = detail


def logMessage(text, detail=2):
    '''
    log a message
    
    :param obj text: item to be logged, assumed to be a string but will be rendered with ``str(text)``
    :param int detail: interest level for this logging item, must be <= LOGGING_DETAIL to be logged
    '''
    global logging_started
    global LOGGING_DETAIL
    if detail == LOGGING_DETAIL__NONE:
        return
    if not logging_started:
        logging.basicConfig(filename=LOG_FILE, filemode='w', level=logging.INFO)
        #logging.basicConfig(level=logging.INFO)
        logging_started = True
    if detail <= LOGGING_DETAIL:
        logging.info(' ' + datenow() + ' ' + str(text))
        print text
        sys.stdout.flush()

def remove_c_comments(text):
    '''
    strip out a C-style comment
    
    ::
    
       /* such as this */
    
    :param str text: text with possible comment
    :see: http://stackoverflow.com/questions/241327/python-snippet-to-remove-c-and-c-comments
    '''
    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return ""
        else:
            return s
    return re.sub(C_LANGUAGE_COMMENT_PATTERN, replacer, text)


def strip_outer_pair(text, left, right = None):
    '''
    remove outer symbols from text

    :param text: string
    :param left: symbol on left side
    :param right: symbol on right side (default is left-side symbol)
    :return: modified string
    :raise Exception: left and right must have len(..) == 1
    '''
    if right == None:
        right = left
    if len(left) != 1:
        raise Exception, "left symbol must be a single character, given: %s"%left
    if len(right) != 1:
        raise Exception, "right symbol must be a single character, given: %s"%right
    txt = text.strip()
    # only strip if both are present
    if txt[0] == left and txt[-1] == right:
        txt = txt[1:-1]
    return txt


def strip_outer_quotes(text):
    '''
    strip outer quotes (either single or double) from text

    :return: text without comments
    '''
    s0 = text[0]
    result = text
    if s0 in ('"', "'"):
        result = strip_outer_pair(text, s0)
    return result


def strip_parentheses(text):
    '''
    remove outer parentheses from text

    :param text: string
    :return: modified string
    '''
    return strip_outer_pair(text, "(", ")")


def strip_quotes(text, quote='"'):
    '''
    strip outer double quotes from text

    :return: text without comments
    '''
    if len(text) > 0 and text[-1] == quote:
        text = text[:-1]
    if len(text) > 0 and text[0] == quote:
        text = text[1:]
    return text
