###########################################################################
# Copyright 2008-2019 Rogue Wave Software, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you
# may not use this file except in compliance with the License. You may
# obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing
# permissions and limitations under the License.
###########################################################################
from pyimsl.util.imslUtils import STAT, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from pyimsl.util.VersionFacade import VersionFacade
from numpy import double, dtype, int, shape
from ctypes import POINTER, c_double, c_int, c_void_p

IMSLS_LAGS = 40513
imslstat = loadimsl(STAT)


def timeSeriesClassFilter(nLags, nClasses, iClass, x, lags=None):
    """ Converts time series data sorted within nominal classes in decreasing chronological order to a useful format for processing by a neural network.
    """
    VersionFacade.checkVersion(6)
    imslstat.imsls_d_time_series_class_filter.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_time_series_class_filter('
    evalstring += 'c_int(nObs)'
    evalstring += ','
    evalstring += 'c_int(nLags)'
    evalstring += ','
    evalstring += 'c_int(nClasses)'
    evalstring += ','
    iClass = toNumpyArray(iClass, 'iClass', shape=shape,
                          dtype='int', expectedShape=(0))
    evalstring += 'iClass.ctypes.data_as(c_void_p)'
    nObs = shape[0]
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(nObs))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    if not (lags is None):
        evalstring += ','
        evalstring += repr(IMSLS_LAGS)
        evalstring += ','
        lags = toNumpyArray(lags, 'lags', shape=shape,
                            dtype='int', expectedShape=(nLags))
        evalstring += 'lag.ctypes.data_as(c_void_p)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    return processRet(result, shape=(nObs, nLags), result=True)
