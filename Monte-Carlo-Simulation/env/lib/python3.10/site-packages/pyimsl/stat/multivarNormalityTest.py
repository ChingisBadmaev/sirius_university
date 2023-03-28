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

IMSLS_FREQUENCIES = 11790
IMSLS_WEIGHTS = 15400
IMSLS_SUM_FREQ = 30035
IMSLS_SUM_WEIGHTS = 20800
IMSLS_N_ROWS_MISSING = 20400
IMSLS_MEANS = 13120
IMSLS_R = 16068
imslstat = loadimsl(STAT)


def multivarNormalityTest(x, frequencies=None, weights=None, sumFreq=None, sumWeights=None, nRowsMissing=None, means=None, r=None):
    """ Computes Mardia's multivariate measures of skewness and kurtosis and tests for multivariate normality.
    """
    imslstat.imsls_d_multivar_normality_test.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_multivar_normality_test('
    evalstring += 'c_int(nObservations)'
    evalstring += ','
    evalstring += 'c_int(nVariables)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nObservations = shape[0]
    nVariables = shape[1]
    if not (frequencies is None):
        evalstring += ','
        evalstring += repr(IMSLS_FREQUENCIES)
        evalstring += ','
        frequencies = toNumpyArray(
            frequencies, 'frequencies', shape=shape, dtype='double', expectedShape=(nRows))
        evalstring += 'frequencies.ctypes.data_as(c_void_p)'
    if not (weights is None):
        evalstring += ','
        evalstring += repr(IMSLS_WEIGHTS)
        evalstring += ','
        weights = toNumpyArray(
            weights, 'weights', shape=shape, dtype='double', expectedShape=(nRows))
        evalstring += 'weights.ctypes.data_as(c_void_p)'
    if not (sumFreq is None):
        evalstring += ','
        evalstring += repr(IMSLS_SUM_FREQ)
        checkForList(sumFreq, 'sumFreq')
        evalstring += ','
        sumFreq_sumFrequencies_tmp = c_int()
        evalstring += 'byref(sumFreq_sumFrequencies_tmp)'
    if not (sumWeights is None):
        evalstring += ','
        evalstring += repr(IMSLS_SUM_WEIGHTS)
        checkForList(sumWeights, 'sumWeights')
        evalstring += ','
        sumWeights_sumWeights_tmp = c_double()
        evalstring += 'byref(sumWeights_sumWeights_tmp)'
    if not (nRowsMissing is None):
        evalstring += ','
        evalstring += repr(IMSLS_N_ROWS_MISSING)
        checkForList(nRowsMissing, 'nRowsMissing')
        evalstring += ','
        nRowsMissing_nrmiss_tmp = c_int()
        evalstring += 'byref(nRowsMissing_nrmiss_tmp)'
    if not (means is None):
        evalstring += ','
        evalstring += repr(IMSLS_MEANS)
        checkForList(means, 'means')
        evalstring += ','
        means_means_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(means_means_tmp)'
    if not (r is None):
        evalstring += ','
        evalstring += repr(IMSLS_R)
        checkForList(r, 'r')
        evalstring += ','
        r_rMatrix_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(r_rMatrix_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (sumFreq is None):
        processRet(sumFreq_sumFrequencies_tmp, shape=1, pyvar=sumFreq)
    if not (sumWeights is None):
        processRet(sumWeights_sumWeights_tmp, shape=1, pyvar=sumWeights)
    if not (nRowsMissing is None):
        processRet(nRowsMissing_nrmiss_tmp, shape=1, pyvar=nRowsMissing)
    if not (means is None):
        processRet(means_means_tmp, shape=(nVariables), pyvar=means)
    if not (r is None):
        processRet(r_rMatrix_tmp, shape=(nVariables, nVariables), pyvar=r)
    return processRet(result, shape=(13), result=True)
