#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Some utilities for operations

import os, sys
import ast, re
import logging
from ConfigParser import RawConfigParser

class LosotoParser(RawConfigParser):

    def __init__(self, parsetFile):
        RawConfigParser.__init__(self)

        # read parset and replace '#' with ';' to allow # as inline comments
        # also add [_global] fake section at beginning
        import StringIO
        config = StringIO.StringIO()
        config.write('[_global]\n'+open(parsetFile).read().replace('#',';'))
        config.seek(0, os.SEEK_SET)
        self.readfp(config)

    def getstr(self, s, v, default=None):
        if self.has_option(s, v):
            return self.parser.get(s, v).replace('\'','').replace('"','') # remove apex
        elif default is None:
            logging.error('Section: %s - Values: %s: required (expected string).' % (s, v))
        else:
            return default

    def getbool(self, s, v, default=None):
        if self.has_option(s, v):
            return self.parser.getboolean(s, v)
        elif default is None:
            logging.error('Section: %s - Values: %s: required (expected bool).' % (s, v))
        else:
            return default

    def getfloat(self, s, v, default=None):
        if self.has_option(s, v):
            return self.parser.getfloat(s, v)
        elif default is None:
            logging.error('Section: %s - Values: %s: required (expected float).' % (s, v))
        else:
            return default

    def getint(self, s, v, default=None):
        if self.has_option(s, v):
            return self.parser.getint(s, v)
        elif default is None:
            logging.error('Section: %s - Values: %s: required (expected int).' % (s, v))
        else:
            return default

    def getarray(self, s, v, default=None):
        if self.has_option(s, v):
            try:
                return list(ast.literal_eval( self.parser.get(s, v) ))
            except:
                logging.error('Error interpreting section: %s - values: %s (should be a list as [xxx,yyy,zzz...], strings shoudl have \'apex\')' % (s, v))
        elif default is None:
            logging.error('Section: %s - Values: %s: required.' % (s, v))
        else:
            return default

    def getarraystr(self, s, v, default=None):
        try:
            return [str(x) for x in self.getarray(s, v, default)]
        except:
            logging.error('Error interpreting section: %s - values: %s (expected array of str.)' % (s, v))

    def getarraybool(self, s, v, default=None):
        try:
            return [bool(x) for x in self.getarray(s, v, default)]
        except:
            logging.error('Error interpreting section: %s - values: %s (expected array of bool.)' % (s, v))

    def getarrayfloat(self, s, v, default=None):
        try:
            return [float(x) for x in self.getarray(s, v, default)]
        except:
            logging.error('Error interpreting section: %s - values: %s (expected array of float.)' % (s, v))

    def getarrayint(self, s, v, default=None):
        try:
            return [int(x) for x in self.getarray(s, v, default)]
        except:
            logging.error('Error interpreting section: %s - values: %s (expected array of int.)' % (s, v))


def getParAxis( parser, step, axisName ):
    """
    Parameters
    ----------
    parser : parser obj
        configuration file
    step : str
        this step
    axisName : str
        an axis name

    Returns
    -------
    str, dict or list
        a selection criteria
    """
    axisOpt = None
    if parser.has_option(step, axisName):
        axisOpt = parser.getstr(step, axisName)
        # if vector/dict, reread it
        if axisOpt != '' and (axisOpt[0] == '[' and axisOpt[-1] == ']') or (axisOpt[0] == '{' and axisOpt[-1] == '}'):
            axisOpt = ast.literal_eval( parser.getstr(step, axisName) )

    elif parser.has_option('_global', axisName):
        axisOpt = parser.getstr('_global', axisName)
        # if vector/dict, reread it
        if axisOpt != '' and (axisOpt[0] == '[' and axisOpt[-1] == ']') or (axisOpt[0] == '{' and axisOpt[-1] == '}'):
            axisOpt = ast.literal_eval( parser.getstr('_global', axisName) )

    if axisOpt == '' or axisOpt == []:
        axisOpt = None
 
    return axisOpt


def getStepSoltabs(parser, step, H):
    """
    Return a list of soltabs object for 

    Parameters
    ----------
    parser : parser obj
        configuration file
    step : str
        current step
    H : h5parm obj
        the h5parm object

    Returns
    -------
    list
        list of soltab obj with applied selection
    """
    cacheSteps = ['clip','flag', 'norm', 'residuals', 'smooth'] # steps to use chaced data

    # selection on soltabs
    if parser.has_option(step, 'soltab'):
        stsel = ast.literal_eval(parser.getstr(step, 'soltab'))
    elif parser.has_option('_global', 'soltab'):
        stsel = ast.literal_eval(parser.getstr('_global', 'soltab'))
    else:
        stsel = '*/*' # select all
    if not type(stsel) is list: stsel = [stsel]

    soltabs = []
    for solset in H.getSolsets():
        for soltabName in solset.getSoltabNames():
            if any(re.compile(this_stsel).match(solset.name+'/'+soltabName) for this_stsel in stsel):
                if step in cacheSteps:
                    soltabs.append( solset.getSoltab(soltabName, useCache=True) )
                else:
                    soltabs.append( solset.getSoltab(soltabName, useCache=False) )

    # axes selection
    for soltab in soltabs:
        userSel = {}
        for axisName in soltab.getAxesNames():
            userSel[axisName] = getParAxis( parser, step, axisName )
        soltab.setSelection(**userSel)

    return soltabs
