"""
A collection of utilities to call subprocess from multiprocess in python.
F. Menanteau, NCSA, Dec 2014
"""

def work_subprocess(cmd):
        
    """ Dummy function to call in multiprocess with shell=True """
    return subprocess.call(cmd,shell=True) 

def work_subprocess_logging(tup):

    """
    Dummy function to call in multiprocess with shell=True and a
    logfile using a tuple as inputs
    """

    cmd,logfile = tup
    log = open(logfile,"w")
    print "# Will write to logfile: %s" % logfile
    return subprocess.call(cmd,shell=True ,stdout=log, stderr=log)
