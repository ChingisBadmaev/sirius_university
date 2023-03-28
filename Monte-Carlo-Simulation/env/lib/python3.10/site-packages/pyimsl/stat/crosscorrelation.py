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
from numpy import array, double, dtype, int, shape, size
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSLS_PRINT_LEVEL = 20530
IMSLS_VARIANCES = 26130
IMSLS_SE_CCF = 26160
IMSLS_CROSS_COVARIANCES = 26140
IMSLS_INPUT_MEANS = 26060
IMSLS_OUTPUT_MEANS = 26120
imslstat = loadimsl(STAT)


def crosscorrelation(x, y, lagmax, printLevel=None, variances=None, seCcf=None, crossCovariances=None, inputMeans=None, outputMeans=None):
    """ Computes the sample cross-correlation function of two stationary time series.
    """
    imslstat.imsls_d_crosscorrelation.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_crosscorrelation('
    evalstring += 'c_int(nObservations)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nObservations = shape[0]
    evalstring += ','
    y = toNumpyArray(y, 'y', shape=shape, dtype='double',
                     expectedShape=(nObservations))
    evalstring += 'y.ctypes.data_as(c_void_p)'
    evalstring += ','
    evalstring += 'c_int(lagmax)'
    if not (printLevel is None):
        evalstring += ','
        evalstring += repr(IMSLS_PRINT_LEVEL)
        evalstring += ','
        evalstring += 'c_int(printLevel)'
    if not (variances is None):
        evalstring += ','
        evalstring += repr(IMSLS_VARIANCES)
        checkForDict(variances, 'variances', [])
        evalstring += ','
        variances_xVariance_tmp = c_double()
        evalstring += 'byref(variances_xVariance_tmp)'
        evalstring += ','
        variances_yVariance_tmp = c_double()
        evalstring += 'byref(variances_yVariance_tmp)'
    if not (seCcf is None):
        evalstring += ','
        evalstring += repr(IMSLS_SE_CCF)
        checkForDict(seCcf, 'seCcf', ['seOption'])
        evalstring += ','
        seCcf_standardErrors_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(seCcf_standardErrors_tmp)'
        evalstring += ','
        seCcf_seOption_tmp = seCcf['seOption']
        evalstring += 'c_int(seCcf_seOption_tmp)'
    if not (crossCovariances is None):
        evalstring += ','
        evalstring += repr(IMSLS_CROSS_COVARIANCES)
        checkForList(crossCovariances, 'crossCovariances')
        evalstring += ','
        crossCovariances_crossCovariances_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(crossCovariances_crossCovariances_tmp)'
    if not (inputMeans is None):
        evalstring += ','
        evalstring += repr(IMSLS_INPUT_MEANS)
        checkForDict(inputMeans, 'inputMeans', ['xMeanIn', 'yMeanIn'])
        evalstring += ','
        inputMeans_xMeanIn_tmp = inputMeans['xMeanIn']
        evalstring += 'c_double(inputMeans_xMeanIn_tmp)'
        evalstring += ','
        inputMeans_yMeanIn_tmp = inputMeans['yMeanIn']
        evalstring += 'c_double(inputMeans_yMeanIn_tmp)'
    if not (outputMeans is None):
        evalstring += ','
        evalstring += repr(IMSLS_OUTPUT_MEANS)
        checkForDict(outputMeans, 'outputMeans', [])
        evalstring += ','
        outputMeans_xMeanOut_tmp = c_double()
        evalstring += 'byref(outputMeans_xMeanOut_tmp)'
        evalstring += ','
        outputMeans_yMeanOut_tmp = c_double()
        evalstring += 'byref(outputMeans_yMeanOut_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (variances is None):
        processRet(variances_xVariance_tmp, shape=(
            1), key='xVariance', pyvar=variances)
        processRet(variances_yVariance_tmp, shape=(
            1), key='yVariance', pyvar=variances)
    if not (seCcf is None):
        processRet(seCcf_standardErrors_tmp, shape=(
            2 * lagmax + 1), key='standardErrors', pyvar=seCcf)
    if not (crossCovariances is None):
        processRet(crossCovariances_crossCovariances_tmp,
                   shape=(2 * lagmax + 1), pyvar=crossCovariances)
    if not (outputMeans is None):
        processRet(outputMeans_xMeanOut_tmp, shape=(
            1), key='xMeanOut', pyvar=outputMeans)
        processRet(outputMeans_yMeanOut_tmp, shape=(
            1), key='yMeanOut', pyvar=outputMeans)
    return processRet(result, shape=(2 * lagmax + 1), result=True)
