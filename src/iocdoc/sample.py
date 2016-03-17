
'''
develop a better token stream parser for macro expressions
'''

import os
from token_support import token_key, TokenLog


def parse_bracketed(tokenLog):
    '''
    walk through a bracketed string, keeping track of delimiters
    
    verify we start on an opening delimiter
    '''
    terminator = {
                  '{': 'OP }',
                  '(': 'OP )',
                  }
    
    tok = tokenLog.getCurrentToken()
    c = tok['tokStr']
    if c not in terminator:
        l, c = tok['start']
        msg = '(%d,%d) ' % (l, c+1)
        msg += 'token stream not starting with "(" or "{"'
        raise KeyError, msg

    pt_start = tokenLog.token_pointer
    tk_start = token_key(tok)
    tk_end = terminator[c]
    depth = 1
    tok = tokenLog.nextActionable()
    commas = []
    equals = []
    while depth > 0:
        tk = token_key(tok)
        if tk == 'OP ,':
            commas.append(tokenLog.token_pointer)
        elif tk == 'OP =':
            equals.append(tokenLog.token_pointer)
        elif tk == tk_start:
            depth += 1
        elif tk == tk_end:
            depth -= 1
            if depth == 0:
                pt_end = tokenLog.token_pointer
        tok = tokenLog.nextActionable()
    print [tokenLog.get(_)['start'][1]+1 for _ in commas],
    print [tokenLog.get(_)['start'][1]+1 for _ in equals]
    # TODO:


def parse_definition_block(tokenLog):
    tok = tokenLog.getCurrentToken()
    while token_key(tok) != 'NAME file':
        tok = tokenLog.nextActionable()
        if tok is None:
            return
    tok = tokenLog.nextActionable()   # filename
    tok = tokenLog.nextActionable()   # {
    tok = tokenLog.nextActionable()   # { | pattern
    if token_key(tok) == 'NAME pattern':
        tok = tokenLog.nextActionable()     # {
        parse_bracketed(tokenLog)           # labels
        tok = tokenLog.getCurrentToken()
    while token_key(tok) != 'OP }':
        parse_bracketed(tokenLog)           # (labels): values
        tok = tokenLog.getCurrentToken()


def main():
    testfile = os.path.join('.', 'testfiles', 'databases', 'scan.db')
    testfile = os.path.join('.', 'testfiles', 'templates', 'example.template')
    
    tokenLog = TokenLog()
    tokenLog.processFile(testfile)
    tok = tokenLog.nextActionable()

    while tok is not None and tok['tokName'] != 'ENDMARKER':
        parse_definition_block(tokenLog)
        tok = tokenLog.getCurrentToken()

if __name__ == '__main__':
    main()
