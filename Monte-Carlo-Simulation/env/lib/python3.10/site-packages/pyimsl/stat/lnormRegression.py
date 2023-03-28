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
from numpy import double, dtype, rank, shape
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSLS_METHOD_LAV = 30009
IMSLS_METHOD_LLP = 30010
IMSLS_METHOD_LMV = 30011
IMSLS_X_COL_DIM = 15470
IMSLS_INTERCEPT = 12400
IMSLS_NO_INTERCEPT = 13350
IMSLS_RANK = 14110
IMSLS_ITERATIONS = 20681
IMSLS_N_ROWS_MISSING = 20400
IMSLS_TOLERANCE = 15040
IMSLS_SEA = 30012
IMSLS_MAX_RESIDUAL = 30013
IMSLS_R = 16068
IMSLS_DEGREES_OF_FREEDOM = 11140
IMSLS_RESIDUALS = 25570
IMSLS_SCALE = 14400
IMSLS_RESIDUALS_LP_NORM = 30014
IMSLS_EPS = 11370
IMSLS_WEIGHTS = 15400
IMSLS_FREQUENCIES = 11790
imslstat = loadimsl(STAT)


def lnormRegression(x, y, methodLav=None, methodLlp=None, methodLmv=None, xColDim=None, intercept=None, noIntercept=None, rank=None, iterations=None, nRowsMissing=None, tolerance=None, sea=None, maxResidual=None, r=None, degreesOfFreedom=None, residuals=None, scale=None, residualsLpNorm=None, eps=None, weights=None, frequencies=None):
    """ Fits a multiple linear regression model using criteria other than least squares.
    """
    imslstat.imsls_d_Lnorm_regression.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_Lnorm_regression('
    evalstring += 'c_int(nRows)'
    evalstring += ','
    evalstring += 'c_int(nIndependent)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nRows = shape[0]
    nIndependent = shape[1]
    evalstring += ','
    y = toNumpyArray(y, 'y', shape=shape, dtype='double',
                     expectedShape=(nRows))
    evalstring += 'y.ctypes.data_as(c_void_p)'
    checkForBoolean(methodLav, 'methodLav')
    if (methodLav):
        evalstring += ','
        evalstring += repr(IMSLS_METHOD_LAV)
    if not (methodLlp is None):
        evalstring += ','
        evalstring += repr(IMSLS_METHOD_LLP)
        evalstring += ','
        evalstring += 'c_double(methodLlp)'
    checkForBoolean(methodLmv, 'methodLmv')
    if (methodLmv):
        evalstring += ','
        evalstring += repr(IMSLS_METHOD_LMV)
    if not (xColDim is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(xColDim)'
    checkForBoolean(intercept, 'intercept')
    if (intercept):
        evalstring += ','
        evalstring += repr(IMSLS_INTERCEPT)
    checkForBoolean(noIntercept, 'noIntercept')
    if (noIntercept):
        evalstring += ','
        evalstring += repr(IMSLS_NO_INTERCEPT)
    if not (rank is None):
        evalstring += ','
        evalstring += repr(IMSLS_RANK)
        checkForList(rank, 'rank')
        evalstring += ','
        rank_rank_tmp = c_int()
        evalstring += 'byref(rank_rank_tmp)'
    if not (iterations is None):
        evalstring += ','
        evalstring += repr(IMSLS_ITERATIONS)
        checkForList(iterations, 'iterations')
        evalstring += ','
        iterations_iterations_tmp = c_int()
        evalstring += 'byref(iterations_iterations_tmp)'
    if not (nRowsMissing is None):
        evalstring += ','
        evalstring += repr(IMSLS_N_ROWS_MISSING)
        checkForList(nRowsMissing, 'nRowsMissing')
        evalstring += ','
        nRowsMissing_nRowsMissing_tmp = c_int()
        evalstring += 'byref(nRowsMissing_nRowsMissing_tmp)'
    if not (tolerance is None):
        evalstring += ','
        evalstring += repr(IMSLS_TOLERANCE)
        evalstring += ','
        evalstring += 'c_double(tolerance)'
    if not (sea is None):
        evalstring += ','
        evalstring += repr(IMSLS_SEA)
        checkForList(sea, 'sea')
        evalstring += ','
        sea_sumLavError_tmp = c_double()
        evalstring += 'byref(sea_sumLavError_tmp)'
    if not (maxResidual is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_RESIDUAL)
        checkForList(maxResidual, 'maxResidual')
        evalstring += ','
        maxResidual_maxResidual_tmp = c_double()
        evalstring += 'byref(maxResidual_maxResidual_tmp)'
    if not (r is None):
        evalstring += ','
        evalstring += repr(IMSLS_R)
        checkForList(r, 'r')
        evalstring += ','
        r_rMatrix_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(r_rMatrix_tmp)'
    if not (degreesOfFreedom is None):
        evalstring += ','
        evalstring += repr(IMSLS_DEGREES_OF_FREEDOM)
        checkForList(degreesOfFreedom, 'degreesOfFreedom')
        evalstring += ','
        degreesOfFreedom_dfError_tmp = c_double()
        evalstring += 'byref(degreesOfFreedom_dfError_tmp)'
    if not (residuals is None):
        evalstring += ','
        evalstring += repr(IMSLS_RESIDUALS)
        checkForList(residuals, 'residuals')
        evalstring += ','
        residuals_residual_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(residuals_residual_tmp)'
    if not (scale is None):
        evalstring += ','
        evalstring += repr(IMSLS_SCALE)
        checkForList(scale, 'scale')
        evalstring += ','
        scale_squareOfScale_tmp = c_double()
        evalstring += 'byref(scale_squareOfScale_tmp)'
    if not (residualsLpNorm is None):
        evalstring += ','
        evalstring += repr(IMSLS_RESIDUALS_LP_NORM)
        checkForList(residualsLpNorm, 'residualsLpNorm')
        evalstring += ','
        residualsLpNorm_lpNormResidual_tmp = c_double()
        evalstring += 'byref(residualsLpNorm_lpNormResidual_tmp)'
    if not (eps is None):
        evalstring += ','
        evalstring += repr(IMSLS_EPS)
        evalstring += ','
        evalstring += 'c_double(eps)'
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
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (rank is None):
        processRet(rank_rank_tmp, shape=(1), pyvar=rank)
    if not (iterations is None):
        processRet(iterations_iterations_tmp, shape=(1), pyvar=iterations)
    if not (nRowsMissing is None):
        processRet(nRowsMissing_nRowsMissing_tmp,
                   shape=(1), pyvar=nRowsMissing)
    if not (sea is None):
        processRet(sea_sumLavError_tmp, shape=(1), pyvar=sea)
    if not (maxResidual is None):
        processRet(maxResidual_maxResidual_tmp, shape=(1), pyvar=maxResidual)
    if not (r is None):
        processRet(r_rMatrix_tmp, shape=(
            nIndependent + 1, nIndependent + 1), pyvar=r)
    if not (degreesOfFreedom is None):
        processRet(degreesOfFreedom_dfError_tmp,
                   shape=(1), pyvar=degreesOfFreedom)
    if not (residuals is None):
        # NOTE: The document says that the size of the residuals array
        # is the number of observations, but it doesn't say which variable
        # represents the number of observations or how to derive it.
        # I'm going to make an educated guess that the number of observations
        # is the same as the number of rows in xx and yy.
        nObservations = nRows
        processRet(residuals_residual_tmp, shape=(
            nObservations), pyvar=residuals)
    if not (scale is None):
        processRet(scale_squareOfScale_tmp, shape=(1), pyvar=scale)
    if not (residualsLpNorm is None):
        processRet(residualsLpNorm_lpNormResidual_tmp,
                   shape=(1), pyvar=residualsLpNorm)
    return processRet(result, shape=(nIndependent + 1), result=True)
