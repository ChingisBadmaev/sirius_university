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
from pyimsl.util.VersionFacade import VersionFacade
from numpy import double, dtype, shape, size
from ctypes import POINTER, byref, c_double, c_int, c_void_p
from .statStructs import Imsls_d_arma

IMSLS_INITIAL_ESTIMATES = 12350
IMSLS_PRINT_LEVEL = 20530
IMSLS_MAX_ITERATIONS = 12970
IMSLS_LOG_LIKELIHOOD = 50180
IMSLS_VAR_NOISE = 25020
IMSLS_ARMA_INFO = 16056
IMSLS_MEAN_ESTIMATE = 16051
imslstat = loadimsl(STAT)


def maxArma(w, p, q, initialEstimates=None, printLevel=None, maxIterations=None, logLikelihood=None, varNoise=None, armaInfo=None, meanEstimate=None):
    """ Exact maximum likelihood estimation of the parameters in a univariate ARMA (autoregressive, moving average) time series model.
    """
    VersionFacade.checkVersion(6)
    imslstat.imsls_d_max_arma.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_max_arma('
    evalstring += 'c_int(nObs)'
    evalstring += ','
    w = toNumpyArray(w, 'w', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'w.ctypes.data_as(c_void_p)'
    nObs = shape[0]
    evalstring += ','
    evalstring += 'c_int(p)'
    evalstring += ','
    evalstring += 'c_int(q)'
    if not (initialEstimates is None):
        evalstring += ','
        evalstring += repr(IMSLS_INITIAL_ESTIMATES)
        checkForDict(initialEstimates, 'initialEstimates',
                     ['initAr', 'initMa'])
        evalstring += ','
        initialEstimates_initAr_tmp = initialEstimates['initAr']
        initialEstimates_initAr_tmp = toNumpyArray(
            initialEstimates_initAr_tmp, 'initAr', shape=shape, dtype='double', expectedShape=(p))
        evalstring += 'initialEstimates_initAr_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        initialEstimates_initMa_tmp = initialEstimates['initMa']
        initialEstimates_initMa_tmp = toNumpyArray(
            initialEstimates_initMa_tmp, 'initMa', shape=shape, dtype='double', expectedShape=(q))
        evalstring += 'initialEstimates_initMa_tmp.ctypes.data_as(c_void_p)'
    if not (printLevel is None):
        evalstring += ','
        evalstring += repr(IMSLS_PRINT_LEVEL)
        evalstring += ','
        evalstring += 'c_int(printLevel)'
    if not (maxIterations is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_ITERATIONS)
        evalstring += ','
        evalstring += 'c_int(maxIterations)'
    if not (logLikelihood is None):
        evalstring += ','
        evalstring += repr(IMSLS_LOG_LIKELIHOOD)
        checkForList(logLikelihood, 'logLikelihood')
        evalstring += ','
        logLikelihood_logLikelihood_tmp = c_double()
        evalstring += 'byref(logLikelihood_logLikelihood_tmp)'
    if not (varNoise is None):
        evalstring += ','
        evalstring += repr(IMSLS_VAR_NOISE)
        checkForList(varNoise, 'varNoise')
        evalstring += ','
        varNoise_varNoise_tmp = c_double()
        evalstring += 'byref(varNoise_varNoise_tmp)'
    if not (armaInfo is None):
        evalstring += ','
        evalstring += repr(IMSLS_ARMA_INFO)
        checkForList(armaInfo, 'armaInfo')
        evalstring += ','
        armaInfo_armaInfo_tmp = POINTER(Imsls_d_arma)(Imsls_d_arma())
        evalstring += 'byref(armaInfo_armaInfo_tmp)'
    if not (meanEstimate is None):
        evalstring += ','
        evalstring += repr(IMSLS_MEAN_ESTIMATE)
        checkForList(meanEstimate, 'meanEstimate')
        evalstring += ','
        meanEstimate_meanEstimate_tmp = meanEstimate[0]
        if (not(isinstance(meanEstimate_meanEstimate_tmp, c_double))):
            meanEstimate_meanEstimate_tmp = c_double(meanEstimate[0])
        evalstring += 'byref(meanEstimate_meanEstimate_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (logLikelihood is None):
        processRet(logLikelihood_logLikelihood_tmp,
                   shape=1, pyvar=logLikelihood)
    if not (varNoise is None):
        processRet(varNoise_varNoise_tmp, shape=1, pyvar=varNoise)
    if not (armaInfo is None):
        processRet(armaInfo_armaInfo_tmp, shape=1, pyvar=armaInfo)
    if not (meanEstimate is None):
        processRet(meanEstimate_meanEstimate_tmp, shape=1, pyvar=meanEstimate)
    return processRet(result, shape=(1 + p + q), result=True)
