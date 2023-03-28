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
from numpy import cov, double, dtype, int, shape, size, empty
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSLS_X_COL_DIM = 15470
IMSLS_WEIGHTS = 15400
IMSLS_FREQUENCIES = 11790
IMSLS_FIRST_STEP = 11630
IMSLS_INTERMEDIATE_STEP = 12410
IMSLS_LAST_STEP = 12680
IMSLS_ALL_STEPS = 10060
IMSLS_N_STEPS = 13490
IMSLS_FORWARD = 11770
IMSLS_BACKWARD = 10200
IMSLS_STEPWISE = 14860
IMSLS_P_VALUE_IN = 15690
IMSLS_P_VALUE_OUT = 15700
IMSLS_TOLERANCE = 15040
IMSLS_ANOVA_TABLE = 10080
IMSLS_COEF_T_TESTS = 10710
IMSLS_COEF_VIF = 10730
IMSLS_LEVEL = 15680
IMSLS_FORCE = 11760
IMSLS_IEND = 15880
IMSLS_SWEPT_USER = 15890
IMSLS_HISTORY_USER = 15900
IMSLS_COV_SWEPT_USER = 15910
IMSLS_INPUT_COV = 15670
imslstat = loadimsl(STAT)


def regressionStepwise(x, y, xColDim=None, weights=None, frequencies=None, firstStep=None, intermediateStep=None, lastStep=None, allSteps=None, nSteps=None, forward=None, backward=None, stepwise=None, pValueIn=None, pValueOut=None, tolerance=None, anovaTable=None, coefTTests=None, coefVif=None, level=None, force=None, iend=None, sweptUser=None, historyUser=None, covSweptUser=None, inputCov=None):
    """ Builds multiple linear regression models using forward selection, backward selection, or stepwise selection.
    """
    imslstat.imsls_d_regression_stepwise.restype = None
    shape = []
    evalstring = 'imslstat.imsls_d_regression_stepwise('
    evalstring += 'c_int(nRows)'
    evalstring += ','
    evalstring += 'c_int(nCandidate)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nRows = shape[0]
    nCandidate = shape[1]
    evalstring += ','
    y = toNumpyArray(y, 'y', shape=shape, dtype='double',
                     expectedShape=(nRows))
    evalstring += 'y.ctypes.data_as(c_void_p)'
    if not (xColDim is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(xColDim)'
    if not (weights is None):
        evalstring += ','
        evalstring += repr(IMSLS_WEIGHTS)
        evalstring += ','
        weights = toNumpyArray(
            weights, 'weights', shape=shape, dtype='double', expectedShape=(nRows))
        evalstring += 'weights.ctypes.data_as(c_void_p)'
    if not (frequencies is None):
        evalstring += ','
        evalstring += repr(IMSLS_FREQUENCIES)
        evalstring += ','
        frequencies = toNumpyArray(
            frequencies, 'frequencies', shape=shape, dtype='double', expectedShape=(nRows))
        evalstring += 'frequencies.ctypes.data_as(c_void_p)'
    checkForBoolean(firstStep, 'firstStep')
    if (firstStep):
        evalstring += ','
        evalstring += repr(IMSLS_FIRST_STEP)
    checkForBoolean(intermediateStep, 'intermediateStep')
    if (intermediateStep):
        evalstring += ','
        evalstring += repr(IMSLS_INTERMEDIATE_STEP)
    checkForBoolean(lastStep, 'lastStep')
    if (lastStep):
        evalstring += ','
        evalstring += repr(IMSLS_LAST_STEP)
    checkForBoolean(allSteps, 'allSteps')
    if (allSteps):
        evalstring += ','
        evalstring += repr(IMSLS_ALL_STEPS)
    if not (nSteps is None):
        evalstring += ','
        evalstring += repr(IMSLS_N_STEPS)
        evalstring += ','
        evalstring += 'c_int(nSteps)'
    checkForBoolean(forward, 'forward')
    if (forward):
        evalstring += ','
        evalstring += repr(IMSLS_FORWARD)
    checkForBoolean(backward, 'backward')
    if (backward):
        evalstring += ','
        evalstring += repr(IMSLS_BACKWARD)
    checkForBoolean(stepwise, 'stepwise')
    if (stepwise):
        evalstring += ','
        evalstring += repr(IMSLS_STEPWISE)
    if not (pValueIn is None):
        evalstring += ','
        evalstring += repr(IMSLS_P_VALUE_IN)
        evalstring += ','
        evalstring += 'c_double(pValueIn)'
    if not (pValueOut is None):
        evalstring += ','
        evalstring += repr(IMSLS_P_VALUE_OUT)
        evalstring += ','
        evalstring += 'c_double(pValueOut)'
    if not (tolerance is None):
        evalstring += ','
        evalstring += repr(IMSLS_TOLERANCE)
        evalstring += ','
        evalstring += 'c_double(tolerance)'
    if not (anovaTable is None):
        evalstring += ','
        evalstring += repr(IMSLS_ANOVA_TABLE)
        checkForList(anovaTable, 'anovaTable')
        evalstring += ','
        anovaTable_anovaTable_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(anovaTable_anovaTable_tmp)'
    if not (coefTTests is None):
        evalstring += ','
        evalstring += repr(IMSLS_COEF_T_TESTS)
        checkForList(coefTTests, 'coefTTests')
        evalstring += ','
        coefTTests_coefTTests_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(coefTTests_coefTTests_tmp)'
    if not (coefVif is None):
        evalstring += ','
        evalstring += repr(IMSLS_COEF_VIF)
        checkForList(coefVif, 'coefVif')
        evalstring += ','
        coefVif_coefVif_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(coefVif_coefVif_tmp)'
    if not (level is None):
        evalstring += ','
        evalstring += repr(IMSLS_LEVEL)
        evalstring += ','
        level = toNumpyArray(level, 'level', shape=shape,
                             dtype='int', expectedShape=(nCandidate + 1))
        evalstring += 'level.ctypes.data_as(c_void_p)'
    if not (force is None):
        evalstring += ','
        evalstring += repr(IMSLS_FORCE)
        evalstring += ','
        evalstring += 'c_int(force)'
    if not (iend is None):
        evalstring += ','
        evalstring += repr(IMSLS_IEND)
        checkForList(iend, 'iend')
        evalstring += ','
        iend_iend_tmp = c_int()
        evalstring += 'byref(iend_iend_tmp)'
    if not (sweptUser is None):
        evalstring += ','
        evalstring += repr(IMSLS_SWEPT_USER)
        checkForList(sweptUser, 'sweptUser')
        evalstring += ','
        # sweptUser_swept_tmp = toNumpyArray(sweptUser, 'sweptUser', shape=shape, dtype='int', expectedShape=(nCandidate+1))
        # Not sure why we cant just use empty to create numpy but somewhow does not work right for int so we use toNumpyArray
        sweptUser_swept_tmp = empty(nCandidate + 1, dtype='int')
        sweptUser_swept_tmp = toNumpyArray(
            sweptUser_swept_tmp, 'sweptUser', shape=shape, dtype='int', expectedShape=(nCandidate + 1))
        evalstring += 'sweptUser_swept_tmp.ctypes.data_as(c_void_p)'
    if not (historyUser is None):
        evalstring += ','
        evalstring += repr(IMSLS_HISTORY_USER)
        checkForList(historyUser, 'historyUser')
        evalstring += ','
        # historyUser_history_tmp = toNumpyArray(historyUser, 'historyUser', shape=shape, dtype='double', expectedShape=(nCandidate+1))
        historyUser_history_tmp = empty(nCandidate + 1, dtype='double')
        evalstring += 'historyUser_history_tmp.ctypes.data_as(c_void_p)'
    if not (covSweptUser is None):
        evalstring += ','
        evalstring += repr(IMSLS_COV_SWEPT_USER)
        checkForList(covSweptUser, 'covSweptUser')
        evalstring += ','
        # covSweptUser_covs_tmp = toNumpyArray(covSweptUser, 'covSweptUser', shape=shape, dtype='double', expectedShape=((nCandidate+1),(nCandidate+1)))
        covSweptUser_covs_tmp = empty(
            (nCandidate + 1) * (nCandidate + 1), dtype='double')
        evalstring += 'covSweptUser_covs_tmp.ctypes.data_as(c_void_p)'
    if not (inputCov is None):
        evalstring += ','
        evalstring += repr(IMSLS_INPUT_COV)
        checkForDict(inputCov, 'inputCov', ['nObservations', 'cov'])
        evalstring += ','
        inputCov_nObservations_tmp = inputCov['nObservations']
        evalstring += 'c_int(inputCov_nObservations_tmp)'
        evalstring += ','
        inputCov_cov_tmp = inputCov['cov']
        inputCov_cov_tmp = toNumpyArray(
            inputCov_cov_tmp, 'cov', shape=shape, dtype='double', expectedShape=(nCandidate + 1, nCandidate + 1))
        evalstring += 'inputCov_cov_tmp.ctypes.data_as(c_void_p)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (anovaTable is None):
        processRet(anovaTable_anovaTable_tmp, shape=(13), pyvar=anovaTable)
    if not (coefTTests is None):
        processRet(coefTTests_coefTTests_tmp, shape=(
            nCandidate, 4), pyvar=coefTTests)
    if not (coefVif is None):
        processRet(coefVif_coefVif_tmp, shape=(nCandidate), pyvar=coefVif)
    if not (iend is None):
        processRet(iend_iend_tmp, shape=(1), pyvar=iend)
    if not (sweptUser is None):
        processRet(sweptUser_swept_tmp, shape=(
            nCandidate + 1), pyvar=sweptUser)
    if not (historyUser is None):
        processRet(historyUser_history_tmp, shape=(
            nCandidate + 1), pyvar=historyUser)
    if not (covSweptUser is None):
        processRet(covSweptUser_covs_tmp, shape=(
            (nCandidate + 1), (nCandidate + 1)), pyvar=covSweptUser)
    return
