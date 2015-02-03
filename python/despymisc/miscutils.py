#!/usr/bin/env python
# $Id$
# $Rev::                                  $:  # Revision of last commit.
# $LastChangedBy::                        $:  # Author of last commit.
# $LastChangedDate::                      $:  # Date of last commit.

import re
import os
import sys
import datetime
import inspect
import errno

""" Miscellaneous support functions for framework """

#######################################################################
def fwdebug(msglvl, envdbgvar, msgstr):
    """ print debugging message based upon thresholds """
    # environment debug variable overrides code set level
    if envdbgvar in os.environ:
        dbglvl = os.environ[envdbgvar]
    elif '_' in envdbgvar:
        prefix = envdbgvar.split('_')[0]
        if '%s_DEBUG' % prefix in os.environ:
            dbglvl = os.environ['%s_DEBUG' % prefix]
        else:
            dbglvl = 0
    else:
        dbglvl = 0

    if int(dbglvl) >= int(msglvl): 
        print "%s - %s - %s" % (datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), inspect.stack()[1][3], msgstr)


#######################################################################
def fwdie(msg, exitcode, depth=1):
    """ abort after printing short message include some info from backtrace """
    frame = inspect.stack()[depth]
    file = os.path.basename(frame[1])
    print "\n\n%s:%s:%s: %s" % (file, frame[3], frame[2], msg) 
    
    sys.exit(exitcode)


#######################################################################
def fwsplit(fullstr, delim=','):
    """ Split by delim and trim substrs, expand #:# into range """
    fullstr = re.sub('[()]', '', fullstr) # delete parens if exist
    items = []
    for item in [x.strip() for x in fullstr.split(delim)]:
        m = re.match("(\d+):(\d+)", item)
        if m:
            items.extend(map(str, range(int(m.group(1)),
                                        int(m.group(2))+1)))
        else:
            items.append(item)
    return items


#######################################################################
def coremakedirs(thedir):
    """ Call os.makedirs handling path already exists """
    if len(thedir) > 0 and not os.path.exists(thedir):  # some parallel filesystems really don't like
                                                        # trying to make directory if it already exists
        try:
            os.makedirs(thedir)
        except OSError as exc:      # go ahead and check for race condition
            if exc.errno == errno.EEXIST:
                pass
            else:
                print "Error: problems making directory: %s" % exc
                raise


#######################################################################
CU_PARSE_PATH = 4
CU_PARSE_FILENAME = 2
CU_PARSE_EXTENSION = 1
def parse_fullname(fullname, retmask = 2):
    fwdebug(3, 'FWUTILS_DEBUG', "fullname = %s" % fullname)
    fwdebug(3, 'FWUTILS_DEBUG', "retmask = %s" % retmask)

    VALID_COMPRESS_EXT = ['fz']

    compress_ext = None
    filename = None
    path = None
    retval = []

    if retmask & CU_PARSE_PATH:
        #if '/' in fullname: # if given full path, canonicalize it
        #    fullname = os.path.realpath(fullname)
        path = os.path.dirname(fullname)
        if len(path) == 0:   # return None instead of empty string
            retval.append(None)
        else:
            retval.append(path)

    filename = os.path.basename(fullname)
    fwdebug(3, 'FWUTILS_DEBUG', "filename = %s" % filename)

    # check for compression extension on fits files
    m = re.search(r'^(\S+.fits)\.([^.]+)$', filename)
    if m:
        fwdebug(3, 'FWUTILS_DEBUG', "m.group(2)=%s" % m.group(2))
        fwdebug(3, 'FWUTILS_DEBUG', "VALID_COMPRESS_EXT=%s" % VALID_COMPRESS_EXT)
        if m.group(2) in VALID_COMPRESS_EXT:
            filename = m.group(1)
            compress_ext = '.'+m.group(2)
        else:
            if retmask & CU_PARSE_EXTENSION:
                print "Not valid compressions extension (%s)  Assuming non-compressed file." % m.group(2)
            compress_ext = None
    else:
        fwdebug(3, 'FWUTILS_DEBUG', "Didn't match pattern for fits file with compress extension")
        compress_ext = None

    if retmask & CU_PARSE_FILENAME:
        retval.append(filename)
    if retmask & CU_PARSE_EXTENSION:
        retval.append(compress_ext)

    if len(retval) == 0:
        retval = None
    elif len(retval) == 1:  # if only 1 entry in array, return as scalar
        retval = retval[0]

    return retval
    

#######################################################################
def convertBool(var):
    #print "Before:", var, type(var)
    newvar = None
    if var is not None:
        tvar = type(var)
        if tvar == int:
            newvar = bool(var)
        elif tvar == str:
            try:
                newvar = bool(int(var))
            except ValueError:
                if var.lower() in ['y','yes','true']:
                    newvar = True
                elif var.lower() in ['n','no','false']:
                    newvar = False
        elif tvar == bool:
            newvar = var
        else:
            raise Exception("Type not handled (var, type): %s, %s" % (var, type(var)))
    else:
        newvar = False
    #print "After:", newvar, type(newvar)
    #print "\n\n"
    return newvar


# For consistent testing of whether to use database or not
#    Function argument value overrides environment variable
#    Nothing set defaults to using DB
def use_db(arg):
    use = True

    args_use_db = None
    scalar_arg = None

    # handle cases where given arg is dict, argparse.Namespace
    if isinstance(arg, dict):
        if 'use_db' in arg:
            scalar_arg = arg['use_db']
    elif hasattr(arg, 'use_db'):
        scalar_arg = arg.use_db
    else:
        scalar_arg = arg

    if scalar_arg is not None:
        args_use_db = convertBool(scalar_arg)

    if args_use_db is not None:
        if not args_use_db:
            use = False
    elif 'DESDM_USE_DB' in os.environ and not convertBool(os.environ['DESDM_USE_DB']):
        use = False

    return use

# For consistent testing of boolean variables 
#    Example: whether to use database or not
#    Function argument value overrides environment variable
#    Lower case key for arg lookup, Upper case for environ lookup
def checkTrue(key, arg, default=True):
    ret_val = default

    args_val = None
    scalar_arg = None

    # handle cases where given arg is dict, argparse.Namespace
    if isinstance(arg, dict):
        if key.lower() in arg:
            scalar_arg = arg[key.lower()]
    elif hasattr(arg, key.lower()):
        scalar_arg = getattr(arg,key.lower())
    else:
        scalar_arg = arg

    if scalar_arg is not None:
        args_val = convertBool(scalar_arg)

    if args_val is not None:
        ret_val = args_val
    else:
        env_key = 'DESDM_%s' % key.upper()
        if env_key in os.environ and not convertBool(os.environ[env_key]):
            ret_val = False

    return ret_val


## PrettyPrinter doesn't work for certain nested dictionary (OrderedDict) cases
##     http://bugs.python.org/issue10592
def pretty_print_dict(the_dict, out_file=None, sortit=False, indent=4):
    """Outputs a given dictionary in a format easier for human reading where items within
       the same sub-dictionary could be output in alphabetical order"""
    if out_file is None:
        out_file = sys.stdout
    if the_dict is None:
        assert("Passed in None for dictionary arg")
    if not isinstance(the_dict, dict):
        assert("Passed in non-dictionary object for dictionary arg")
    _recurs_pretty_print_dict(the_dict, out_file, sortit, indent, 0)


def _recurs_pretty_print_dict(the_dict, out_file, sortit, inc_indent, curr_indent):
    """Internal recursive function to do actual WCL writing"""
    if len(the_dict) > 0:
        if sortit:
            dictitems = sorted(the_dict.items())
        else:
            dictitems = the_dict.items()

        for key, value in dictitems:
            if isinstance(value, dict):
                print >> out_file, ' ' * curr_indent + str(key) 
                _recurs_pretty_print_dict(value, out_file, sortit, inc_indent,
                                    curr_indent + inc_indent)
            else:
                print >> out_file, ' ' * curr_indent + str(key) + \
                        " = " + str(value)


def dynamically_load_class(class_desc):
    """ Loads class at runtime based upon given string description """

    fwdebug(3, 'COREMISC_DEBUG', "class_desc = %s" % class_desc)
    modparts = class_desc.split('.')
    fromname = '.'.join(modparts[0:-1])
    importname = modparts[-1]
    fwdebug(3, 'COREMISC_DEBUG', "\tfromname = %s" % fromname)
    fwdebug(3, 'COREMISC_DEBUG', "\timportname = %s" % importname)
    mod = __import__(fromname, fromlist=[importname])
    dynclass = getattr(mod, importname)
    return dynclass


#######################################################################
def get_list_directories(filelist):
    dirlist = {}
    for f in filelist:
        filedir = parse_fullname(f, CU_PARSE_PATH)
        relparents = filedir.split('/')
        thedir = ""
        for i in range(1,len(relparents)):
            thedir += '/' + relparents[i]
            dirlist[thedir] = True

    return sorted(dirlist.keys())



#########################################################################
# Some functions added by Felipe Menanteau, coming from the old despyutils

def elapsed_time(t1,verbose=False):
    """ Formating of the elapsed time """
    import time
    t2    = time.time()
    stime = "%dm %2.2fs" % ( int( (t2-t1)/60.), (t2-t1) - 60*int((t2-t1)/60.))
    if verbose:
        print "# Elapsed time: %s" % stime
    return stime

def query2dict_of_lists(query,dbhandle):

    """
    Transforms the result of an SQL query and a Database handle object [dhandle]
    into a dictionary of lists 
    """ 

    # Get the cursor from the DB handle
    cur = dbhandle.cursor()
    # Execute
    cur.execute(query)
    # Get them all at once
    list_of_tuples = cur.fetchall()
    # Get the description of the columns to make the dictionary
    desc = [d[0] for d in cur.description] 

    querydic = {} # We will populate this one
    cols = zip(*list_of_tuples)
    for k in range(len(cols)):
        key = desc[k]
        querydic[key] = cols[k]    

    return querydic 

