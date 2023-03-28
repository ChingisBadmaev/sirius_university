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
from pyimsl.util.imslUtils import STAT, checkForList, fatalErrorCheck, loadimsl, processRet, toNumpyArray, checkForDict
from numpy import double, dtype, shape
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSLS_CHI_SQUARED = 10450
IMSLS_LRT = 12880
IMSLS_EXPECTED = 11550
IMSLS_CONTRIBUTIONS = 10470
IMSLS_CHI_SQUARED_STATS = 10490
IMSLS_STATISTICS = 14780
imslstat = loadimsl(STAT)


def contingencyTable(table, chiSquared=None, lrt=None, expected=None, contributions=None, chiSquaredStats=None, statistics=None):
    """ Performs a chi-squared analysis of a two-way contingency table.
    """
    imslstat.imsls_d_contingency_table.restype = c_double
    shape = []
    evalstring = 'imslstat.imsls_d_contingency_table('
    evalstring += 'c_int(nRows)'
    evalstring += ','
    evalstring += 'c_int(nColumns)'
    evalstring += ','
    table = toNumpyArray(table, 'table', shape=shape,
                         dtype='double', expectedShape=(0, 0))
    evalstring += 'table.ctypes.data_as(c_void_p)'
    nRows = shape[0]
    nColumns = shape[1]
    if not (chiSquared is None):
        evalstring += ','
        evalstring += repr(IMSLS_CHI_SQUARED)
        checkForDict(chiSquared, 'chiSquared', [])
        evalstring += ','
        chiSquared_df_tmp = c_int()
        evalstring += 'byref(chiSquared_df_tmp)'
        evalstring += ','
        chiSquared_chiSquared_tmp = c_double()
        evalstring += 'byref(chiSquared_chiSquared_tmp)'
        evalstring += ','
        chiSquared_pValue_tmp = c_double()
        evalstring += 'byref(chiSquared_pValue_tmp)'
    if not (lrt is None):
        evalstring += ','
        evalstring += repr(IMSLS_LRT)
        checkForDict(lrt, 'lrt', [])
        evalstring += ','
        lrt_df_tmp = c_int()
        evalstring += 'byref(lrt_df_tmp)'
        evalstring += ','
        lrt_gSquared_tmp = c_double()
        evalstring += 'byref(lrt_gSquared_tmp)'
        evalstring += ','
        lrt_pValue_tmp = c_double()
        evalstring += 'byref(lrt_pValue_tmp)'
    if not (expected is None):
        evalstring += ','
        evalstring += repr(IMSLS_EXPECTED)
        checkForList(expected, 'expected')
        evalstring += ','
        expected_expected_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(expected_expected_tmp)'
    if not (contributions is None):
        evalstring += ','
        evalstring += repr(IMSLS_CONTRIBUTIONS)
        checkForList(contributions, 'contributions')
        evalstring += ','
        contributions_chiSquaredContributions_tmp = POINTER(
            c_double)(c_double())
        evalstring += 'byref(contributions_chiSquaredContributions_tmp)'
    if not (chiSquaredStats is None):
        evalstring += ','
        evalstring += repr(IMSLS_CHI_SQUARED_STATS)
        checkForList(chiSquaredStats, 'chiSquaredStats')
        evalstring += ','
        chiSquaredStats_chiSquaredStats_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(chiSquaredStats_chiSquaredStats_tmp)'
    if not (statistics is None):
        evalstring += ','
        evalstring += repr(IMSLS_STATISTICS)
        checkForList(statistics, 'statistics')
        evalstring += ','
        statistics_statistics_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(statistics_statistics_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (chiSquared is None):
        processRet(chiSquared_df_tmp, shape=(1), key='df', pyvar=chiSquared)
        processRet(chiSquared_chiSquared_tmp, shape=(
            1), key='chiSquared', pyvar=chiSquared)
        processRet(chiSquared_pValue_tmp, shape=(
            1), key='pValue', pyvar=chiSquared)
    if not (lrt is None):
        processRet(lrt_df_tmp, shape=(1), key='df', pyvar=lrt)
        processRet(lrt_gSquared_tmp, shape=(1), key='gSquared', pyvar=lrt)
        processRet(lrt_pValue_tmp, shape=(1), key='pValue', pyvar=lrt)
    if not (expected is None):
        processRet(expected_expected_tmp, shape=(
            (nRows + 1), (nColumns + 1)), pyvar=expected)
    if not (contributions is None):
        processRet(contributions_chiSquaredContributions_tmp, shape=(
            (nRows + 1), (nColumns + 1)), pyvar=contributions)
    if not (chiSquaredStats is None):
        processRet(chiSquaredStats_chiSquaredStats_tmp,
                   shape=(5), pyvar=chiSquaredStats)
    if not (statistics is None):
        processRet(statistics_statistics_tmp, shape=(23, 5), pyvar=statistics)
    return result
