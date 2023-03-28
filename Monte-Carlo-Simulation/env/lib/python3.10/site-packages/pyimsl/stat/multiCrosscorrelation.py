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

IMSLS_PRINT_LEVEL = 20530
IMSLS_VARIANCES = 26130
IMSLS_CROSS_COVARIANCES = 26140
IMSLS_INPUT_MEANS = 26060
IMSLS_OUTPUT_MEANS = 26120
imslstat = loadimsl(STAT)


def multiCrosscorrelation(x, y, lagmax, printLevel=None, variances=None, crossCovariances=None, inputMeans=None, outputMeans=None):
    """ Computes the multichannel cross-correlation function of two mutually stationary multichannel time series.
    """
    imslstat.imsls_d_multi_crosscorrelation.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_multi_crosscorrelation('
    evalstring += 'c_int(nObservationsX)'
    evalstring += ','
    evalstring += 'c_int(nChannelX)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nObservationsX = shape[0]
    nChannelX = shape[1]
    evalstring += ','
    evalstring += 'c_int(nObservationsY)'
    evalstring += ','
    evalstring += 'c_int(nChannelY)'
    evalstring += ','
    y = toNumpyArray(y, 'y', shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'y.ctypes.data_as(c_void_p)'
    nObservationsY = shape[0]
    nChannelY = shape[1]
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
        variances_xVariance_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(variances_xVariance_tmp)'
        evalstring += ','
        variances_yVariance_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(variances_yVariance_tmp)'
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
        inputMeans_xMeanIn_tmp = toNumpyArray(
            inputMeans_xMeanIn_tmp, 'xMeanIn', shape=shape, dtype='double', expectedShape=(nChannelX))
        evalstring += 'inputMeans_xMeanIn_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        inputMeans_yMeanIn_tmp = inputMeans['yMeanIn']
        inputMeans_yMeanIn_tmp = toNumpyArray(
            inputMeans_yMeanIn_tmp, 'yMeanIn', shape=shape, dtype='double', expectedShape=(nChannelY))
        evalstring += 'inputMeans_yMeanIn_tmp.ctypes.data_as(c_void_p)'
    if not (outputMeans is None):
        evalstring += ','
        evalstring += repr(IMSLS_OUTPUT_MEANS)
        checkForDict(outputMeans, 'outputMeans', [])
        evalstring += ','
        outputMeans_xMeanOut_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(outputMeans_xMeanOut_tmp)'
        evalstring += ','
        outputMeans_yMeanOut_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(outputMeans_yMeanOut_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (variances is None):
        processRet(variances_xVariance_tmp, shape=(
            nChannelX), key='xVariance', pyvar=variances)
        processRet(variances_yVariance_tmp, shape=(
            nChannelY), key='yVariance', pyvar=variances)
    if not (crossCovariances is None):
        processRet(crossCovariances_crossCovariances_tmp, shape=(
            nChannelX * nChannelY * (2 * lagmax + 1)), pyvar=crossCovariances)
    if not (outputMeans is None):
        processRet(outputMeans_xMeanOut_tmp, shape=(
            nChannelX), key='xMeanOut', pyvar=outputMeans)
        processRet(outputMeans_yMeanOut_tmp, shape=(
            nChannelY), key='yMeanOut', pyvar=outputMeans)
    return processRet(result, shape=(nChannelX * nChannelY * (2 * lagmax + 1)), result=True)
