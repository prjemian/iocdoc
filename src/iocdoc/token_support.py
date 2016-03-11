'''
Applies Python :mod:`tokenize` analysis to each line of a text file.
'''


import token
import tokenize
from utils import logMessage
import text_file


PRINT_DIAGNOSTICS = False


class TokenLog():
    '''
    Applies the Python <code>tokenize</code> analysis
    to each line of a file.  This allows a lexical analysis
    of the file, line-by-line.  This is powerful and makes
    some complex analyses more simple but it assumes the file
    resembles Python source code.

    :note The <code>tokenize</code> analysis is not robust.  
          Some files will cause exceptions for various reasons.

    :see http://docs.python.org/library/tokenize.html
    :see http://docs.python.org/library/token.html
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.tokenList = []
        self.xref = {}
        self.nameTable = token.tok_name
        self.nameTable[tokenize.COMMENT] = 'COMMENT'
        self.nameTable[tokenize.NL] = 'NEWLINE'
        self.token_pointer = None
        if PRINT_DIAGNOSTICS:
            print "\n".join( sorted(self.nameTable.values()) )

    def tokenName(self, tokType):
        '''
        convert token number to a useful string
        '''
        return self.nameTable[tokType]

    def tokenReceiver(self, tokType, tokStr, start, end, tokLine):
        '''
        called by tokenize package, logs tokens as they are called
        '''
        tokName = self.tokenName(tokType)
        tok_dict = {
            'tokName': tokName,
            'tokType': tokType,
            'tokStr': tokStr,
            'start': start,
            'end': end,
            'tokLine': tokLine,
        }
        self.tokenList.append( tok_dict )
        if not tokName in self.xref:
            self.xref[tokName] = []
        self.xref[tokName].append( len(self.tokenList)-1 )

    def getTokenList(self):
        '''
        :return: list of token dictionaries
        '''
        return self.tokenList

    def getCrossReferences(self):
        '''
        :return: dictionary of token cross-references
        '''
        return self.xref

    def report(self):
        '''
        prints (to stdout) results contained in tokenList list and xref dictionary
        '''
        print len(self.tokenList), "tokens were found"
        print len(self.xref), "different kinds of tokens were found"
        for k, v in self.xref.items():
            print k, len(v), "[",
            for index in v:
                report_dict = self.tokenList[index]
                print report_dict['start'][0],
            print "]"
        for k in ['OP', 'NAME', 'STRING']:
            if k in self.xref:
                for index in self.xref[k]:
                    report_dict = self.tokenList[index]
                    print k, report_dict['start'], "|" + report_dict['tokStr'].strip() + "|"

    def summary(self, alsoPrint = False):
        '''
        Summarizes the xref dictionary contents.
        Reports number of each different token name (type).

        :param alsoPrint: boolean to enable print to stdout
        :return: dictionary of token frequencies
        '''
        summary_dict = {k: len(v) for k, v in self.xref.items()}
        if alsoPrint:
            for k, v in sorted(summary_dict.items()):
                print "%s : %d" % (k, v)
        return summary_dict

    def processFile(self, filename):
        '''
        process just one file
        '''
        f = text_file.read(filename)    # use the file cache
        try:
            tokenize.tokenize(f.iterator().readline, self.tokenReceiver)
        except Exception, _exc:
            f.close()   # remember to close the file!
            msg = 'trouble with: ' + filename
            msg += '\n' + str(_exc)
            logMessage(msg)
            raise RuntimeError(msg)
        self.token_pointer = None
        f.close()

    def lineAnalysis(self):
        '''
        analyze the tokens by line

        :return dictionary with all the lines, including tokenized form
        '''
        # build a dictionary with all the lines, and a list of all the lines, in order
        lines = {'numbers':[]}
        longest = len(self.tokenList)
        lastProgress = None
        for tok in self.tokenList:
            lineNum = tok['start'][0]
            progress = lineNum*100/longest
            if progress != lastProgress:
                lastProgress = progress
                #if (progress % 5) == 0:
                #    print "%3d%%" % progress
            if not lineNum in lines['numbers']:
                # remember the order the line numbers came in
                lines['numbers'].append( lineNum )
                # each line number has a dictionary with:
                #   - (string) full text of the line from f.readline()
                #   - (string) token pattern
                #   - (list) tuple:  tokName, tokType, tokStr, start, end
                lines[lineNum] = {}
                lines[lineNum]['pattern'] = []
                lines[lineNum]['tokens'] = []
                lines[lineNum]['readline'] = tok['tokLine']
            # initially, pattern is a list of token names
            lines[lineNum]['pattern'].append( tok['tokName'] )
            item = { 'tokName': tok['tokName'], 
                     'tokType': tok['tokType'],
                     'tokStr': tok['tokStr'],
                     'start': tok['start'], 
                     'end': tok['end'] }
            lines[lineNum]['tokens'].append( item )
        # change pattern from list to string
        for line in lines['numbers']:
            pat = lines[line]['pattern']
            lines[line]['pattern'] = " ".join( pat )
        # don't retain this list locally, just return it to the caller
        return lines

    def setTokenPointer(self, position = None):
        '''
        set the token pointer to the given position
        
        :param position: index position within list of tokens
        :raise Exception: token pointer position errors
        '''
        if position != None:
            if position < 0:
                # allow easy Pythonic reference to the last indices
                position = len(self.tokenList) + position
            if position < 0:
                raise Exception, "position cannot be a negative number"
            if position >= len(self.tokenList):
                raise Exception, "position cannot be greater than or equal to number of tokens"
        self.token_pointer = position
    
    def getCurrentToken(self):
        return self.tokenList[self.token_pointer]

    #def __iter__(self):
    #    '''
    #    this class satisfies Python's iterator interface
    #    http://docs.python.org/reference/datamodel.html
    #    http://docs.python.org/library/stdtypes.html#typeiter
    #    '''
        
    def next(self):
        '''
        return the next element or raise a StopIteration exception 
        upon reaching the end of the sequence

        :return: token object
        :raise StopIteration: reached the end of the sequence
        '''
        if self.token_pointer == len(self.tokenList) - 1:
            raise StopIteration
        if self.token_pointer == None:
            self.token_pointer = -1
        self.token_pointer += 1
        return self.tokenList[self.token_pointer]
        
    def nextActionable(self, skip_list=None):
        '''
        walk through the tokens and find the next actionable token
        
        :param (str) skip_list: list of tokens to ignore 
           
           default list: ('COMMENT', 'NEWLINE', 'ENDMARKER', 
            'ERRORTOKEN', 'INDENT', 'DEDENT')

        :return: token object or None if no more tokens
        '''
        # TODO: can this become an iterator?
        if skip_list is None:
            skip_these_tokens = ('COMMENT', 'NEWLINE', 'ENDMARKER', 
                                 'ERRORTOKEN', 'INDENT', 'DEDENT')
        else:
            skip_these_tokens = skip_list
        found = False
        while not found:
            try:
                token = self.next()
            except StopIteration:
                return None
            if token['tokName'] not in skip_these_tokens:
                found = True
        return token

    def old_next(self, ptr = -1):
        '''
        walk through the tokens and find the next actionable token

        :param ptr: current buffer pointer, integer [0 .. len(self.tokenList)-1]
        :return: tuple (ptr, self.tokenList[ptr]), where ptr points to an actionable token or (None, None)
        '''
        skip_these_tokens = ('COMMENT', 'NEWLINE', 'ENDMARKER', 
                             'ERRORTOKEN', 'INDENT', 'DEDENT')
        ptr += 1
        while ptr < len(self.tokenList):
            tkn = self.tokenList[ptr]
            if tkn['tokName'] not in skip_these_tokens:
                return ptr, tkn
            ptr += 1
        return None, None

    def print_token(self, tkn):
        '''developer use'''
        print '%3d,%3d' % tkn['start'], 
        print '%10s' % tkn['tokName'], 
        print '|%15s|' % tkn['tokStr'].strip(), 
        print '|%s|' % tkn['tokLine'].strip()


def token_key(tkn):
    '''developer use, short string identifying the type and text of this token'''
    if tkn is None:
        m = ''
    else:
        m = tkn['tokName'] + ' ' + tkn['tokStr']
    return m


def getFullWord(tokenLog):
    '''
    parse the token stream for a contiguous word and return it as str
    
    Some words in template files might not be enclosed in quotes
    and thus the whole word is broken into several tokens.
    This command rebuilds the word, without stripping quotes (if provided).
    '''
    tok = tokenLog.getCurrentToken()
    end = tok['start'][1]
    v = ''
    while tok is not None:
        if tok['start'][1] == end:
            v += tok['tokStr']
            end = tok['end'][1]
        else:
            break
        tok = tokenLog.nextActionable()
    if v.endswith('{'):     # moved from template.py
        # watch for patterns such as this: "../../33iddApp/Db/filterDrive.db"{
        while tok['tokStr'] != '{':
            # walk the pointer back
            tokenLog.setTokenPointer(tokenLog.token_pointer-1)
            tok = tokenLog.getCurrentToken()
        v = v[:-1]
    return v


######################################################################


def main():
    filename = 'TokenLog.py'
    obj = TokenLog()
    obj.processFile(filename)
    obj.summary(True)
    analysis = obj.lineAnalysis()
    for number in analysis['numbers']:
        pattern = analysis[number]['pattern']
        print number
        if pattern not in ('NEWLINE', 'ENDMARK', 'COMMENT NEWLINE', ):
            print number, pattern, analysis[number]['readline'].strip()
    for _i in range(5):
        print str(obj.nextActionable())
    obj.setTokenPointer(-10)
    tok = obj.nextActionable()
    while tok != None:
        print str(tok)
        tok = obj.nextActionable()


if __name__ == '__main__':
    main()
