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
from numpy import double, dtype, shape
from ctypes import POINTER, c_double, c_int, c_void_p

IMSLS_FUZZ = 11870
imslstat = loadimsl(STAT)


def tieStatistics(x, fuzz=None):
    """ Compute tie statistics for a sample of observations.
    """
    imslstat.imsls_d_tie_statistics.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_tie_statistics('
    evalstring += 'c_int(nObservations)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nObservations = shape[0]
    if not (fuzz is None):
        evalstring += ','
        evalstring += repr(IMSLS_FUZZ)
        evalstring += ','
        evalstring += 'c_double(fuzz)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    return processRet(result, shape=(4), result=True)
