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
from pyimsl.util.imslUtils import STAT, checkForBoolean, checkForList, fatalErrorCheck, loadimsl, processRet, toNumpyArray, checkForDict
from numpy import double, dtype, int, ma, max, shape, size
from ctypes import POINTER, byref, c_double, c_int, c_void_p
from .statStructs import Imsls_d_arma
from .simpleStatistics import simpleStatistics

IMSLS_NO_CONSTANT = 13340
IMSLS_CONSTANT = 10930
IMSLS_AR_LAGS = 10110
IMSLS_MA_LAGS = 13110
IMSLS_METHOD_OF_MOMENTS = 13180
IMSLS_LEAST_SQUARES = 12700
IMSLS_BACKCASTING = 10190
IMSLS_CONVERGENCE_TOLERANCE = 10990
IMSLS_RELATIVE_ERROR = 16050
IMSLS_MAX_ITERATIONS = 12970
IMSLS_MEAN_ESTIMATE = 16051
IMSLS_INITIAL_ESTIMATES = 12350
IMSLS_RESIDUAL = 14190
IMSLS_PARAM_EST_COV = 16052
IMSLS_AUTOCOV = 16054
IMSLS_SS_RESIDUAL = 14740
IMSLS_VAR_NOISE = 25020
IMSLS_ARMA_INFO = 16056
imslstat = loadimsl(STAT)


def arma(z, p, q, noConstant=None, constant=None, arLags=None, maLags=None, methodOfMoments=None, leastSquares=None, backcasting=None, convergenceTolerance=None, relativeError=None, maxIterations=None, meanEstimate=None, initialEstimates=None, residual=None, paramEstCov=None, autocov=None, ssResidual=None, varNoise=None, armaInfo=None):
    """ Computes least-square estimates of parameters for an ARMA model.
    """
    imslstat.imsls_d_arma.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_arma('
    evalstring += 'c_int(nObservations)'
    evalstring += ','
    z = toNumpyArray(z, 'z', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'z.ctypes.data_as(c_void_p)'
    nObservations = shape[0]
    evalstring += ','
    evalstring += 'c_int(p)'
    evalstring += ','
    evalstring += 'c_int(q)'
    checkForBoolean(noConstant, 'noConstant')
    if (noConstant):
        evalstring += ','
        evalstring += repr(IMSLS_NO_CONSTANT)
    checkForBoolean(constant, 'constant')
    if (constant):
        evalstring += ','
        evalstring += repr(IMSLS_CONSTANT)
    if not (arLags is None):
        evalstring += ','
        evalstring += repr(IMSLS_AR_LAGS)
        evalstring += ','
        arLags = toNumpyArray(arLags, 'arLags', shape=shape,
                              dtype='int', expectedShape=(p))
        evalstring += 'arLags.ctypes.data_as(c_void_p)'
    else:
        arLags = list(range(p))
    if not (maLags is None):
        evalstring += ','
        evalstring += repr(IMSLS_MA_LAGS)
        evalstring += ','
        maLags = toNumpyArray(maLags, 'maLags', shape=shape,
                              dtype='int', expectedShape=(q))
        evalstring += 'maLags.ctypes.data_as(c_void_p)'
    checkForBoolean(methodOfMoments, 'methodOfMoments')
    if (methodOfMoments):
        evalstring += ','
        evalstring += repr(IMSLS_METHOD_OF_MOMENTS)
    checkForBoolean(leastSquares, 'leastSquares')
    if (leastSquares):
        evalstring += ','
        evalstring += repr(IMSLS_LEAST_SQUARES)
    if not (backcasting is None):
        evalstring += ','
        evalstring += repr(IMSLS_BACKCASTING)
        checkForDict(backcasting, 'backcasting', ['length', 'tolerance'])
        evalstring += ','
        backcasting_length_tmp = backcasting['length']
        evalstring += 'c_int(backcasting_length_tmp)'
        evalstring += ','
        backcasting_tolerance_tmp = backcasting['tolerance']
        evalstring += 'c_double(backcasting_tolerance_tmp)'
    else:
        backcasting_length_tmp = 10
        sstats = simpleStatistics(z)
        backcasting_tolerance_tmp = 0.01 * sstats[2]
    if not (convergenceTolerance is None):
        evalstring += ','
        evalstring += repr(IMSLS_CONVERGENCE_TOLERANCE)
        evalstring += ','
        evalstring += 'c_double(convergenceTolerance)'
    if not (relativeError is None):
        evalstring += ','
        evalstring += repr(IMSLS_RELATIVE_ERROR)
        evalstring += ','
        evalstring += 'c_double(relativeError)'
    if not (maxIterations is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_ITERATIONS)
        evalstring += ','
        evalstring += 'c_int(maxIterations)'
    if not (meanEstimate is None):
        evalstring += ','
        evalstring += repr(IMSLS_MEAN_ESTIMATE)
        checkForList(meanEstimate, 'meanEstimate')
        evalstring += ','
        meanEstimate_meanEstimate_tmp = meanEstimate[0]
        if (not(isinstance(meanEstimate_meanEstimate_tmp, c_double))):
            meanEstimate_meanEstimate_tmp = c_double(meanEstimate[0])
        evalstring += 'byref(meanEstimate_meanEstimate_tmp)'
    if not (initialEstimates is None):
        evalstring += ','
        evalstring += repr(IMSLS_INITIAL_ESTIMATES)
        checkForList(initialEstimates, 'initialEstimates', size=2)
        evalstring += ','
        initialEstimates_ar_tmp = initialEstimates[0]
        initialEstimates_ar_tmp = toNumpyArray(
            initialEstimates_ar_tmp, 'ar', shape=shape, dtype='double', expectedShape=(p))
        evalstring += 'initialEstimates_ar_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        initialEstimates_ma_tmp = initialEstimates[1]
        initialEstimates_ma_tmp = toNumpyArray(
            initialEstimates_ma_tmp, 'ma', shape=shape, dtype='double', expectedShape=(q))
        evalstring += 'initialEstimates_ma_tmp.ctypes.data_as(c_void_p)'
    if not (residual is None):
        evalstring += ','
        evalstring += repr(IMSLS_RESIDUAL)
        checkForList(residual, 'residual')
        evalstring += ','
        residual_residual_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(residual_residual_tmp)'
    if not (paramEstCov is None):
        evalstring += ','
        evalstring += repr(IMSLS_PARAM_EST_COV)
        checkForList(paramEstCov, 'paramEstCov')
        evalstring += ','
        paramEstCov_paramEstCov_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(paramEstCov_paramEstCov_tmp)'
    if not (autocov is None):
        evalstring += ','
        evalstring += repr(IMSLS_AUTOCOV)
        checkForList(autocov, 'autocov')
        evalstring += ','
        autocov_autocov_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(autocov_autocov_tmp)'
    if not (ssResidual is None):
        evalstring += ','
        evalstring += repr(IMSLS_SS_RESIDUAL)
        checkForList(ssResidual, 'ssResidual')
        evalstring += ','
        ssResidual_ssResidual_tmp = c_double()
        evalstring += 'byref(ssResidual_ssResidual_tmp)'
    if not (varNoise is None):
        evalstring += ','
        evalstring += repr(IMSLS_VAR_NOISE)
        checkForList(varNoise, 'varNoise')
        evalstring += ','
        varNoise_avar_tmp = c_double()
        evalstring += 'byref(varNoise_avar_tmp)'
    if not (armaInfo is None):
        evalstring += ','
        evalstring += repr(IMSLS_ARMA_INFO)
        checkForList(armaInfo, 'armaInfo')
        evalstring += ','
        armaInfo_armaInfo_tmp = POINTER(Imsls_d_arma)(Imsls_d_arma())
        evalstring += 'byref(armaInfo_armaInfo_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (meanEstimate is None):
        processRet(meanEstimate_meanEstimate_tmp, shape=1, pyvar=meanEstimate)
    if not (residual is None):
        processRet(residual_residual_tmp, shape=(nObservations
                                                 - max(arLags) + backcasting_length_tmp), pyvar=residual)
    if not (paramEstCov is None):
        checkForBoolean(noConstant, 'noConstant')
        if (noConstant):
            np = p + q
        else:
            np = p + q + 1
        processRet(paramEstCov_paramEstCov_tmp,
                   shape=(np, np), pyvar=paramEstCov)
    if not (autocov is None):
        processRet(autocov_autocov_tmp, shape=(p + q + 1), pyvar=autocov)
    if not (ssResidual is None):
        processRet(ssResidual_ssResidual_tmp, shape=1, pyvar=ssResidual)
    if not (varNoise is None):
        processRet(varNoise_avar_tmp, shape=(1), pyvar=varNoise)
    if not (armaInfo is None):
        armaInfo[:] = []
        armaInfo.append(armaInfo_armaInfo_tmp)
    return processRet(result, shape=(1 + p + q), result=True)
