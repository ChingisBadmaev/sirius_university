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
from pyimsl.util.imslUtils import STAT, checkForBoolean, checkForList, fatalErrorCheck, loadimsl, toNumpyArray
from numpy import double, dtype, shape
from ctypes import byref, c_double, c_int, c_void_p

IMSLS_PRINT = 13900
IMSLS_X_RESPONSE_COL = 40410
IMSLS_CENSOR_CODES_COL = 40409
IMSLS_FREQ_RESPONSE_COL = 40411
IMSLS_STRATUM_NUMBER_COL = 40412
IMSLS_SORTED = 40044
IMSLS_N_MISSING = 13440
imslstat = loadimsl(STAT)


def kaplanMeierEstimates(x, t_print=None, xResponseCol=None, censorCodesCol=None, freqResponseCol=None, stratumNumberCol=None, sorted=None, nMissing=None):
    """ Computes Kaplan-Meier estimates of survival probabilities in stratified samples.
    """
    imslstat.imsls_d_kaplan_meier_estimates.restype = c_double
    shape = []
    evalstring = 'imslstat.imsls_d_kaplan_meier_estimates('
    evalstring += 'c_int(nObservations)'
    evalstring += ','
    evalstring += 'c_int(ncol)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nObservations = shape[0]
    ncol = shape[1]
    checkForBoolean(t_print, 't_print')
    if (t_print):
        evalstring += ','
        evalstring += repr(IMSLS_PRINT)
    if not (xResponseCol is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_RESPONSE_COL)
        evalstring += ','
        evalstring += 'c_int(xResponseCol)'
    if not (censorCodesCol is None):
        evalstring += ','
        evalstring += repr(IMSLS_CENSOR_CODES_COL)
        evalstring += ','
        evalstring += 'c_int(censorCodesCol)'
    if not (freqResponseCol is None):
        evalstring += ','
        evalstring += repr(IMSLS_FREQ_RESPONSE_COL)
        evalstring += ','
        evalstring += 'c_int(freqResponseCol)'
    if not (stratumNumberCol is None):
        evalstring += ','
        evalstring += repr(IMSLS_STRATUM_NUMBER_COL)
        evalstring += ','
        evalstring += 'c_int(stratumNumberCol)'
    checkForBoolean(sorted, 'sorted')
    if (sorted):
        evalstring += ','
        evalstring += repr(IMSLS_SORTED)
    if not (nMissing is None):
        evalstring += ','
        evalstring += repr(IMSLS_N_MISSING)
        checkForList(nMissing, 'nMissing')
        evalstring += ','
        nMissing_nrmiss_tmp = c_int()
        evalstring += 'byref(nMissing_nrmiss_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (nMissing is None):
        processRet(nMissing_nrmiss_tmp, shape=1, pyvar=nMissing)
    return result
