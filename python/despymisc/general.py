"""
An attempt to organize and avoid repetition for the collection of
simple functions used in diferent modules.


F. Menanteau, July/October 2014
"""

#
# def createDBH(section,verbose=False):
#     """ Connects to DESDM DB using coreutils.desdbi """
#
#     import coreutils.desdbi
#
#     try:
#         desdmfile = os.environ["des_services"]
#     except KeyError:
#         desdmfile = None
#     if verbose: print "# Creating DB connection to: %s" % section
#     dbh = coreutils.desdbi.DesDbi(desdmfile,section)
#     return dbh


def elapsed_time(t1,verbose=False):
    """ Formating of the elapsed time """
    import time
    t2    = time.time()
    stime = "%dm %2.2fs" % ( int( (t2-t1)/60.), (t2-t1) - 60*int((t2-t1)/60.))
    if verbose:
        print "# Elapsed time: %s" % stime
    return stime

def query2dict_of_columns(query,dbhandle):

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
