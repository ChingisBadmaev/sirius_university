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
from .statStructs import Imsls_d_regression
from .statStructs import Imsls_d_regression
from .statStructs import d_complex
from .statStructs import d_complex

IMSLS_MA_LAG = 51000
IMSLS_A0 = 51010
IMSLS_AR_MODEL = 50896
IMSLS_MA_MODEL = 51001
IMSLS_AR_CONSTANTS = 51004
IMSLS_MA_CONSTANTS = 51003
IMSLS_PRESAMPLE = 51002
IMSLS_MAX_LAG = 25160
IMSLS_N_STEPS = 13490
IMSLS_MAX_ITERATIONS = 12970
IMSLS_TOLERANCE = 15040
IMSLS_TREND = 50780
IMSLS_SCALE = 14400
IMSLS_CENTER = 25390
IMSLS_X_DATA = 51007
IMSLS_ERROR_CORRECTION = 51005
IMSLS_CAUSALITY = 51006
IMSLS_CAUSALITY_STATS = 51019
IMSLS_VAR_INFO = 51011
IMSLS_VARMA_INFO = 51012
IMSLS_UNIT_ROOT = 51008
IMSLS_VECM_COEF = 51013
IMSLS_VECM_EIGENVALUES = 51017
IMSLS_VECM_ALPHABETA = 51015
IMSLS_FORECASTS = 25730
IMSLS_CRITERIA = 50915
IMSLS_LOG_LIKELIHOOD = 50180
imslstat = loadimsl(STAT)


def vectorAutoregression(y, p, maLag=None, a0=None, arModel=None, maModel=None, arConstants=None, maConstants=None, presample=None, maxLag=None, nSteps=None, maxIterations=None, tolerance=None, trend=None, scale=None, center=None, xData=None, errorCorrection=None, causality=None, causalityStats=None, varInfo=None, varmaInfo=None, unitRoot=None, vecmCoef=None, vecmEigenvalues=None, vecmAlphabeta=None, forecasts=None, criteria=None, logLikelihood=None):
    """ Estimates a vector auto-regressive time series model with optional moving average components.
    """
    imslstat.imsls_d_vector_autoregression.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_vector_autoregression('
    evalstring += 'c_int(nObs)'
    evalstring += ','
    evalstring += 'c_int(nCols)'
    evalstring += ','
    y = toNumpyArray(y, 'y', shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'y.ctypes.data_as(c_void_p)'
    nObs = shape[0]
    nCols = shape[1]
    evalstring += ','
    evalstring += 'c_int(p)'
    # custom code: need a default value for q.
    q = 0
    if not (maLag is None):
        evalstring += ','
        evalstring += repr(IMSLS_MA_LAG)
        evalstring += ','
        evalstring += 'c_int(maLag)'
        q = maLag
    checkForBoolean(a0, 'a0')
    if (a0):
        evalstring += ','
        evalstring += repr(IMSLS_A0)
        # custom code: need to use A0_flag when determining length of result.
        A0_flag = 1
    else:
        A0_flag = 0
    if not (arModel is None):
        evalstring += ','
        evalstring += repr(IMSLS_AR_MODEL)
        evalstring += ','
        # custom code: introduce use of A0_flag for length.
        arModel = toNumpyArray(arModel, 'arModel', shape=shape,
                               dtype='int', expectedShape=nCols * nCols * (p + A0_flag))
        evalstring += 'arModel.ctypes.data_as(c_void_p)'
    if not (maModel is None):
        evalstring += ','
        evalstring += repr(IMSLS_MA_MODEL)
        evalstring += ','
        # custom code: introduce use of A0_flag for length.
        maModel = toNumpyArray(maModel, 'maModel', shape=shape,
                               dtype='int', expectedShape=nCols * nCols * (q + A0_flag))
        evalstring += 'maModel.ctypes.data_as(c_void_p)'
    if not (arConstants is None):
        evalstring += ','
        evalstring += repr(IMSLS_AR_CONSTANTS)
        evalstring += ','
        # custom code: introduce use of A0_flag for length.
        arConstants = toNumpyArray(arConstants, 'arConstants', shape=shape,
                                   dtype='double', expectedShape=nCols * nCols * (p + A0_flag))
        evalstring += 'arConstants.ctypes.data_as(c_void_p)'
    if not (maConstants is None):
        evalstring += ','
        evalstring += repr(IMSLS_MA_CONSTANTS)
        evalstring += ','
        # custom code: introduce use of A0_flag for length.
        maConstants = toNumpyArray(maConstants, 'maConstants', shape=shape,
                                   dtype='double', expectedShape=nCols * nCols * (q + A0_flag))
        evalstring += 'maConstants.ctypes.data_as(c_void_p)'
    if not (presample is None):
        evalstring += ','
        evalstring += repr(IMSLS_PRESAMPLE)
        evalstring += ','
        evalstring += 'c_int(presample)'
    if not (maxLag is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_LAG)
        evalstring += ','
        evalstring += 'c_int(maxLag)'
    if not (nSteps is None):
        evalstring += ','
        evalstring += repr(IMSLS_N_STEPS)
        evalstring += ','
        evalstring += 'c_int(nSteps)'
        # custom code: need to set a default value of maxSteps.
        maxSteps = nSteps
    else:
        maxSteps = 4
    if not (maxIterations is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_ITERATIONS)
        evalstring += ','
        evalstring += 'c_int(maxIterations)'
    if not (tolerance is None):
        evalstring += ','
        evalstring += repr(IMSLS_TOLERANCE)
        evalstring += ','
        evalstring += 'c_double(tolerance)'
    checkForBoolean(trend, 'trend')
    if (trend):
        evalstring += ','
        evalstring += repr(IMSLS_TREND)
        # custom code: need to set a default value of trend.
        trend = 1
    else:
        trend = 0
    checkForBoolean(scale, 'scale')
    if (scale):
        evalstring += ','
        evalstring += repr(IMSLS_SCALE)
    checkForBoolean(center, 'center')
    if (center):
        evalstring += ','
        evalstring += repr(IMSLS_CENTER)
    if not (xData is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_DATA)
        evalstring += ','
        evalstring += 'c_int(xData_nXvars_tmp)'
        evalstring += ','
        xData_x_tmp = toNumpyArray(
            xData, 'xData', shape=shape, dtype='double', expectedShape=(nObs, 0))
        evalstring += 'xData_x_tmp.ctypes.data_as(c_void_p)'
        xData_nXvars_tmp = shape[1]
    else:
        xData_nXvars_tmp = 0
    if not (errorCorrection is None):
        evalstring += ','
        evalstring += repr(IMSLS_ERROR_CORRECTION)
        evalstring += ','
        evalstring += 'c_int(errorCorrection)'
        # custom code: introduce irank to be used for some array sizes
        irank = c_int(errorCorrection)
    else:
        irank = 0
    if not (causality is None):
        evalstring += ','
        evalstring += repr(IMSLS_CAUSALITY)
        checkForDict(causality, 'causality', ['s1', 's2'])
        evalstring += ','
        evalstring += 'c_int(causality_sizeS1_tmp)'
        evalstring += ','
        causality_s1_tmp = causality['s1']
        causality_s1_tmp = toNumpyArray(
            causality_s1_tmp, 's1', shape=shape, dtype='double', expectedShape=(0))
        evalstring += 'causality_s1_tmp.ctypes.data_as(c_void_p)'
        causality_sizeS1_tmp = shape[0]
        evalstring += ','
        causality_s2_tmp = causality['s2']
        causality_s2_tmp = toNumpyArray(
            causality_s2_tmp, 's2', shape=shape, dtype='double', expectedShape=(nCols - causality_sizeS1_tmp))
        evalstring += 'causality_s2_tmp.ctypes.data_as(c_void_p)'
    if not (causalityStats is None):
        evalstring += ','
        evalstring += repr(IMSLS_CAUSALITY_STATS)
        checkForList(causalityStats, 'causalityStats')
        evalstring += ','
        causalityStats_stats_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(causalityStats_stats_tmp)'
    if not (varInfo is None):
        evalstring += ','
        evalstring += repr(IMSLS_VAR_INFO)
        checkForList(varInfo, 'varInfo')
        evalstring += ','
        varInfo_varInfo_tmp = POINTER(Imsls_d_regression)(Imsls_d_regression())
        evalstring += 'byref(varInfo_varInfo_tmp)'
    if not (varmaInfo is None):
        evalstring += ','
        evalstring += repr(IMSLS_VARMA_INFO)
        checkForList(varmaInfo, 'varmaInfo')
        evalstring += ','
        varmaInfo_varmaInfo_tmp = POINTER(
            Imsls_d_regression)(Imsls_d_regression())
        evalstring += 'byref(varmaInfo_varmaInfo_tmp)'
    if not (unitRoot is None):
        evalstring += ','
        evalstring += repr(IMSLS_UNIT_ROOT)
        checkForList(unitRoot, 'unitRoot')
        evalstring += ','
        unitRoot_urEvals_tmp = POINTER(d_complex)(d_complex())
        evalstring += 'byref(unitRoot_urEvals_tmp)'
    if not (vecmCoef is None):
        evalstring += ','
        evalstring += repr(IMSLS_VECM_COEF)
        checkForList(vecmCoef, 'vecmCoef')
        evalstring += ','
        vecmCoef_vecmCoef_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(vecmCoef_vecmCoef_tmp)'
    if not (vecmEigenvalues is None):
        evalstring += ','
        evalstring += repr(IMSLS_VECM_EIGENVALUES)
        checkForList(vecmEigenvalues, 'vecmEigenvalues')
        evalstring += ','
        vecmEigenvalues_vecmEigens_tmp = POINTER(d_complex)(d_complex())
        evalstring += 'byref(vecmEigenvalues_vecmEigens_tmp)'
    if not (vecmAlphabeta is None):
        evalstring += ','
        evalstring += repr(IMSLS_VECM_ALPHABETA)
        checkForList(vecmAlphabeta, 'vecmAlphabeta')
        evalstring += ','
        vecmAlphabeta_vecmAlphabeta_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(vecmAlphabeta_vecmAlphabeta_tmp)'
    if not (forecasts is None):
        evalstring += ','
        evalstring += repr(IMSLS_FORECASTS)
        checkForList(forecasts, 'forecasts')
        evalstring += ','
        forecasts_forecasts_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(forecasts_forecasts_tmp)'
    if not (criteria is None):
        evalstring += ','
        evalstring += repr(IMSLS_CRITERIA)
        checkForList(criteria, 'criteria')
        evalstring += ','
        criteria_criteria_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(criteria_criteria_tmp)'
    if not (logLikelihood is None):
        evalstring += ','
        evalstring += repr(IMSLS_LOG_LIKELIHOOD)
        checkForList(logLikelihood, 'logLikelihood')
        evalstring += ','
        logLikelihood_ll_tmp = c_double()
        evalstring += 'byref(logLikelihood_ll_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (causalityStats is None):
        processRet(causalityStats_stats_tmp, shape=(2), pyvar=causalityStats)
    if not (varInfo is None):
        # processRet(varInfo_varInfo_tmp, shape=(1), pyvar=varInfo)
        varInfo.append(varInfo_varInfo_tmp)
    if not (varmaInfo is None):
        # processRet(varmaInfo_varmaInfo_tmp, shape=(1), pyvar=varmaInfo)
        varmaInfo.append(varmaInfo_varmaInfo_tmp)
    if not (unitRoot is None):
        processRet(unitRoot_urEvals_tmp, shape=(
            nCols, (p + q)), pyvar=unitRoot)
    if not (vecmCoef is None):
        # custom code: introduce use of A0_flag for length.
        processRet(vecmCoef_vecmCoef_tmp, shape=(
            nCols * nCols * (p + q + A0_flag)), pyvar=vecmCoef)
    if not (vecmEigenvalues is None):
        processRet(vecmEigenvalues_vecmEigens_tmp,
                   shape=(nCols), pyvar=vecmEigenvalues)
    if not (vecmAlphabeta is None):
        processRet(vecmAlphabeta_vecmAlphabeta_tmp, shape=(
            2 * nCols * irank), pyvar=vecmAlphabeta)
    if not (forecasts is None):
        processRet(forecasts_forecasts_tmp, shape=(
            nObs * nCols * maxSteps), pyvar=forecasts)
    if not (criteria is None):
        processRet(criteria_criteria_tmp, shape=(4), pyvar=criteria)
    if not (logLikelihood is None):
        processRet(logLikelihood_ll_tmp, shape=(1), pyvar=logLikelihood)
    # custom code: added use of A0_flag based on CNL source code.
    return processRet(result, shape=(nCols * (trend + xData_nXvars_tmp + nCols * (p + q + A0_flag))), result=True)
