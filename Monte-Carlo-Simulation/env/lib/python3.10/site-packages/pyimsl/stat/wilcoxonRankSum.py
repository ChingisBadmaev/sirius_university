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
from pyimsl.util.imslUtils import STAT, checkForList, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, shape
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSLS_FUZZ = 11870
IMSLS_STAT = 14770
imslstat = loadimsl(STAT)


def wilcoxonRankSum(x1, x2, fuzz=None, stat=None):
    """ Performs a Wilcoxon rank sum test.
    """
    imslstat.imsls_d_wilcoxon_rank_sum.restype = c_double
    shape = []
    evalstring = 'imslstat.imsls_d_wilcoxon_rank_sum('
    evalstring += 'c_int(n1Observations)'
    evalstring += ','
    x1 = toNumpyArray(x1, 'x1', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'x1.ctypes.data_as(c_void_p)'
    n1Observations = shape[0]
    evalstring += ','
    evalstring += 'c_int(n2Observations)'
    evalstring += ','
    x2 = toNumpyArray(x2, 'x2', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'x2.ctypes.data_as(c_void_p)'
    n2Observations = shape[0]
    if not (fuzz is None):
        evalstring += ','
        evalstring += repr(IMSLS_FUZZ)
        evalstring += ','
        evalstring += 'c_double(fuzz)'
    if not (stat is None):
        evalstring += ','
        evalstring += repr(IMSLS_STAT)
        checkForList(stat, 'stat')
        evalstring += ','
        stat_stat_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(stat_stat_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (stat is None):
        processRet(stat_stat_tmp, shape=(10), pyvar=stat)
    return result
