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
from numpy import double, dtype, shape
from ctypes import POINTER, c_double, c_int, c_void_p

imslstat = loadimsl(STAT)


def timeSeriesFilter(maxLag, x):
    """ Converts time series data to the format required for processing by a neural network.
    """
    VersionFacade.checkVersion(6)
    imslstat.imsls_d_time_series_filter.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_time_series_filter('
    evalstring += 'c_int(nObs)'
    evalstring += ','
    evalstring += 'c_int(nVar)'
    evalstring += ','
    evalstring += 'c_int(maxLag)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nObs = shape[0]
    nVar = shape[1]
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    return processRet(result, shape=((nObs - maxLag), (nVar * (maxLag + 1))), result=True)
