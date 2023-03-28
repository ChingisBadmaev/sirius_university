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
from numpy import double, dtype, int, shape, size
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSLS_METHOD = 13170
IMSLS_MAX_LAG = 25160
IMSLS_MODEL = 20100
IMSLS_DELTA = 50220
IMSLS_CRITICAL = 50230
IMSLS_EPSILON = 50240
IMSLS_RESIDUAL = 14190
IMSLS_RESIDUAL_SIGMA = 50250
IMSLS_NUM_OUTLIERS = 50260
IMSLS_P_INITIAL = 50390
IMSLS_Q_INITIAL = 50400
IMSLS_S_INITIAL = 50410
IMSLS_D_INITIAL = 50170
IMSLS_OUTLIER_STATISTICS = 50310
IMSLS_AIC = 30042
IMSLS_AICC = 50630
IMSLS_BIC = 50631
IMSLS_MODEL_SELECTION_CRITERION = 50632
IMSLS_OUT_FREE_SERIES = 50420
IMSLS_CONFIDENCE = 10860
IMSLS_NUM_PREDICT = 50440
IMSLS_OUT_FREE_FORECAST = 50300
IMSLS_OUTLIER_FORECAST = 50450
IMSLS_SUPPLY_WORK_ARRAYS = 50900
imslstat = loadimsl(STAT)


def autoArima(tpoints, x, method=None, maxLag=None, model=None, delta=None, critical=None, epsilon=None, residual=None, residualSigma=None, numOutliers=None, pInitial=None, qInitial=None, sInitial=None, dInitial=None, outlierStatistics=None, modelSelectionCriterion=None, aic=None, aicc=None, bic=None, outFreeSeries=None, confidence=None, numPredict=None, outFreeForecast=None, outlierForecast=None, supplyWorkArrays=None):
    """ Automatically identifies time series outliers, determines parameters of a multiplicative seasonal ARIMA model and produces forecasts that incorporate the effects of outliers whose effects persist beyond the end of the series.
    """
    VersionFacade.checkVersion(6)
    imslstat.imsls_d_auto_arima.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_auto_arima('
    evalstring += 'c_int(nObs)'
    evalstring += ','
    tpoints = toNumpyArray(tpoints, 'tpoints', shape=shape,
                           dtype='int', expectedShape=(0))
    evalstring += 'tpoints.ctypes.data_as(c_void_p)'
    nObs = shape[0]
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(nObs))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    if not (method is None):
        evalstring += ','
        evalstring += repr(IMSLS_METHOD)
        evalstring += ','
        evalstring += 'c_int(method)'
    else:
        method = 1
    if not (maxLag is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_LAG)
        evalstring += ','
        evalstring += 'c_int(maxLag)'
    if not (model is None):
        if method == 1 or method == 2:  # input ignored, just used for output
            checkForList(model, 'model')
            imodel = [0, 0, 0, 0]
            model_model_tmp = toNumpyArray(
                imodel, 'model', shape=shape, dtype='int', expectedShape=(0))
        else:  # input expected
            checkForList(model, 'model', size=4)
            model_model_tmp = toNumpyArray(
                model, 'model', shape=shape, dtype='int', expectedShape=(4))
    else:  # no model passed but still need it internally
        imodel = [0, 0, 0, 0]
        model_model_tmp = toNumpyArray(
            imodel, 'model', shape=shape, dtype='int', expectedShape=(0))
    evalstring += ','
    evalstring += repr(IMSLS_MODEL)
    evalstring += ','
    evalstring += 'model_model_tmp.ctypes.data_as(c_void_p)'
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
    if not (numOutliers is None):
        evalstring += ','
        evalstring += repr(IMSLS_NUM_OUTLIERS)
        checkForList(numOutliers, 'numOutliers')
        evalstring += ','
        numOutliers_numOutliers_tmp = c_int()
        evalstring += 'byref(numOutliers_numOutliers_tmp)'
    if not (pInitial is None):
        evalstring += ','
        evalstring += repr(IMSLS_P_INITIAL)
        evalstring += ','
        evalstring += 'c_int(pInitial_nPInitial_tmp)'
        evalstring += ','
        pInitial_pInitial_tmp = toNumpyArray(
            pInitial, 'pInitial', shape=shape, dtype='int', expectedShape=(0))
        evalstring += 'pInitial_pInitial_tmp.ctypes.data_as(c_void_p)'
        pInitial_nPInitial_tmp = shape[0]
    if not (qInitial is None):
        evalstring += ','
        evalstring += repr(IMSLS_Q_INITIAL)
        evalstring += ','
        evalstring += 'c_int(qInitial_nQInitial_tmp)'
        evalstring += ','
        qInitial_qInitial_tmp = toNumpyArray(
            qInitial, 'qInitial', shape=shape, dtype='int', expectedShape=(0))
        evalstring += 'qInitial_qInitial_tmp.ctypes.data_as(c_void_p)'
        qInitial_nQInitial_tmp = shape[0]
    if not (sInitial is None):
        evalstring += ','
        evalstring += repr(IMSLS_S_INITIAL)
        evalstring += ','
        evalstring += 'c_int(sInitial_nSInitial_tmp)'
        evalstring += ','
        sInitial_sInitial_tmp = toNumpyArray(
            sInitial, 'sInitial', shape=shape, dtype='int', expectedShape=(0))
        evalstring += 'sInitial_sInitial_tmp.ctypes.data_as(c_void_p)'
        sInitial_nSInitial_tmp = shape[0]
    if not (dInitial is None):
        evalstring += ','
        evalstring += repr(IMSLS_D_INITIAL)
        evalstring += ','
        evalstring += 'c_int(dInitial_nDInitial_tmp)'
        evalstring += ','
        dInitial_dInitial_tmp = toNumpyArray(
            dInitial, 'dInitial', shape=shape, dtype='int', expectedShape=(0))
        evalstring += 'dInitial_dInitial_tmp.ctypes.data_as(c_void_p)'
        dInitial_nDInitial_tmp = shape[0]
    if not (outlierStatistics is None):
        evalstring += ','
        evalstring += repr(IMSLS_OUTLIER_STATISTICS)
        checkForList(outlierStatistics, 'outlierStatistics')
        evalstring += ','
        outlierStatistics_outlierStatistics_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(outlierStatistics_outlierStatistics_tmp)'
    if not (modelSelectionCriterion is None):
        VersionFacade.checkVersion(7)
        evalstring += ','
        evalstring += repr(IMSLS_MODEL_SELECTION_CRITERION)
        evalstring += ','
        evalstring += 'c_int(modelSelectionCriterion)'
    else:
        modelSelectionCriterion = 0
    if not (aic is None):
        evalstring += ','
        evalstring += repr(IMSLS_AIC)
        checkForList(aic, 'aic')
        evalstring += ','
        aic_aic_tmp = c_double()
        evalstring += 'byref(aic_aic_tmp)'
    if not (aicc is None):
        VersionFacade.checkVersion(7)
        evalstring += ','
        evalstring += repr(IMSLS_AICC)
        checkForList(aicc, 'aicc')
        evalstring += ','
        aicc_aicc_tmp = c_double()
        evalstring += 'byref(aicc_aicc_tmp)'
    if not (bic is None):
        VersionFacade.checkVersion(7)
        evalstring += ','
        evalstring += repr(IMSLS_BIC)
        checkForList(bic, 'bic')
        evalstring += ','
        bic_bic_tmp = c_double()
        evalstring += 'byref(bic_bic_tmp)'
    if not (outFreeSeries is None):
        evalstring += ','
        evalstring += repr(IMSLS_OUT_FREE_SERIES)
        checkForList(outFreeSeries, 'outFreeSeries')
        evalstring += ','
        outFreeSeries_outFreeSeries_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(outFreeSeries_outFreeSeries_tmp)'
    if not (confidence is None):
        evalstring += ','
        evalstring += repr(IMSLS_CONFIDENCE)
        evalstring += ','
        evalstring += 'c_double(confidence)'
    if not (numPredict is None):
        evalstring += ','
        evalstring += repr(IMSLS_NUM_PREDICT)
        evalstring += ','
        evalstring += 'c_int(numPredict)'
    else:
        numPredict = 0
    if not (outFreeForecast is None):
        evalstring += ','
        evalstring += repr(IMSLS_OUT_FREE_FORECAST)
        checkForList(outFreeForecast, 'outFreeForecast')
        evalstring += ','
        outFreeForecast_outFreeForecast_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(outFreeForecast_outFreeForecast_tmp)'
    if not (outlierForecast is None):
        evalstring += ','
        evalstring += repr(IMSLS_OUTLIER_FORECAST)
        checkForList(outlierForecast, 'outlierForecast')
        evalstring += ','
        outlierForecast_outlierForecast_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(outlierForecast_outlierForecast_tmp)'
    if not (supplyWorkArrays is None):
        evalstring += ','
        evalstring += repr(IMSLS_SUPPLY_WORK_ARRAYS)
        checkForDict(supplyWorkArrays, 'supplyWorkArrays', ['iwork', 'work'])
        evalstring += ','
        supplyWorkArrays_iwork_tmp = supplyWorkArrays['iwork']
        supplyWorkArrays_iwork_tmp = toNumpyArray(
            supplyWorkArrays_iwork_tmp, 'iwork', shape=shape, dtype='int', expectedShape=(0))
        supplyWorkArrays_liwork_tmp = shape[0]
        evalstring += 'c_int(supplyWorkArrays_liwork_tmp)'
        evalstring += ','
        evalstring += 'supplyWorkArrays_iwork_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        supplyWorkArrays_work_tmp = supplyWorkArrays['work']
        supplyWorkArrays_work_tmp = toNumpyArray(
            supplyWorkArrays_work_tmp, 'work', shape=shape, dtype='double', expectedShape=(0))
        supplyWorkArrays_lwork_tmp = shape[0]
        evalstring += 'c_int(supplyWorkArrays_lwork_tmp)'
        evalstring += ','
        evalstring += 'supplyWorkArrays_work_tmp.ctypes.data_as(c_void_p)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (model is None):
        processRet(model_model_tmp, shape=(4), pyvar=model)
    if not (residual is None):
        processRet(residual_residual_tmp, shape=(
            tpoints[nObs - 1] - tpoints[0] + 1), pyvar=residual)
    if not (residualSigma is None):
        processRet(residualSigma_residualSigma_tmp,
                   shape=1, pyvar=residualSigma)
    if not (numOutliers is None):
        processRet(numOutliers_numOutliers_tmp, shape=1, pyvar=numOutliers)
    if not (outlierStatistics is None):
        processRet(outlierStatistics_outlierStatistics_tmp, shape=(
            numOutliers_numOutliers_tmp, 2), pyvar=outlierStatistics)
    if not (aic is None):
        processRet(aic_aic_tmp, shape=1, pyvar=aic)
    if not (aicc is None):
        processRet(aicc_aicc_tmp, shape=1, pyvar=aicc)
    if not (bic is None):
        processRet(bic_bic_tmp, shape=1, pyvar=bic)
    if not (outFreeSeries is None):
        processRet(outFreeSeries_outFreeSeries_tmp, shape=(
            tpoints[nObs - 1] - tpoints[0] + 1, 2), pyvar=outFreeSeries)
    if not (outFreeForecast is None):
        processRet(outFreeForecast_outFreeForecast_tmp,
                   shape=(numPredict, 3), pyvar=outFreeForecast)
    if not (outlierForecast is None):
        processRet(outlierForecast_outlierForecast_tmp,
                   shape=(numPredict, 3), pyvar=outlierForecast)
    if not (supplyWorkArrays is None):
        processRet(supplyWorkArrays_iwork_tmp, shape=(
            supplyWorkArrays_liwork_tmp), key='iwork', inout=True, pyvar=supplyWorkArrays)
        processRet(supplyWorkArrays_work_tmp, shape=(
            supplyWorkArrays_lwork_tmp), key='work', inout=True, pyvar=supplyWorkArrays)
    return processRet(result, shape=(1 + model_model_tmp[0] + model_model_tmp[1]), result=True)
