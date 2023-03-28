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

IMSLS_REGRESSION = 50750
IMSLS_REGRESSION_FORECASTS = 50760
IMSLS_REGRESSION_INDICES = 50770
IMSLS_NO_TREND = 50781
IMSLS_MAX_ITERATIONS = 12970
IMSLS_PRINT_LEVEL = 20530
IMSLS_FORECASTS = 25730
IMSLS_REGRESSION_COEF = 50790
IMSLS_SE_ARMA = 50813
IMSLS_VAR_NOISE = 25020
IMSLS_SE_COEF = 50792
IMSLS_COEF_COVARIANCES = 10690
IMSLS_AIC = 30042
IMSLS_LOG_LIKELIHOOD = 50180
imslstat = loadimsl(STAT)


def regressionArima(nObs, y, model, regression=None, regressionForecasts=None, regressionIndices=None, noTrend=None, maxIterations=None, printLevel=None, forecasts=None, regressionCoef=None, seArma=None, varNoise=None, seCoef=None, coefCovariances=None, aic=None, logLikelihood=None):
    imslstat.imsls_d_regression_arima.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_regression_arima('
    evalstring += 'c_int(nObs)'
    evalstring += ','
    y = toNumpyArray(y, 'y', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'y.ctypes.data_as(c_void_p)'
    evalstring += ','
    model = toNumpyArray(model, 'model', shape=shape,
                         dtype='int', expectedShape=(3))
    evalstring += 'model.ctypes.data_as(c_void_p)'
    p_tmp = model[0]
    d_tmp = model[1]
    q_tmp = model[2]
    if not (regression is None):
        evalstring += ','
        evalstring += repr(IMSLS_REGRESSION)
        evalstring += ','
        evalstring += 'c_int(regression_nRegressors_tmp)'
        evalstring += ','
        regression_x_tmp = toNumpyArray(
            regression, 'regression', shape=shape, dtype='double', expectedShape=(0, 0))
        evalstring += 'regression_x_tmp.ctypes.data_as(c_void_p)'
        regression_nRegressors_tmp = shape[1]
    if not (regressionForecasts is None):
        evalstring += ','
        evalstring += repr(IMSLS_REGRESSION_FORECASTS)
        evalstring += ','
        regressionForecasts = toNumpyArray(regressionForecasts, 'regressionForecasts',
                                           shape=shape, dtype='double', expectedShape=(0, regression_nRegressors_tmp))
        evalstring += 'regressionForecasts.ctypes.data_as(c_void_p)'
        nPredict = shape[0]
    if not (regressionIndices is None):
        evalstring += ','
        evalstring += repr(IMSLS_REGRESSION_INDICES)
        evalstring += ','
        evalstring += 'c_int(regressionIndices_nIndices_tmp)'
        evalstring += ','
        regressionIndices_indices_tmp = toNumpyArray(
            regressionIndices, 'regressionIndices', shape=shape, dtype='int', expectedShape=(0))
        evalstring += 'regressionIndices_indices_tmp.ctypes.data_as(c_void_p)'
        regressionIndices_nIndices_tmp = shape[0]
    checkForBoolean(noTrend, 'noTrend')
    t = 1  # used for output array size later.
    if (noTrend):
        t = 0
        evalstring += ','
        evalstring += repr(IMSLS_NO_TREND)
    if not (maxIterations is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_ITERATIONS)
        evalstring += ','
        evalstring += 'c_int(maxIterations)'
    if not (printLevel is None):
        evalstring += ','
        evalstring += repr(IMSLS_PRINT_LEVEL)
        evalstring += ','
        evalstring += 'c_int(printLevel)'
    if not (forecasts is None):
        evalstring += ','
        evalstring += repr(IMSLS_FORECASTS)
        checkForDict(forecasts, 'forecasts', ['nPredict'])
        evalstring += ','
        forecasts_nPredict_tmp = c_int(forecasts['nPredict'])
        nPredict = forecasts['nPredict']
        evalstring += 'forecasts_nPredict_tmp'
        evalstring += ','
        forecasts_forecasts_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(forecasts_forecasts_tmp)'
        evalstring += ','
        forecasts_forecastVariances_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(forecasts_forecastVariances_tmp)'
    if not (regressionCoef is None):
        evalstring += ','
        evalstring += repr(IMSLS_REGRESSION_COEF)
        checkForList(regressionCoef, 'regressionCoef')
        evalstring += ','
        regressionCoef_coefficients_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(regressionCoef_coefficients_tmp)'
    if not (seArma is None):
        evalstring += ','
        evalstring += repr(IMSLS_SE_ARMA)
        checkForList(seArma, 'seArma')
        evalstring += ','
        seArma_armaStdErrors_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(seArma_armaStdErrors_tmp)'
    if not (varNoise is None):
        evalstring += ','
        evalstring += repr(IMSLS_VAR_NOISE)
        checkForList(varNoise, 'varNoise')
        evalstring += ','
        varNoise_avar_tmp = c_double()
        evalstring += 'byref(varNoise_avar_tmp)'
    if not (seCoef is None):
        evalstring += ','
        evalstring += repr(IMSLS_SE_COEF)
        checkForList(seCoef, 'seCoef')
        evalstring += ','
        seCoef_regcoefStdError_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(seCoef_regcoefStdError_tmp)'
    if not (coefCovariances is None):
        evalstring += ','
        evalstring += repr(IMSLS_COEF_COVARIANCES)
        checkForList(coefCovariances, 'coefCovariances')
        evalstring += ','
        coefCovariances_coefCovar_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(coefCovariances_coefCovar_tmp)'
    if not (aic is None):
        evalstring += ','
        evalstring += repr(IMSLS_AIC)
        checkForList(aic, 'aic')
        evalstring += ','
        aic_aic_tmp = c_double()
        evalstring += 'byref(aic_aic_tmp)'
    if not (logLikelihood is None):
        evalstring += ','
        evalstring += repr(IMSLS_LOG_LIKELIHOOD)
        checkForList(logLikelihood, 'logLikelihood')
        evalstring += ','
        logLikelihood_logLikelihood_tmp = c_double()
        evalstring += 'byref(logLikelihood_logLikelihood_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (forecasts is None):
        processRet(forecasts_forecasts_tmp, shape=(
            forecasts_nPredict_tmp), key='forecasts', pyvar=forecasts)
        processRet(forecasts_forecastVariances_tmp, shape=(
            forecasts_nPredict_tmp), key='forecastVariances', pyvar=forecasts)
    if not (regressionCoef is None):
        processRet(regressionCoef_coefficients_tmp, shape=(
            regression_nRegressors_tmp + t), pyvar=regressionCoef)
    if not (seArma is None):
        processRet(seArma_armaStdErrors_tmp,
                   shape=(p_tmp + q_tmp), pyvar=seArma)
    if not (varNoise is None):
        processRet(varNoise_avar_tmp, shape=(1), pyvar=varNoise)
    if not (seCoef is None):
        processRet(seCoef_regcoefStdError_tmp, shape=(
            regression_nRegressors_tmp + t), pyvar=seCoef)
    if not (coefCovariances is None):
        processRet(coefCovariances_coefCovar_tmp, shape=(
            regression_nRegressors_tmp + t, regression_nRegressors_tmp + t), pyvar=coefCovariances)
    if not (aic is None):
        processRet(aic_aic_tmp, shape=(1), pyvar=aic)
    if not (logLikelihood is None):
        processRet(logLikelihood_logLikelihood_tmp,
                   shape=(1), pyvar=logLikelihood)
    return processRet(result, shape=(1 + p_tmp + q_tmp), result=True)
