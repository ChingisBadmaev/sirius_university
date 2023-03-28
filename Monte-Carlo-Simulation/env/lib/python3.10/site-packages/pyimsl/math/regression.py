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
from pyimsl.util.imslUtils import MATH, checkForBoolean, checkForList, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, math, rank, shape, version
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSL_X_COL_DIM = 10045
IMSL_NO_INTERCEPT = 10050
IMSL_TOLERANCE = 10053
IMSL_RANK = 10049
IMSL_COEF_COVARIANCES = 10047
IMSL_COV_COL_DIM = 10046
IMSL_X_MEAN = 10158
IMSL_RESIDUAL = 10172
IMSL_ANOVA_TABLE = 10051
imslmath = loadimsl(MATH)


def regression(x, y, xColDim=None, noIntercept=None, tolerance=None, rank=None, coefCovariances=None, covColDim=None, xMean=None, residual=None, anovaTable=None):
    """ Fits a multiple linear regression model using least squares.
    """
    imslmath.imsl_d_regression.restype = POINTER(c_double)
    shape = []
    nDependent = 1  # this is not changable in the math version of regression
    evalstring = 'imslmath.imsl_d_regression('
    evalstring += 'c_int(nRows)'
    evalstring += ','
    evalstring += 'c_int(nIndependent)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nRows = shape[0]
    nIndependent = shape[1]
    evalstring += ','
    y = toNumpyArray(y, 'y', shape=shape, dtype='double')
    evalstring += 'y.ctypes.data_as(c_void_p)'
    if not (xColDim is None):
        evalstring += ','
        evalstring += repr(IMSL_X_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(xColDim)'
    checkForBoolean(noIntercept, 'noIntercept')
    if (noIntercept):
        evalstring += ','
        evalstring += repr(IMSL_NO_INTERCEPT)
    if not (tolerance is None):
        evalstring += ','
        evalstring += repr(IMSL_TOLERANCE)
        evalstring += ','
        evalstring += 'c_double(tolerance)'
    if not (rank is None):
        evalstring += ','
        evalstring += repr(IMSL_RANK)
        checkForList(rank, 'rank')
        evalstring += ','
        rank_rank_tmp = c_int()
        evalstring += 'byref(rank_rank_tmp)'
    if not (coefCovariances is None):
        evalstring += ','
        evalstring += repr(IMSL_COEF_COVARIANCES)
        checkForList(coefCovariances, 'coefCovariances')
        evalstring += ','
        coefCovariances_pCoefCovariances_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(coefCovariances_pCoefCovariances_tmp)'
    if not (covColDim is None):
        evalstring += ','
        evalstring += repr(IMSL_COV_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(covColDim)'
    if not (xMean is None):
        evalstring += ','
        evalstring += repr(IMSL_X_MEAN)
        checkForList(xMean, 'xMean')
        evalstring += ','
        xMean_pXMean_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(xMean_pXMean_tmp)'
    if not (residual is None):
        evalstring += ','
        evalstring += repr(IMSL_RESIDUAL)
        checkForList(residual, 'residual')
        evalstring += ','
        residual_pResidual_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(residual_pResidual_tmp)'
    if not (anovaTable is None):
        evalstring += ','
        evalstring += repr(IMSL_ANOVA_TABLE)
        checkForList(anovaTable, 'anovaTable')
        evalstring += ','
        anovaTable_pAnovaTable_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(anovaTable_pAnovaTable_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (rank is None):
        processRet(rank_rank_tmp, shape=1, pyvar=rank)
    if not (coefCovariances is None):
        checkForBoolean(noIntercept, 'noIntercept')
        if (noIntercept):
            m = nIndependent
        else:
            m = nIndependent + 1
        processRet(coefCovariances_pCoefCovariances_tmp,
                   shape=(m), pyvar=coefCovariances)
    if not (xMean is None):
        processRet(xMean_pXMean_tmp, shape=(nIndependent), pyvar=xMean)
    if not (residual is None):
        processRet(residual_pResidual_tmp, shape=(
            nRows, nDependent), pyvar=residual)
    if not (anovaTable is None):
        processRet(anovaTable_pAnovaTable_tmp, shape=(
            15, nDependent), pyvar=anovaTable)
    checkForBoolean(noIntercept, 'noIntercept')
    if (noIntercept):
        m = (nDependent, nIndependent)
    else:
        m = (nDependent, nIndependent + 1)
    return processRet(result, shape=(m), result=True)
