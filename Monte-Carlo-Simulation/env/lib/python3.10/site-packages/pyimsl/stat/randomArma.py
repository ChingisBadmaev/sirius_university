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
from pyimsl.util.imslUtils import STAT, checkForBoolean, checkForList, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, int, ma, shape, zeros
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSLS_ARMA_CONSTANT = 25010
IMSLS_VAR_NOISE = 25020
IMSLS_INPUT_NOISE = 25030
IMSLS_OUTPUT_NOISE = 25040
IMSLS_NONZERO_ARLAGS = 25060
IMSLS_NONZERO_MALAGS = 25070
IMSLS_INITIAL_W = 25080
IMSLS_ACCEPT_REJECT_METHOD = 20430
imslstat = loadimsl(STAT)


def randomArma(nObservations, ar, ma, armaConstant=None, varNoise=None, inputNoise=None, outputNoise=None, nonzeroArlags=None, nonzeroMalags=None, initialW=None, acceptRejectMethod=None):
    """ Generates a time series from a specific ARMA model.
    """
    imslstat.imsls_d_random_arma.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_random_arma('
    evalstring += 'c_int(nObservations)'
    evalstring += ','
    evalstring += 'c_int(p)'
    evalstring += ','
    ar = toNumpyArray(ar, 'ar', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'ar.ctypes.data_as(c_void_p)'
    p = shape[0]
    evalstring += ','
    evalstring += 'c_int(q)'
    evalstring += ','
    ma = toNumpyArray(ma, 'ma', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'ma.ctypes.data_as(c_void_p)'
    q = shape[0]
    if not (nonzeroMalags is None):
        evalstring += ','
        evalstring += repr(IMSLS_NONZERO_MALAGS)
        evalstring += ','
        nonzeroMalags = toNumpyArray(
            nonzeroMalags, 'nonzeroMalags', shape=shape, dtype='int', expectedShape=(q))
        evalstring += 'nonzeroMalags.ctypes.data_as(c_void_p)'
    else:
        if(q > 0):
            nonzeroMalags = zeros((q), dtype='int')
            for i in range(0, q):
                nonzeroMalags[i] = i + 1
            maxMalags = nonzeroMalags[0]
            for i in range(1, q):
                if (nonzeroMalags[i] > maxMalags):
                    maxMalags = nonzeroMalags[i]
    if not (nonzeroArlags is None):
        evalstring += ','
        evalstring += repr(IMSLS_NONZERO_ARLAGS)
        evalstring += ','
        nonzeroArlags = toNumpyArray(
            nonzeroArlags, 'nonzeroArlags', shape=shape, dtype='int', expectedShape=(p))
        evalstring += 'nonzeroArLags.ctypes.data_as(c_void_p)'
    else:
        if(p > 0):
            nonzeroArlags = zeros((p), dtype='int')
            for i in range(0, p):
                nonzeroArlags[i] = i + 1
            maxArlags = nonzeroArlags[0]
            for i in range(1, p):
                if (nonzeroArlags[i] > maxArlags):
                    maxArlags = nonzeroArlags[i]
    if not (armaConstant is None):
        evalstring += ','
        evalstring += repr(IMSLS_ARMA_CONSTANT)
        evalstring += ','
        evalstring += 'c_double(armaConstant)'
    else:
        armaConstant = 0
    if not (varNoise is None):
        evalstring += ','
        evalstring += repr(IMSLS_VAR_NOISE)
        evalstring += ','
        evalstring += 'c_double(varNoise)'
    else:
        varNoise = 1.0
    if not (inputNoise is None):
        evalstring += ','
        evalstring += repr(IMSLS_INPUT_NOISE)
        evalstring += ','
        inputNoise = toNumpyArray(inputNoise, 'inputNoise', shape=shape,
                                  dtype='double', expectedShape=(nObservations + maxMalags))
        evalstring += 'aInput.ctypes.data_as(c_void_p)'
    if not (outputNoise is None):
        evalstring += ','
        evalstring += repr(IMSLS_OUTPUT_NOISE)
        checkForList(outputNoise, 'outputNoise')
        evalstring += ','
        outputNoise_aReturn_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(outputNoise_aReturn_tmp)'
    if not (initialW is None):
        evalstring += ','
        evalstring += repr(IMSLS_INITIAL_W)
        evalstring += ','
        initialW = toNumpyArray(
            initialW, 'initialW', shape=shape, dtype='double', expectedShape=(maxArlags))
        evalstring += 'initialW.ctypes.data_as(c_void_p)'
    checkForBoolean(acceptRejectMethod, 'acceptRejectMethod')
    if (acceptRejectMethod):
        evalstring += ','
        evalstring += repr(IMSLS_ACCEPT_REJECT_METHOD)
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (outputNoise is None):
        processRet(outputNoise_aReturn_tmp, shape=(
            nObservations + maxMalags), pyvar=outputNoise)
    return processRet(result, shape=(nObservations), result=True)
