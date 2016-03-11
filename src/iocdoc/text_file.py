'''
text_file.py - describe any text file used by an EPICS IOC
'''


import os
import StringIO


class FileNotFound(Exception): pass


file_cache = None       # singleton instance of FileCache()


def read(filename):
    '''
    get a file either from the cache or from storage
    
    Always use complete filenames (no unexpanded macros), can be relative.
    This code will use absolute filenames internally.
    '''
    global file_cache
    if file_cache is None:
        _setup_file_cache()
    filename = os.path.abspath(filename)
    if not file_cache.exists(filename):
        file_cache.set(filename, _IocTextFile(filename))
    return file_cache.get(filename)


def items():
    '''get the cache as a set of dictionary items'''
    return file_cache.cache.items()


def keys():
    '''get the names of files in the cache'''
    return file_cache.cache.keys()


def values():
    '''get the Python objects of items in the cache'''
    return file_cache.cache.values()


# --- internal routines below --------------


def _setup_file_cache():
    '''define ``file_cache`` as a singleton'''
    global file_cache
    file_cache = _FileCache()


class _FileCache(object):
    '''load each file only once'''
    
    def __init__(self):
        global file_cache
        if file_cache is not None:
            msg = '_FileCache() called more than once'
            msg += ': use text_file.file_cache object instead'
            raise RuntimeError(msg)
        self.cache = {}
        file_cache = self
    
    def exists(self, filename):
        return filename in self.cache
    
    def set(self, filename, value):
        '''
        define a reference to a file in the cache
        '''
        self.cache[filename] = value
    
    def get(self, filename, alternative = None):
        '''
        get a reference to a file from the cache
        '''
        return self.cache.get(filename, alternative)


class _IocTextFile(object):
    '''
    superclass: description and common handling of a file used by an EPICS IOC
    
    This class should only be called by the read() method above.
    '''
    
    def __init__(self, filename):
        self.filename = filename
        if not os.path.exists(filename):
            raise FileNotFound(filename)

        self.absolute_filename = os.path.abspath(filename)
        self.absolute_directory = os.path.dirname(self.absolute_filename)
        stats = os.stat(self.absolute_filename)
        self.mtime = stats.st_mtime 
        self.bytes = stats.st_size 
        self.cwd = os.getcwd()

        self._read()
        self.number_of_lines = len(self)
    
    def close(self):
        '''some code likes to call this'''
        pass
    
    def iterator(self):
        '''iterator interface: provide str.readline for tokenizer'''
        return StringIO.StringIO(self.full_text)
    
    def __len__(self):
        '''iterator interface'''
        return len(self.full_text.splitlines())
    
    def _read(self):
        '''read the complete file from storage'''
        if not os.path.exists(self.absolute_filename):
            raise FileNotFound(self.absolute_filename)
        self.full_text = open(self.absolute_filename, 'r').read()
    
    def __str__(self):
        return self.filename
