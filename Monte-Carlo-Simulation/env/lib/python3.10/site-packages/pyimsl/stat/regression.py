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
from pyimsl.util.imslUtils import STAT, checkForBoolean, checkForList, fatalErrorCheck, loadimsl, processRet, toNumpyArray, checkForDict
from numpy import double, dtype, int, rank, shape, size
from ctypes import POINTER, byref, c_double, c_int, c_void_p
from .statStructs import Imsls_d_regression

IMSLS_X_COL_DIM = 15470
IMSLS_Y_COL_DIM = 15540
IMSLS_N_DEPENDENT = 20900
IMSLS_X_INDICES = 20443
IMSLS_IDO = 20440
IMSLS_ROWS_ADD = 20441
IMSLS_ROWS_DELETE = 20442
IMSLS_INTERCEPT = 12400
IMSLS_NO_INTERCEPT = 13350
IMSLS_TOLERANCE = 15040
IMSLS_RANK = 14110
IMSLS_COEF_COVARIANCES = 10690
IMSLS_COV_COL_DIM = 11055
IMSLS_X_MEAN = 15490
IMSLS_RESIDUAL = 14190
IMSLS_ANOVA_TABLE = 10080
IMSLS_SCPE = 20930
IMSLS_FREQUENCIES = 11790
IMSLS_WEIGHTS = 15400
IMSLS_REGRESSION_INFO = 14140
imslstat = loadimsl(STAT)


def regression(x, y, xColDim=None, yColDim=None, nDependent=None, xIndices=None, ido=None, rowsAdd=None, rowsDelete=None, intercept=None, noIntercept=None, tolerance=None, rank=None, coefCovariances=None, covColDim=None, xMean=None, residual=None, anovaTable=None, scpe=None, frequencies=None, weights=None, regressionInfo=None):
    """ Fits a multivariate linear regression model using least squares.
    """
    imslstat.imsls_d_regression.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_regression('
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
        evalstring += repr(IMSLS_X_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(xColDim)'
    if not (yColDim is None):
        evalstring += ','
        evalstring += repr(IMSLS_Y_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(yColDim)'
    if not (nDependent is None):
        evalstring += ','
        evalstring += repr(IMSLS_N_DEPENDENT)
        evalstring += ','
        evalstring += 'c_int(nDependent)'
    else:
        nDependent = 1
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
#
#       If xIndices is specified, it overrides the values of nIndependent
#       and nDependent.  Stupid, but I'll handle the special case here.
#
        nIndependent = len(xIndices_indind_tmp)
        nDependent = len(xIndices_inddep_tmp)
    if not (ido is None):
        evalstring += ','
        evalstring += repr(IMSLS_IDO)
        evalstring += ','
        evalstring += 'c_int(ido)'
    checkForBoolean(rowsAdd, 'rowsAdd')
    if (rowsAdd):
        evalstring += ','
        evalstring += repr(IMSLS_ROWS_ADD)
    checkForBoolean(rowsDelete, 'rowsDelete')
    if (rowsDelete):
        evalstring += ','
        evalstring += repr(IMSLS_ROWS_DELETE)
    checkForBoolean(intercept, 'intercept')
    if (intercept):
        evalstring += ','
        evalstring += repr(IMSLS_INTERCEPT)
    checkForBoolean(noIntercept, 'noIntercept')
    if (noIntercept):
        evalstring += ','
        evalstring += repr(IMSLS_NO_INTERCEPT)
    if not (tolerance is None):
        evalstring += ','
        evalstring += repr(IMSLS_TOLERANCE)
        evalstring += ','
        evalstring += 'c_double(tolerance)'
    if not (rank is None):
        evalstring += ','
        evalstring += repr(IMSLS_RANK)
        checkForList(rank, 'rank')
        evalstring += ','
        rank_rank_tmp = c_int()
        evalstring += 'byref(rank_rank_tmp)'
    if not (coefCovariances is None):
        evalstring += ','
        evalstring += repr(IMSLS_COEF_COVARIANCES)
        checkForList(coefCovariances, 'coefCovariances')
        evalstring += ','
        coefCovariances_coefCovariances_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(coefCovariances_coefCovariances_tmp)'
    if not (covColDim is None):
        evalstring += ','
        evalstring += repr(IMSLS_COV_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(covColDim)'
    if not (xMean is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_MEAN)
        checkForList(xMean, 'xMean')
        evalstring += ','
        xMean_xMean_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(xMean_xMean_tmp)'
    if not (residual is None):
        evalstring += ','
        evalstring += repr(IMSLS_RESIDUAL)
        checkForList(residual, 'residual')
        evalstring += ','
        residual_residual_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(residual_residual_tmp)'
    if not (anovaTable is None):
        evalstring += ','
        evalstring += repr(IMSLS_ANOVA_TABLE)
        checkForList(anovaTable, 'anovaTable')
        evalstring += ','
        anovaTable_anovaTable_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(anovaTable_anovaTable_tmp)'
    if not (scpe is None):
        evalstring += ','
        evalstring += repr(IMSLS_SCPE)
        checkForList(scpe, 'scpe')
        evalstring += ','
        scpe_scpe_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(scpe_scpe_tmp)'
    if not (frequencies is None):
        evalstring += ','
        evalstring += repr(IMSLS_FREQUENCIES)
        evalstring += ','
        frequencies = toNumpyArray(
            frequencies, 'frequencies', shape=shape, dtype='double', expectedShape=(nRows))
        evalstring += 'frequencies.ctypes.data_as(c_void_p)'
    if not (weights is None):
        evalstring += ','
        evalstring += repr(IMSLS_WEIGHTS)
        evalstring += ','
        weights = toNumpyArray(
            weights, 'weights', shape=shape, dtype='double', expectedShape=(nRows))
        evalstring += 'weights.ctypes.data_as(c_void_p)'
    if not (regressionInfo is None):
        evalstring += ','
        evalstring += repr(IMSLS_REGRESSION_INFO)
        checkForList(regressionInfo, 'regressionInfo')
        evalstring += ','
        regressionInfo_regressionInfo_tmp = POINTER(
            Imsls_d_regression)(Imsls_d_regression())
        evalstring += 'byref(regressionInfo_regressionInfo_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (rank is None):
        processRet(rank_rank_tmp, shape=1, pyvar=rank)
    if not (coefCovariances is None):
        checkForBoolean(noIntercept, 'noIntercept')
        if (noIntercept):
            m = nIndependent
        else:
            m = nIndependent + 1
        processRet(coefCovariances_coefCovariances_tmp,
                   shape=(m, m), pyvar=coefCovariances)
    if not (xMean is None):
        processRet(xMean_xMean_tmp, shape=(nIndependent), pyvar=xMean)
    if not (residual is None):
        processRet(residual_residual_tmp, shape=(
            nRows, nDependent), pyvar=residual)
    if not (anovaTable is None):
        processRet(anovaTable_anovaTable_tmp, shape=(
            15, nDependent), pyvar=anovaTable)
    if not (scpe is None):
        processRet(scpe_scpe_tmp, shape=(nDependent, nDependent), pyvar=scpe)
    if not (regressionInfo is None):
        regressionInfo.append(regressionInfo_regressionInfo_tmp)
    m = (nDependent, nIndependent + 1)
    if (noIntercept):
        m = (nDependent, nIndependent)

    return processRet(result, shape=(m), result=True)
