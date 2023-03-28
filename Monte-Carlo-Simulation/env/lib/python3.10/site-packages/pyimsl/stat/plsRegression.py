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
from numpy import array, empty, double
from ctypes import *

IMSLS_N_OBSERVATIONS = 15640
IMSLS_Y_INDICES = 50807
IMSLS_X_INDICES = 20443
IMSLS_N_COMPONENTS = 50806
IMSLS_CROSS_VALIDATION = 50805
IMSLS_N_FOLD = 50804
IMSLS_SCALE = 14400
IMSLS_PRINT_LEVEL = 20530
IMSLS_PREDICTED = 16079
IMSLS_RESIDUALS = 25570
IMSLS_STD_ERRORS = 40120
IMSLS_PRESS = 50802
IMSLS_X_SCORES = 50800
IMSLS_Y_SCORES = 50798
IMSLS_X_LOADINGS = 50796
IMSLS_Y_LOADINGS = 50794
IMSLS_WEIGHTS = 15400
imslstat = loadimsl(STAT)


def plsRegression(y, x, nObservations=None, yIndices=None, xIndices=None, nComponents=None, crossValidation=None, nFold=None, scale=None, printLevel=None, predicted=None, residuals=None, stdErrors=None, press=None, xScores=None, yScores=None, xLoadings=None, yLoadings=None, weights=None):
    imslstat.imsls_d_pls_regression.restype = POINTER(c_double)
    """ Performs partial least squares (PLS) regression for one or more response variables
        and one or more predictor variables.
    """
    shape = []
    evalstring = 'imslstat.imsls_d_pls_regression('
    evalstring += 'c_int(ny)'
    evalstring += ','
    evalstring += 'c_int(h)'
    evalstring += ','
    y = toNumpyArray(y, 'y', shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'y.ctypes.data_as(c_void_p)'
    ny = shape[0]
    h = shape[1]
    evalstring += ','
    evalstring += 'c_int(nx)'
    evalstring += ','
    evalstring += 'c_int(p)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nx = shape[0]
    p = shape[1]
    nobs = min(ny, nx)  # custom code
    xIndices_ix_tmp = p  # custom
    yIndices_iy_tmp = h  # custom
    ncomps = xIndices_ix_tmp  # custom
    if not (nObservations is None):
        evalstring += ','
        evalstring += repr(IMSLS_N_OBSERVATIONS)
        evalstring += ','
        evalstring += 'c_int(nObservations)'
        nobs = nObservations  # custom
    if not (yIndices is None):
        evalstring += ','
        evalstring += repr(IMSLS_Y_INDICES)
        evalstring += ','
        evalstring += 'c_int(yIndices_iy_tmp)'
        evalstring += ','
        yIndices_iyind_tmp = toNumpyArray(
            yIndices, 'yIndices', shape=shape, dtype='int', expectedShape=(0))
        evalstring += 'yIndices_iyind_tmp.ctypes.data_as(c_void_p)'
        yIndices_iy_tmp = shape[0]
    if not (xIndices is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_INDICES)
        evalstring += ','
        evalstring += 'c_int(xIndices_ix_tmp)'
        evalstring += ','
        xIndices_ixind_tmp = toNumpyArray(
            xIndices, 'xIndices', shape=shape, dtype='int', expectedShape=(0))
        evalstring += 'xIndices_ixind_tmp.ctypes.data_as(c_void_p)'
        xIndices_ix_tmp = shape[0]
        ncomps = xIndices_ix_tmp  # custom
    if not (nComponents is None):
        evalstring += ','
        evalstring += repr(IMSLS_N_COMPONENTS)
        evalstring += ','
        evalstring += 'c_int(nComponents)'

    if not (crossValidation is None):
        evalstring += ','
        evalstring += repr(IMSLS_CROSS_VALIDATION)
        evalstring += ','
        evalstring += 'c_int(crossValidation)'
    if not (nFold is None):
        evalstring += ','
        evalstring += repr(IMSLS_N_FOLD)
        evalstring += ','
        evalstring += 'c_int(nFold)'
    if not (scale is None):
        evalstring += ','
        evalstring += repr(IMSLS_SCALE)
        evalstring += ','
        evalstring += 'c_int(scale)'
    if not (printLevel is None):
        evalstring += ','
        evalstring += repr(IMSLS_PRINT_LEVEL)
        evalstring += ','
        evalstring += 'c_int(printLevel)'
    if not (predicted is None):
        evalstring += ','
        evalstring += repr(IMSLS_PREDICTED)
        checkForList(predicted, 'predicted')
        evalstring += ','
        predicted_yhat_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(predicted_yhat_tmp)'
    if not (residuals is None):
        evalstring += ','
        evalstring += repr(IMSLS_RESIDUALS)
        checkForList(residuals, 'residuals')
        evalstring += ','
        residuals_resids_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(residuals_resids_tmp)'
    if not (stdErrors is None):
        evalstring += ','
        evalstring += repr(IMSLS_STD_ERRORS)
        checkForList(stdErrors, 'stdErrors')
        evalstring += ','
        stdErrors_se_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(stdErrors_se_tmp)'
    if not (press is None):
        evalstring += ','
        evalstring += repr(IMSLS_PRESS)
        checkForList(press, 'press')
        evalstring += ','
        press_press_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(press_press_tmp)'
    if not (xScores is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_SCORES)
        checkForList(xScores, 'xScores')
        evalstring += ','
        xScores_xscrs_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(xScores_xscrs_tmp)'
    if not (yScores is None):
        evalstring += ','
        evalstring += repr(IMSLS_Y_SCORES)
        checkForList(yScores, 'yScores')
        evalstring += ','
        yScores_yscrs_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(yScores_yscrs_tmp)'
    if not (xLoadings is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_LOADINGS)
        checkForList(xLoadings, 'xLoadings')
        evalstring += ','
        xLoadings_xldgs_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(xLoadings_xldgs_tmp)'
    if not (yLoadings is None):
        evalstring += ','
        evalstring += repr(IMSLS_Y_LOADINGS)
        checkForList(yLoadings, 'yLoadings')
        evalstring += ','
        yLoadings_yldgs_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(yLoadings_yldgs_tmp)'
    if not (weights is None):
        evalstring += ','
        evalstring += repr(IMSLS_WEIGHTS)
        checkForList(weights, 'weights')
        evalstring += ','
        weights_xldgs_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(weights_xldgs_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (predicted is None):
        processRet(predicted_yhat_tmp, shape=(
            nobs, yIndices_iy_tmp), pyvar=predicted)
    if not (residuals is None):
        processRet(residuals_resids_tmp, shape=(
            nobs, yIndices_iy_tmp), pyvar=residuals)
    if not (stdErrors is None):
        processRet(stdErrors_se_tmp, shape=(
            xIndices_ix_tmp, yIndices_iy_tmp), pyvar=stdErrors)
    if not (press is None):
        processRet(press_press_tmp, shape=(
            ncomps, yIndices_iy_tmp), pyvar=press)
    if not (xScores is None):
        processRet(xScores_xscrs_tmp, shape=(nobs, ncomps), pyvar=xScores)
    if not (yScores is None):
        processRet(yScores_yscrs_tmp, shape=(nobs, ncomps), pyvar=yScores)
    if not (xLoadings is None):
        processRet(xLoadings_xldgs_tmp, shape=(
            xIndices_ix_tmp, ncomps), pyvar=xLoadings)
    if not (yLoadings is None):
        processRet(yLoadings_yldgs_tmp, shape=(
            yIndices_iy_tmp, ncomps), pyvar=yLoadings)
    if not (weights is None):
        processRet(weights_xldgs_tmp, shape=(
            xIndices_ix_tmp, ncomps), pyvar=weights)
    # custom
    return processRet(result, shape=(xIndices_ix_tmp, yIndices_iy_tmp), result=True)
