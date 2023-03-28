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
from numpy import double, dtype, shape
from ctypes import POINTER, byref, c_double, c_int, c_void_p
from .statStructs import Imsls_d_poly_regression

IMSLS_WEIGHTS = 15400
IMSLS_SSQ_POLY = 14700
IMSLS_SSQ_POLY_COL_DIM = 14710
IMSLS_SSQ_LOF = 14670
IMSLS_SSQ_LOF_COL_DIM = 14680
IMSLS_X_MEAN = 15490
IMSLS_X_VARIANCE = 15520
IMSLS_ANOVA_TABLE = 10080
IMSLS_DF_PURE_ERROR = 11210
IMSLS_SSQ_PURE_ERROR = 14730
IMSLS_RESIDUAL = 14190
IMSLS_POLY_REGRESSION_INFO = 13840
imslstat = loadimsl(STAT)


def polyRegression(x, y, degree, weights=None, ssqPoly=None, ssqPolyColDim=None, ssqLof=None, ssqLofColDim=None, xMean=None, xVariance=None, anovaTable=None, dfPureError=None, ssqPureError=None, residual=None, polyRegressionInfo=None):
    """ Performs a polynomial least-squares regression.
    """
    imslstat.imsls_d_poly_regression.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_poly_regression('
    evalstring += 'c_int(nObservations)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=0)
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nObservations = shape[0]
    evalstring += ','
    y = toNumpyArray(y, 'y', shape=shape, dtype='double',
                     expectedShape=nObservations)
    evalstring += 'y.ctypes.data_as(c_void_p)'
    evalstring += ','
    evalstring += 'c_int(degree)'
    if not (weights is None):
        evalstring += ','
        evalstring += repr(IMSLS_WEIGHTS)
        evalstring += ','
        weights = toNumpyArray(
            weights, 'weights', shape=shape, dtype='double', expectedShape=nObservations)
        evalstring += 'weights.ctypes.data_as(c_void_p)'
    if not (ssqPoly is None):
        evalstring += ','
        evalstring += repr(IMSLS_SSQ_POLY)
        checkForList(ssqPoly, 'ssqPoly')
        evalstring += ','
        ssqPoly_ssqPoly_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(ssqPoly_ssqPoly_tmp)'
    if not (ssqPolyColDim is None):
        evalstring += ','
        evalstring += repr(IMSLS_SSQ_POLY_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(ssqPolyColDim)'
    if not (ssqLof is None):
        evalstring += ','
        evalstring += repr(IMSLS_SSQ_LOF)
        checkForList(ssqLof, 'ssqLof')
        evalstring += ','
        ssqLof_ssqLof_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(ssqLof_ssqLof_tmp)'
    if not (ssqLofColDim is None):
        evalstring += ','
        evalstring += repr(IMSLS_SSQ_LOF_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(ssqLofColDim)'
    if not (xMean is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_MEAN)
        checkForList(xMean, 'xMean')
        evalstring += ','
        xMean_xMean_tmp = c_double()
        evalstring += 'byref(xMean_xMean_tmp)'
    if not (xVariance is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_VARIANCE)
        checkForList(xVariance, 'xVariance')
        evalstring += ','
        xVariance_xVariance_tmp = c_double()
        evalstring += 'byref(xVariance_xVariance_tmp)'
    if not (anovaTable is None):
        evalstring += ','
        evalstring += repr(IMSLS_ANOVA_TABLE)
        checkForList(anovaTable, 'anovaTable')
        evalstring += ','
        anovaTable_anovaTable_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(anovaTable_anovaTable_tmp)'
    if not (dfPureError is None):
        evalstring += ','
        evalstring += repr(IMSLS_DF_PURE_ERROR)
        checkForList(dfPureError, 'dfPureError')
        evalstring += ','
        dfPureError_dfPureError_tmp = c_int()
        evalstring += 'byref(dfPureError_dfPureError_tmp)'
    if not (ssqPureError is None):
        evalstring += ','
        evalstring += repr(IMSLS_SSQ_PURE_ERROR)
        checkForList(ssqPureError, 'ssqPureError')
        evalstring += ','
        ssqPureError_ssqPureError_tmp = c_double()
        evalstring += 'byref(ssqPureError_ssqPureError_tmp)'
    if not (residual is None):
        evalstring += ','
        evalstring += repr(IMSLS_RESIDUAL)
        checkForList(residual, 'residual')
        evalstring += ','
        residual_residual_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(residual_residual_tmp)'
    if not (polyRegressionInfo is None):
        evalstring += ','
        evalstring += repr(IMSLS_POLY_REGRESSION_INFO)
        checkForList(polyRegressionInfo, 'polyRegressionInfo')
        evalstring += ','
        polyRegressionInfo_polyInfo_tmp = POINTER(
            Imsls_d_poly_regression)(Imsls_d_poly_regression())
        evalstring += 'byref(polyRegressionInfo_polyInfo_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (ssqPoly is None):
        processRet(ssqPoly_ssqPoly_tmp, shape=(degree, 4), pyvar=ssqPoly)
    if not (ssqLof is None):
        processRet(ssqLof_ssqLof_tmp, shape=(degree, 4), pyvar=ssqLof)
    if not (xMean is None):
        processRet(xMean_xMean_tmp, shape=(1), pyvar=xMean)
    if not (xVariance is None):
        processRet(xVariance_xVariance_tmp, shape=(1), pyvar=xVariance)
    if not (anovaTable is None):
        processRet(anovaTable_anovaTable_tmp, shape=(15), pyvar=anovaTable)
    if not (dfPureError is None):
        processRet(dfPureError_dfPureError_tmp, shape=(1), pyvar=dfPureError)
    if not (ssqPureError is None):
        processRet(ssqPureError_ssqPureError_tmp,
                   shape=(1), pyvar=ssqPureError)
    if not (residual is None):
        processRet(residual_residual_tmp, shape=(
            nObservations), pyvar=residual)
    if not (polyRegressionInfo is None):
        polyRegressionInfo.append(polyRegressionInfo_polyInfo_tmp)
    return processRet(result, shape=(degree + 1), result=True)
