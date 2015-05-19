#!/usr/bin/env python
# $Id: special_metadata_funcs.py 38203 2015-05-17 14:28:09Z mgower $
# $Rev:: 38203                            $:  # Revision of last commit.
# $LastChangedBy:: mgower                 $:  # Author of last commit.
# $LastChangedDate:: 2015-05-17 09:28:09 #$:  # Date of last commit.

"""
Specialized functions for computing metadata
"""

import calendar
import re


VALID_BANDS = ['u','g','r','i','z','Y','VR']

######################################################################
def create_band(filter):
    """ Create band from filter """

    band = filter.split(' ')[0]
    if band not in intgdefs.VALID_BANDS:
        raise KeyError("filter yields invalid band")
    return band


######################################################################
def create_camsym(instrume):
    """ Create band from filter """

    return instrume[0]


######################################################################
def create_nite(date_obs):
    """ Create nite from DATE-OBS """

    # date_obs = 'YYYY-MM-DDTHH:MM:SS.S'
    v = date_obs.split(':')
    hh = int(v[0].split('-')[2][-2:])
    if hh > 14:
        nite = v[0][:-3].replace('-','')
    else:
        y = int(v[0][0:4])
        m = int(v[0][5:7])
        d = int(v[0][8:10])-1
        if d==0:
            m = m - 1
            if m==0:
                m = 12
                y = y - 1
            d = calendar.monthrange(y,m)[1]
        nite = str(y).zfill(4)+str(m).zfill(2)+str(d).zfill(2)

    return nite


######################################################################
def create_field(object):
    """ create the field from OBJECT """

    m = re.search(" hex (\S+)", object)
    if m:
        field = m.group(1)
    else:
        raise KeyError("Cannot parse OBJECT (%s) for 'field' value")

    return field
