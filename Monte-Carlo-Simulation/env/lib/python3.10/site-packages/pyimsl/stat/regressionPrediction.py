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
from numpy import double, dtype, int, shape, size
from ctypes import POINTER, byref, c_double, c_int, c_void_p
from .statStructs import Imsls_d_regression

IMSLS_X_COL_DIM = 15470
IMSLS_Y_COL_DIM = 15540
IMSLS_INDEX_REGRESSION = 20941
IMSLS_X_INDICES = 20443
IMSLS_WEIGHTS = 15400
IMSLS_CONFIDENCE = 10860
IMSLS_SCHEFFE_CI = 14420
IMSLS_POINTWISE_CI_POP_MEAN = 13820
IMSLS_POINTWISE_CI_NEW_SAMPLE = 13800
IMSLS_LEVERAGE = 12740
IMSLS_Y = 15535
IMSLS_RESIDUAL = 14190
IMSLS_STANDARDIZED_RESIDUAL = 14750
IMSLS_DELETED_RESIDUAL = 11150
IMSLS_COOKSD = 11000
IMSLS_DFFITS = 11190
imslstat = loadimsl(STAT)


def regressionPrediction(regressionInfo, x, xColDim=None, yColDim=None, indexRegression=None, xIndices=None, weights=None, confidence=None, scheffeCi=None, pointwiseCiPopMean=None, pointwiseCiNewSample=None, leverage=None, y=None, residual=None, standardizedResidual=None, deletedResidual=None, cooksd=None, dffits=None):
    """ Computes predicted values, confidence intervals, and diagnostics after fitting a regression model.
    """
    imslstat.imsls_d_regression_prediction.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_regression_prediction('
    evalstring += 'regressionInfo'
    evalstring += ','
    evalstring += 'c_int(nPredict)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nPredict = shape[0]
    if not (xColDim is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(xColDim)'
    if not (yColDim is None):
        evalstring += ','
        evalstring += repr(IMSLS_Y_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(yColDim)'
    if not (indexRegression is None):
        evalstring += ','
        evalstring += repr(IMSLS_INDEX_REGRESSION)
        evalstring += ','
        evalstring += 'c_int(indexRegression)'
    if not (xIndices is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_INDICES)
        checkForDict(xIndices, 'xIndices', ['indind', 'inddep', 'ifrq', 'iwt'])
        evalstring += ','
        xIndices_indind_tmp = xIndices['indind']
        xIndices_indind_tmp = toNumpyArray(
            xIndices_indind_tmp, 'indind', shape=shape, dtype='int')
        evalstring += 'xIndices_indind_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        xIndices_inddep_tmp = xIndices['inddep']
        xIndices_inddep_tmp = toNumpyArray(
            xIndices_inddep_tmp, 'inddep', shape=shape, dtype='int')
        evalstring += 'xIndices_inddep_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        xIndices_ifrq_tmp = xIndices['ifrq']
        evalstring += 'c_int(xIndices_ifrq_tmp)'
        evalstring += ','
        xIndices_iwt_tmp = xIndices['iwt']
        evalstring += 'c_int(xIndices_iwt_tmp)'
    if not (weights is None):
        evalstring += ','
        evalstring += repr(IMSLS_WEIGHTS)
        evalstring += ','
        weights = toNumpyArray(
            weights, 'weights', shape=shape, dtype='double', expectedShape=(nPredict))
        evalstring += 'weights.ctypes.data_as(c_void_p)'
    if not (confidence is None):
        evalstring += ','
        evalstring += repr(IMSLS_CONFIDENCE)
        evalstring += ','
        evalstring += 'c_double(confidence)'
    if not (scheffeCi is None):
        evalstring += ','
        evalstring += repr(IMSLS_SCHEFFE_CI)
        checkForDict(scheffeCi, 'scheffeCi', [])
        evalstring += ','
        scheffeCi_lowerLimit_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(scheffeCi_lowerLimit_tmp)'
        evalstring += ','
        scheffeCi_upperLimit_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(scheffeCi_upperLimit_tmp)'
    if not (pointwiseCiPopMean is None):
        evalstring += ','
        evalstring += repr(IMSLS_POINTWISE_CI_POP_MEAN)
        checkForDict(pointwiseCiPopMean, 'pointwiseCiPopMean', [])
        evalstring += ','
        pointwiseCiPopMean_lowerLimit_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(pointwiseCiPopMean_lowerLimit_tmp)'
        evalstring += ','
        pointwiseCiPopMean_upperLimit_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(pointwiseCiPopMean_upperLimit_tmp)'
    if not (pointwiseCiNewSample is None):
        evalstring += ','
        evalstring += repr(IMSLS_POINTWISE_CI_NEW_SAMPLE)
        checkForDict(pointwiseCiNewSample, 'pointwiseCiNewSample', [])
        evalstring += ','
        pointwiseCiNewSample_lowerLimit_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(pointwiseCiNewSample_lowerLimit_tmp)'
        evalstring += ','
        pointwiseCiNewSample_upperLimit_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(pointwiseCiNewSample_upperLimit_tmp)'
    if not (leverage is None):
        evalstring += ','
        evalstring += repr(IMSLS_LEVERAGE)
        checkForList(leverage, 'leverage')
        evalstring += ','
        leverage_leverage_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(leverage_leverage_tmp)'
    if not (y is None):
        evalstring += ','
        evalstring += repr(IMSLS_Y)
        evalstring += ','
        y = toNumpyArray(y, 'y', shape=shape, dtype='double',
                         expectedShape=(nPredict))
        evalstring += 'y.ctypes.data_as(c_void_p)'
    if not (residual is None):
        evalstring += ','
        evalstring += repr(IMSLS_RESIDUAL)
        checkForList(residual, 'residual')
        evalstring += ','
        residual_residual_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(residual_residual_tmp)'
    if not (standardizedResidual is None):
        evalstring += ','
        evalstring += repr(IMSLS_STANDARDIZED_RESIDUAL)
        checkForList(standardizedResidual, 'standardizedResidual')
        evalstring += ','
        standardizedResidual_standardizedResidual_tmp = POINTER(
            c_double)(c_double())
        evalstring += 'byref(standardizedResidual_standardizedResidual_tmp)'
    if not (deletedResidual is None):
        evalstring += ','
        evalstring += repr(IMSLS_DELETED_RESIDUAL)
        checkForList(deletedResidual, 'deletedResidual')
        evalstring += ','
        deletedResidual_deletedResidual_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(deletedResidual_deletedResidual_tmp)'
    if not (cooksd is None):
        evalstring += ','
        evalstring += repr(IMSLS_COOKSD)
        checkForList(cooksd, 'cooksd')
        evalstring += ','
        cooksd_cooksd_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(cooksd_cooksd_tmp)'
    if not (dffits is None):
        evalstring += ','
        evalstring += repr(IMSLS_DFFITS)
        checkForList(dffits, 'dffits')
        evalstring += ','
        dffits_dffits_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(dffits_dffits_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (scheffeCi is None):
        processRet(scheffeCi_lowerLimit_tmp, shape=(
            nPredict), key='lowerLimit', pyvar=scheffeCi)
        processRet(scheffeCi_upperLimit_tmp, shape=(
            nPredict), key='upperLimit', pyvar=scheffeCi)
    if not (pointwiseCiPopMean is None):
        processRet(pointwiseCiPopMean_lowerLimit_tmp, shape=(
            nPredict), key='lowerLimit', pyvar=pointwiseCiPopMean)
        processRet(pointwiseCiPopMean_upperLimit_tmp, shape=(
            nPredict), key='upperLimit', pyvar=pointwiseCiPopMean)
    if not (pointwiseCiNewSample is None):
        processRet(pointwiseCiNewSample_lowerLimit_tmp, shape=(
            nPredict), key='lowerLimit', pyvar=pointwiseCiNewSample)
        processRet(pointwiseCiNewSample_upperLimit_tmp, shape=(
            nPredict), key='upperLimit', pyvar=pointwiseCiNewSample)
    if not (leverage is None):
        processRet(leverage_leverage_tmp, shape=(nPredict), pyvar=leverage)
    if not (residual is None):
        processRet(residual_residual_tmp, shape=(nPredict), pyvar=residual)
    if not (standardizedResidual is None):
        processRet(standardizedResidual_standardizedResidual_tmp,
                   shape=(nPredict), pyvar=standardizedResidual)
    if not (deletedResidual is None):
        processRet(deletedResidual_deletedResidual_tmp,
                   shape=(nPredict), pyvar=deletedResidual)
    if not (cooksd is None):
        processRet(cooksd_cooksd_tmp, shape=(nPredict), pyvar=cooksd)
    if not (dffits is None):
        processRet(dffits_dffits_tmp, shape=(nPredict), pyvar=dffits)
    return processRet(result, shape=(nPredict), result=True)
