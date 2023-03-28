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
IMSLS_ALPHA = 10070
IMSLS_STAT = 14770
IMSLS_SUM_RANK = 30015
IMSLS_DIFFERENCE = 11230
imslstat = loadimsl(STAT)


def friedmansTest(y, fuzz=None, alpha=None, stat=None, sumRank=None, difference=None):
    """ Performs Friedman's test for a randomized complete block design.
    """
    imslstat.imsls_d_friedmans_test.restype = c_double
    shape = []
    evalstring = 'imslstat.imsls_d_friedmans_test('
    evalstring += 'c_int(nBlocks)'
    evalstring += ','
    evalstring += 'c_int(nTreatments)'
    evalstring += ','
    y = toNumpyArray(y, 'y', shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'y.ctypes.data_as(c_void_p)'
    nBlocks = shape[0]
    nTreatments = shape[1]
    if not (fuzz is None):
        evalstring += ','
        evalstring += repr(IMSLS_FUZZ)
        evalstring += ','
        evalstring += 'c_double(fuzz)'
    if not (alpha is None):
        evalstring += ','
        evalstring += repr(IMSLS_ALPHA)
        evalstring += ','
        evalstring += 'c_double(alpha)'
    if not (stat is None):
        evalstring += ','
        evalstring += repr(IMSLS_STAT)
        checkForList(stat, 'stat')
        evalstring += ','
        stat_stat_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(stat_stat_tmp)'
    if not (sumRank is None):
        evalstring += ','
        evalstring += repr(IMSLS_SUM_RANK)
        checkForList(sumRank, 'sumRank')
        evalstring += ','
        sumRank_sumRanks_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(sumRank_sumRanks_tmp)'
    if not (difference is None):
        evalstring += ','
        evalstring += repr(IMSLS_DIFFERENCE)
        checkForList(difference, 'difference')
        evalstring += ','
        difference_difference_tmp = c_double()
        evalstring += 'byref(difference_difference_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (stat is None):
        processRet(stat_stat_tmp, shape=(6), pyvar=stat)
    if not (sumRank is None):
        processRet(sumRank_sumRanks_tmp, shape=(nTreatments), pyvar=sumRank)
    if not (difference is None):
        processRet(difference_difference_tmp, shape=1, pyvar=difference)
    return result
