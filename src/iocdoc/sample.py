
'''
develop a better token stream parser for macro expressions

Cannot correctly handle this uncommon definition::

    $(abcd=$(a)$(b)$(c)$(d),a=A,b=B,c=C,d=D)

eventually, this will go into the "macros" module
'''

import os
from token_support import token_key, TokenLog


def parse_bracketed_macro_definitions(tokenLog):
    '''
    walk through a bracketed string, keeping track of delimiters
    
    verify we start on an opening delimiter
    '''
    analysis = _find_sections(tokenLog)

    token_dividers = [analysis['start'], analysis['end']]
    for key in 'commas equals'.split():
        token_dividers += analysis[key]
    token_dividers.sort()
    
    if len(analysis['commas']) == 0 and len(analysis['equals']) == 0:
        # No delimiters found: either no macro, 1 macro, or space-delimited.
        # Cannot become a dict since no "=" were found.
        # Look at all tokens between the enclosure, 
        # accumulate contiguous text,
        # break on non-contiguous boundaries
        # Note: makes no assumption about all on one line.
        s, f = token_dividers
        l, c = tokenLog.get(s)['end']
        text = ''
        parts = []
        for i in range(s+1, f):
            tok = tokenLog.get(i)
            if tok['start'][1] != c or tok['start'][0] != l:
                if len(text) > 0:
                    parts.append(text)
                text = tok['tokStr']
            else:
                text += tok['tokStr']
            l, c = tokenLog.get(i)['end']
        if len(text) > 0:
            parts.append(text)
        return parts

    text_list = []
    for index, key in enumerate(token_dividers[0:-1]):
        s = key+1
        f = token_dividers[index+1]
        text_list.append( _rebuild_text([tokenLog.get(_) for _ in range(s, f)]) )
    
    if len(analysis['commas']) > len(analysis['equals']):
        return text_list
    else:
        # tricky: http://stackoverflow.com/questions/6900955/python-convert-list-to-dictionary
        # if text_list = ['a', 'b', 'c', 'd']
        # this returns dict(a='b', c='d')
        return dict(zip(text_list[::2], text_list[1::2]))


def _find_sections(tokenLog):
    '''
    locate the tokens that divide this sequence into sections
    
    The overall section is delimited by {} or ().
    Internally, the delimiters are , or =.
    All the rest (that is not a comment) is string content to be kept.
    Return the sections as a a dictionary with these members:
    
    * 'open': token number for the opening symbol
    * 'commas': list of token numbers for comma delimiters
    * 'equals': list of token numbers for equal sign delimiters
    * 'close': token number for the matching closing symbol
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
        if tk == 'OP ,' and depth == 1:
            commas.append(tokenLog.token_pointer)
        elif tk == 'OP =' and depth == 1:
            equals.append(tokenLog.token_pointer)
        elif tk == tk_start:
            depth += 1
        elif tk == tk_end:
            depth -= 1
            if depth == 0:
                pt_end = tokenLog.token_pointer
        tok = tokenLog.nextActionable()
    
    return dict(
                start = pt_start,
                end = pt_end,
                commas = commas,
                equals = equals,
                )


def __print_token__(tok):
    '''developer use'''
    print '(%d,%d)-(%d,%d) %s: %s' % (
         tok['start'][0],
         tok['start'][1],
         tok['end'][0],
         tok['end'][1],
         tok['tokName'],
         tok['tokStr'],
     )


def __print_token_sequence__(token_list):
    '''developer use'''
    for tok in token_list:
        __print_token__(tok)


def _rebuild_text(token_list):
    '''
    reconstruct the text from the list of tokens
    '''
    text = ''
    for tok in token_list:
        # Q: What if tok['tokName'] is a COMMENT or other undesirable?
        # A: not common in macro definitions, fix code if this is seen
        # Q: what about line number or column number gaps between tokens?
        # A: addressed above, do not mix comma delimited and whitespace delimited
        text += tok['tokStr']
        # __print_token__(tok)
    return text


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def parse_macro_definition_block(tokenLog):
    '''demo purposes only'''
    tok = tokenLog.getCurrentToken()
    while token_key(tok) != 'NAME file':
        tok = tokenLog.nextActionable()
        if tok is None:
            return
    tok = tokenLog.nextActionable()   # filename
    tok = tokenLog.nextActionable()   # {
    tok = tokenLog.nextActionable()   # { | pattern

    definitions = []
    labels = []
    if token_key(tok) == 'NAME pattern':
        tok = tokenLog.nextActionable()     # {
        labels = parse_bracketed_macro_definitions(tokenLog)   # labels
        tok = tokenLog.getCurrentToken()
    while token_key(tok) != 'OP }':
        parts = parse_bracketed_macro_definitions(tokenLog)    # (labels): values
        if isinstance(parts, list):
            env = dict(zip(labels, parts))
        else:
            env = parts
        tok = tokenLog.getCurrentToken()
        definitions.append(env)
    return definitions


def main():
    testfile = os.path.join('.', 'testfiles', 'databases', 'scan.db')
    testfile = os.path.join('.', 'testfiles', 'templates', 'example.template')
    
    tokenLog = TokenLog()
    tokenLog.processFile(testfile)
    tok = tokenLog.nextActionable()

    while tok is not None and tok['tokName'] != 'ENDMARKER':
        defs = parse_macro_definition_block(tokenLog)
        if defs is None: break
        tok = tokenLog.getCurrentToken()
        for d in defs:
            print d

if __name__ == '__main__':
    main()
