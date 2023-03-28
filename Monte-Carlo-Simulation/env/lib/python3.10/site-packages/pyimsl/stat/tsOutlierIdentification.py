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
from pyimsl.util.VersionFacade import VersionFacade
from numpy import double, dtype, int, shape
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSLS_DELTA = 50220
IMSLS_CRITICAL = 50230
IMSLS_EPSILON = 50240
IMSLS_RELATIVE_ERROR = 16050
IMSLS_RESIDUAL = 14190
IMSLS_RESIDUAL_SIGMA = 50250
IMSLS_NUM_OUTLIERS = 50260
IMSLS_OUTLIER_STATISTICS = 50310
IMSLS_TAU_STATISTICS = 50330
IMSLS_OMEGA_WEIGHTS = 50350
IMSLS_ARMA_PARAM = 50370
IMSLS_AIC = 30042
imslstat = loadimsl(STAT)


def tsOutlierIdentification(model, w, delta=None, critical=None, epsilon=None, relativeError=None, residual=None, residualSigma=None, numOutliers=None, outlierStatistics=None, tauStatistics=None, omegaWeights=None, armaParam=None, aic=None):
    """ Detects and determines outliers and simultaneously estimates the model parameters in a time series whose underlying outlier free series follows a general seasonal or nonseasonal ARMA model.
    """
    VersionFacade.checkVersion(6)
    imslstat.imsls_d_ts_outlier_identification.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_ts_outlier_identification('
    evalstring += 'c_int(nObs)'
    evalstring += ','
    model = toNumpyArray(model, 'model', shape=shape,
                         dtype='int', expectedShape=(4))
    evalstring += 'model.ctypes.data_as(c_void_p)'
    evalstring += ','
    w = toNumpyArray(w, 'w', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'w.ctypes.data_as(c_void_p)'
    nObs = shape[0]
    if not (delta is None):
        evalstring += ','
        evalstring += repr(IMSLS_DELTA)
        evalstring += ','
        evalstring += 'c_double(delta)'
    if not (critical is None):
        evalstring += ','
        evalstring += repr(IMSLS_CRITICAL)
        evalstring += ','
        evalstring += 'c_double(critical)'
    if not (epsilon is None):
        evalstring += ','
        evalstring += repr(IMSLS_EPSILON)
        evalstring += ','
        evalstring += 'c_double(epsilon)'
    if not (relativeError is None):
        evalstring += ','
        evalstring += repr(IMSLS_RELATIVE_ERROR)
        evalstring += ','
        evalstring += 'c_double(relativeError)'
    if not (residual is None):
        evalstring += ','
        evalstring += repr(IMSLS_RESIDUAL)
        checkForList(residual, 'residual')
        evalstring += ','
        residual_residual_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(residual_residual_tmp)'
    if not (residualSigma is None):
        evalstring += ','
        evalstring += repr(IMSLS_RESIDUAL_SIGMA)
        checkForList(residualSigma, 'residualSigma')
        evalstring += ','
        residualSigma_residualSigma_tmp = c_double()
        evalstring += 'byref(residualSigma_residualSigma_tmp)'
    # if not (numOutliers is None):
    # always get this as we might need for outlier_stats
    evalstring += ','
    evalstring += repr(IMSLS_NUM_OUTLIERS)
    checkForList(numOutliers, 'numOutliers')
    evalstring += ','
    numOutliers_numOutliers_tmp = c_int()
    evalstring += 'byref(numOutliers_numOutliers_tmp)'
    if not (outlierStatistics is None):
        evalstring += ','
        evalstring += repr(IMSLS_OUTLIER_STATISTICS)
        checkForList(outlierStatistics, 'outlierStatistics')
        evalstring += ','
        outlierStatistics_outlierStatistics_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(outlierStatistics_outlierStatistics_tmp)'
    if not (tauStatistics is None):
        evalstring += ','
        evalstring += repr(IMSLS_TAU_STATISTICS)
        checkForList(tauStatistics, 'tauStatistics')
        evalstring += ','
        tauStatistics_tauStatistics_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(tauStatistics_tauStatistics_tmp)'
    if not (omegaWeights is None):
        evalstring += ','
        evalstring += repr(IMSLS_OMEGA_WEIGHTS)
        checkForList(omegaWeights, 'omegaWeights')
        evalstring += ','
        omegaWeights_omegaWeights_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(omegaWeights_omegaWeights_tmp)'
    if not (armaParam is None):
        evalstring += ','
        evalstring += repr(IMSLS_ARMA_PARAM)
        checkForList(armaParam, 'armaParam')
        evalstring += ','
        armaParam_armaParam_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(armaParam_armaParam_tmp)'
    if not (aic is None):
        evalstring += ','
        evalstring += repr(IMSLS_AIC)
        checkForList(aic, 'aic')
        evalstring += ','
        aic_aic_tmp = c_double()
        evalstring += 'byref(aic_aic_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (residual is None):
        processRet(residual_residual_tmp, shape=(nObs), pyvar=residual)
    if not (residualSigma is None):
        processRet(residualSigma_residualSigma_tmp,
                   shape=1, pyvar=residualSigma)
    if not (numOutliers is None):
        processRet(numOutliers_numOutliers_tmp, shape=1, pyvar=numOutliers)
    if not (outlierStatistics is None):
        processRet(outlierStatistics_outlierStatistics_tmp, shape=(
            numOutliers_numOutliers_tmp.value, 2), pyvar=outlierStatistics)
    if not (tauStatistics is None):
        processRet(tauStatistics_tauStatistics_tmp, shape=(
            numOutliers_numOutliers_tmp.value), pyvar=tauStatistics)
    if not (omegaWeights is None):
        processRet(omegaWeights_omegaWeights_tmp, shape=(
            numOutliers_numOutliers_tmp.value), pyvar=omegaWeights)
    if not (armaParam is None):
        processRet(armaParam_armaParam_tmp, shape=(
            1 + model[0] + model[1]), pyvar=armaParam)
    if not (aic is None):
        processRet(aic_aic_tmp, shape=1, pyvar=aic)
    return processRet(result, shape=(nObs), result=True)
