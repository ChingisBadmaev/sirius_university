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
from pyimsl.util.imslUtils import *
from numpy import array, empty
from ctypes import *

IMSLS_LAMBDAS = 50881
IMSLS_GAMMA_PARAM = 50879
IMSLS_METHOD = 13170
IMSLS_SMOOTHING_PAR = 14590
IMSLS_N_SAMPLE = 13470
IMSLS_RANDOM_SEED = 50600
IMSLS_CONFIDENCE = 10860
IMSLS_NULL_PROB = 50884
IMSLS_UPPER_LIMITS = 50882
imslstat = loadimsl(STAT)


def falseDiscoveryRates(pvalues, lambdas=None, gammaParam=None, method=None, smoothingPar=None, nSample=None, randomSeed=None, confidence=None, nullProb=None, upperLimits=None):
    imslstat.imsls_d_false_discovery_rates.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_false_discovery_rates('
    evalstring += 'c_int(nTests)'
    evalstring += ','
    pvalues = toNumpyArray(pvalues, 'pvalues', shape=shape,
                           dtype='double', expectedShape=(0))
    evalstring += 'pvalues.ctypes.data_as(c_void_p)'
    nTests = shape[0]
    if not (lambdas is None):
        evalstring += ','
        evalstring += repr(IMSLS_LAMBDAS)
        evalstring += ','
        evalstring += 'c_int(lambdas_nLambdas_tmp)'
        evalstring += ','
        lambdas_lambdas_tmp = toNumpyArray(
            lambdas, 'lambdas', shape=shape, dtype='double', expectedShape=(0))
        evalstring += 'lambdas_lambdas_tmp.ctypes.data_as(c_void_p)'
        lambdas_nLambdas_tmp = shape[0]
    if not (gammaParam is None):
        evalstring += ','
        evalstring += repr(IMSLS_GAMMA_PARAM)
        evalstring += ','
        evalstring += 'c_double(gammaParam)'
    if not (method is None):
        evalstring += ','
        evalstring += repr(IMSLS_METHOD)
        evalstring += ','
        evalstring += 'c_int(method)'
    if not (smoothingPar is None):
        evalstring += ','
        evalstring += repr(IMSLS_SMOOTHING_PAR)
        evalstring += ','
        evalstring += 'c_double(smoothingPar)'
    if not (nSample is None):
        evalstring += ','
        evalstring += repr(IMSLS_N_SAMPLE)
        evalstring += ','
        evalstring += 'c_int(nSample)'
    if not (randomSeed is None):
        evalstring += ','
        evalstring += repr(IMSLS_RANDOM_SEED)
        evalstring += ','
        evalstring += 'c_int(randomSeed)'
    if not (confidence is None):
        evalstring += ','
        evalstring += repr(IMSLS_CONFIDENCE)
        evalstring += ','
        evalstring += 'c_double(confidence)'
    if not (nullProb is None):
        evalstring += ','
        evalstring += repr(IMSLS_NULL_PROB)
        checkForList(nullProb, 'nullProb')
        evalstring += ','
        nullProb_pi0_tmp = c_double()
        evalstring += 'byref(nullProb_pi0_tmp)'
    if not (upperLimits is None):
        evalstring += ','
        evalstring += repr(IMSLS_UPPER_LIMITS)
        checkForList(upperLimits, 'upperLimits')
        evalstring += ','
        upperLimits_upperLimts_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(upperLimits_upperLimts_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (nullProb is None):
        processRet(nullProb_pi0_tmp, shape=(1), pyvar=nullProb)
    if not (upperLimits is None):
        processRet(upperLimits_upperLimts_tmp, shape=(2), pyvar=upperLimits)
    return processRet(result, shape=(nTests), result=True)
