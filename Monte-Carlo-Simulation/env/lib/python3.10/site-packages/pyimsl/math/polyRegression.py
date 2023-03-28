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
from pyimsl.util.imslUtils import MATH, checkForList, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, shape
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSL_WEIGHTS = 10141
IMSL_SSQ_POLY = 10156
IMSL_SSQ_POLY_COL_DIM = 10265
IMSL_SSQ_LOF = 10157
IMSL_SSQ_LOF_COL_DIM = 10267
IMSL_X_MEAN = 10158
IMSL_X_VARIANCE = 10160
IMSL_ANOVA_TABLE = 10051
IMSL_DF_PURE_ERROR = 10262
IMSL_SSQ_PURE_ERROR = 10263
IMSL_RESIDUAL = 10172
imslmath = loadimsl(MATH)


def polyRegression(xdata, ydata, degree, weights=None, ssqPoly=None, ssqPolyColDim=None, ssqLof=None, ssqLofColDim=None, xMean=None, xVariance=None, anovaTable=None, dfPureError=None, ssqPureError=None, residual=None):
    """ Performs a polynomial least-squares regression.
    """
    imslmath.imsl_d_poly_regression.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslmath.imsl_d_poly_regression('
    evalstring += 'c_int(nObservations)'
    evalstring += ','
    xdata = toNumpyArray(xdata, 'xdata', shape=shape,
                         dtype='double', expectedShape=(0))
    evalstring += 'xdata.ctypes.data_as(c_void_p)'
    nObservations = shape[0]
    evalstring += ','
    ydata = toNumpyArray(ydata, 'ydata', shape=shape,
                         dtype='double', expectedShape=(nObservations))
    evalstring += 'ydata.ctypes.data_as(c_void_p)'
    evalstring += ','
    evalstring += 'c_int(degree)'
    if not (weights is None):
        evalstring += ','
        evalstring += repr(IMSL_WEIGHTS)
        evalstring += ','
        weights = toNumpyArray(
            weights, 'weights', shape=shape, dtype='double', expectedShape=(nObservations))
        evalstring += 'weights.ctypes.data_as(c_void_p)'
    if not (ssqPoly is None):
        evalstring += ','
        evalstring += repr(IMSL_SSQ_POLY)
        checkForList(ssqPoly, 'ssqPoly')
        evalstring += ','
        ssqPoly_pSsqPoly_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(ssqPoly_pSsqPoly_tmp)'
    if not (ssqPolyColDim is None):
        evalstring += ','
        evalstring += repr(IMSL_SSQ_POLY_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(ssqPolyColDim)'
    if not (ssqLof is None):
        evalstring += ','
        evalstring += repr(IMSL_SSQ_LOF)
        checkForList(ssqLof, 'ssqLof')
        evalstring += ','
        ssqLof_pSsqLof_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(ssqLof_pSsqLof_tmp)'
    if not (ssqLofColDim is None):
        evalstring += ','
        evalstring += repr(IMSL_SSQ_LOF_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(ssqLofColDim)'
    if not (xMean is None):
        evalstring += ','
        evalstring += repr(IMSL_X_MEAN)
        checkForList(xMean, 'xMean')
        evalstring += ','
        xMean_xMean_tmp = c_double()
        evalstring += 'byref(xMean_xMean_tmp)'
    if not (xVariance is None):
        evalstring += ','
        evalstring += repr(IMSL_X_VARIANCE)
        checkForList(xVariance, 'xVariance')
        evalstring += ','
        xVariance_xVariance_tmp = c_double()
        evalstring += 'byref(xVariance_xVariance_tmp)'
    if not (anovaTable is None):
        evalstring += ','
        evalstring += repr(IMSL_ANOVA_TABLE)
        checkForList(anovaTable, 'anovaTable')
        evalstring += ','
        anovaTable_pAnovaTable_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(anovaTable_pAnovaTable_tmp)'
    if not (dfPureError is None):
        evalstring += ','
        evalstring += repr(IMSL_DF_PURE_ERROR)
        checkForList(dfPureError, 'dfPureError')
        evalstring += ','
        dfPureError_dfPureError_tmp = c_int()
        evalstring += 'byref(dfPureError_dfPureError_tmp)'
    if not (ssqPureError is None):
        evalstring += ','
        evalstring += repr(IMSL_SSQ_PURE_ERROR)
        checkForList(ssqPureError, 'ssqPureError')
        evalstring += ','
        ssqPureError_ssqPureError_tmp = c_double()
        evalstring += 'byref(ssqPureError_ssqPureError_tmp)'
    if not (residual is None):
        evalstring += ','
        evalstring += repr(IMSL_RESIDUAL)
        checkForList(residual, 'residual')
        evalstring += ','
        residual_pResidual_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(residual_pResidual_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (ssqPoly is None):
        processRet(ssqPoly_pSsqPoly_tmp, shape=(degree, 4), pyvar=ssqPoly)
    if not (ssqLof is None):
        processRet(ssqLof_pSsqLof_tmp, shape=(degree, 4), pyvar=ssqLof)
    if not (xMean is None):
        processRet(xMean_xMean_tmp, shape=1, pyvar=xMean)
    if not (xVariance is None):
        processRet(xVariance_xVariance_tmp, shape=1, pyvar=xVariance)
    if not (anovaTable is None):
        processRet(anovaTable_pAnovaTable_tmp, shape=(15), pyvar=anovaTable)
    if not (dfPureError is None):
        processRet(dfPureError_dfPureError_tmp, shape=1, pyvar=dfPureError)
    if not (ssqPureError is None):
        processRet(ssqPureError_ssqPureError_tmp, shape=1, pyvar=ssqPureError)
    if not (residual is None):
        processRet(residual_pResidual_tmp, shape=(
            nObservations), pyvar=residual)
    return processRet(result, shape=(degree + 1), result=True)
