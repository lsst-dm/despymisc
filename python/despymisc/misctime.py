# $Id$
# $Rev::                                  $:  # Revision of last commit.
# $LastChangedBy::                        $:  # Author of last commit.
# $LastChangedDate::                      $:  # Date of last commit.

""" Miscellaneous date/time utilities """

import pytz
import datetime
from dateutil.parser import parse

######################################################################
def convert_utc_str_to_nite(datestr):
    """ Convert an UTC date string to a nite string """

    # e.g. datestr: 2014-08-15T17:31:02.416533+00:00
    nite = None

    # convert date string to datetime object
    utc_dt = parse(datestr)

    # convert utc to local on mountain
    local_tz = pytz.timezone('Chile/Continental') # use your local timezone name here
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    local_dt = local_tz.normalize(local_dt) # .normalize might be unnecessary

    # see if before or after noon on mountain
    noon_dt = local_dt.replace(hour=12, minute=0, second=0, microsecond=0)
    if local_dt < noon_dt:  # if before noon, observing nite has previous date
        obsdate = (local_dt - datetime.timedelta(days=1)).date()
    else:
        obsdate = local_dt.date()

    nite = obsdate.strftime('%Y%m%d')
    return nite

if __name__ == '__main__':
    pass
