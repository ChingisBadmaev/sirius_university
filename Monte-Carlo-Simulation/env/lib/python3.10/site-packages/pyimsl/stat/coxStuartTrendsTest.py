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
from numpy import double, dtype, shape, size
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSLS_DISPERSION = 30017
IMSLS_FUZZ = 11870
IMSLS_STAT = 14770
IMSLS_N_MISSING = 13440
imslstat = loadimsl(STAT)


def coxStuartTrendsTest(x, dispersion=None, fuzz=None, stat=None, nMissing=None):
    """ Performs the Cox and Stuart sign test for trends in location and dispersion.
    """
    imslstat.imsls_d_cox_stuart_trends_test.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_cox_stuart_trends_test('
    evalstring += 'c_int(nObservations)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nObservations = shape[0]
    if not (dispersion is None):
        evalstring += ','
        evalstring += repr(IMSLS_DISPERSION)
        checkForDict(dispersion, 'dispersion', ['k', 'ids'])
        evalstring += ','
        dispersion_k_tmp = dispersion['k']
        evalstring += 'c_int(dispersion_k_tmp)'
        evalstring += ','
        dispersion_ids_tmp = dispersion['ids']
        evalstring += 'c_int(dispersion_ids_tmp)'
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
        stat_nstat_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(stat_nstat_tmp)'
    if not (nMissing is None):
        evalstring += ','
        evalstring += repr(IMSLS_N_MISSING)
        checkForList(nMissing, 'nMissing')
        evalstring += ','
        nMissing_nMissing_tmp = c_int()
        evalstring += 'byref(nMissing_nMissing_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (stat is None):
        processRet(stat_nstat_tmp, shape=(8), pyvar=stat)
    if not (nMissing is None):
        processRet(nMissing_nMissing_tmp, shape=(1), pyvar=nMissing)
    return processRet(result, shape=(8), result=True)
