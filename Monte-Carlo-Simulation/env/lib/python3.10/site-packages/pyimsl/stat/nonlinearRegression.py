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
from pyimsl.util.imslUtils import STAT, checkForCallable, checkForList, fatalErrorCheck, loadimsl, processRet, toNumpyArray, checkForDict
from numpy import double, dtype, shape, size
from ctypes import CFUNCTYPE, POINTER, byref, c_double, c_int, c_void_p

IMSLS_THETA_GUESS = 15000
IMSLS_JACOBIAN = 12520
IMSLS_THETA_SCALE = 15010
IMSLS_GRADIENT_EPS = 12060
IMSLS_STEP_EPS = 14880
IMSLS_SSE_REL_EPS = 14660
IMSLS_SSE_ABS_EPS = 14650
IMSLS_MAX_STEP = 13070
IMSLS_INITIAL_TRUST_REGION = 12360
IMSLS_GOOD_DIGIT = 12030
IMSLS_MAX_ITERATIONS = 12970
IMSLS_MAX_SSE_EVALUATIONS = 13060
IMSLS_MAX_JACOBIAN_EVALUATIONS = 13000
IMSLS_TOLERANCE = 15040
IMSLS_PREDICTED = 16079
IMSLS_RESIDUAL = 14190
IMSLS_R = 16068
IMSLS_R_COL_DIM = 16072
IMSLS_R_RANK = 16070
IMSLS_X_COL_DIM = 15470
IMSLS_DF = 11185
IMSLS_SSE = 14640
IMSLS_VARIANCE_COVARIANCE_MATRIX = 15330
IMSLS_FCN_W_DATA = 40020
IMSLS_JACOBIAN_W_DATA = 40023
imslstat = loadimsl(STAT)


def nonlinearRegression(fcn, nParameters, x, y, thetaGuess=None, jacobian=None, thetaScale=None, gradientEps=None, stepEps=None, sseRelEps=None, sseAbsEps=None, maxStep=None, initialTrustRegion=None, goodDigit=None, maxIterations=None, maxSseEvaluations=None, maxJacobianEvaluations=None, tolerance=None, predicted=None, residual=None, r=None, rColDim=None, rRank=None, xColDim=None, df=None, sse=None, varianceCovarianceMatrix=None, fcnWData=None, jacobianWData=None):
    """ Fits a multivarite nonlinear regression model.
    """
    imslstat.imsls_d_nonlinear_regression.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_nonlinear_regression('
    checkForCallable(fcn, 'fcn')
    TMP_FCN = CFUNCTYPE(c_double, c_int, POINTER(
        c_double), c_int, POINTER(c_double))
    tmp_fcn = TMP_FCN(fcn)
    evalstring += 'tmp_fcn'
    evalstring += ','
    evalstring += 'c_int(nParameters)'
    evalstring += ','
    evalstring += 'c_int(nObservations)'
    evalstring += ','
    evalstring += 'c_int(nIndependent)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nObservations = shape[0]
    nIndependent = shape[1]
    evalstring += ','
    y = toNumpyArray(y, 'y', shape=shape, dtype='double',
                     expectedShape=(nObservations))
    evalstring += 'y.ctypes.data_as(c_void_p)'
    if not (thetaGuess is None):
        evalstring += ','
        evalstring += repr(IMSLS_THETA_GUESS)
        evalstring += ','
        thetaGuess = toNumpyArray(
            thetaGuess, 'thetaGuess', shape=shape, dtype='double', expectedShape=(nParameters))
        evalstring += 'thetaGuess.ctypes.data_as(c_void_p)'
    if not (jacobian is None):
        evalstring += ','
        evalstring += repr(IMSLS_JACOBIAN)
        evalstring += ','
        checkForCallable(jacobian, 'jacobian')
        TMP_JACOBIAN_JACOBIAN = CFUNCTYPE(c_void_p, c_int, POINTER(
            c_double), c_int, POINTER(c_double), POINTER(c_double))
        tmp_jacobian_jacobian = TMP_JACOBIAN_JACOBIAN(jacobian)
        evalstring += 'tmp_jacobian_jacobian'
    if not (thetaScale is None):
        evalstring += ','
        evalstring += repr(IMSLS_THETA_SCALE)
        evalstring += ','
        thetaScale = toNumpyArray(
            thetaScale, 'thetaScale', shape=shape, dtype='double', expectedShape=(nParameters))
        evalstring += 'thetaScale.ctypes.data_as(c_void_p)'
    if not (gradientEps is None):
        evalstring += ','
        evalstring += repr(IMSLS_GRADIENT_EPS)
        evalstring += ','
        evalstring += 'c_double(gradientEps)'
    if not (stepEps is None):
        evalstring += ','
        evalstring += repr(IMSLS_STEP_EPS)
        evalstring += ','
        evalstring += 'c_double(stepEps)'
    if not (sseRelEps is None):
        evalstring += ','
        evalstring += repr(IMSLS_SSE_REL_EPS)
        evalstring += ','
        evalstring += 'c_double(sseRelEps)'
    if not (sseAbsEps is None):
        evalstring += ','
        evalstring += repr(IMSLS_SSE_ABS_EPS)
        evalstring += ','
        evalstring += 'c_double(sseAbsEps)'
    if not (maxStep is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_STEP)
        evalstring += ','
        evalstring += 'c_double(maxStep)'
    if not (initialTrustRegion is None):
        evalstring += ','
        evalstring += repr(IMSLS_INITIAL_TRUST_REGION)
        evalstring += ','
        evalstring += 'c_double(initialTrustRegion)'
    if not (goodDigit is None):
        evalstring += ','
        evalstring += repr(IMSLS_GOOD_DIGIT)
        evalstring += ','
        evalstring += 'c_int(goodDigit)'
    if not (maxIterations is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_ITERATIONS)
        evalstring += ','
        evalstring += 'c_int(maxIterations)'
    if not (maxSseEvaluations is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_SSE_EVALUATIONS)
        evalstring += ','
        evalstring += 'c_int(maxSseEvaluations)'
    if not (maxJacobianEvaluations is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_JACOBIAN_EVALUATIONS)
        evalstring += ','
        evalstring += 'c_int(maxJacobianEvaluations)'
    if not (tolerance is None):
        evalstring += ','
        evalstring += repr(IMSLS_TOLERANCE)
        evalstring += ','
        evalstring += 'c_double(tolerance)'
    if not (predicted is None):
        evalstring += ','
        evalstring += repr(IMSLS_PREDICTED)
        checkForList(predicted, 'predicted')
        evalstring += ','
        predicted_predicted_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(predicted_predicted_tmp)'
    if not (residual is None):
        evalstring += ','
        evalstring += repr(IMSLS_RESIDUAL)
        checkForList(residual, 'residual')
        evalstring += ','
        residual_residual_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(residual_residual_tmp)'
    if not (r is None):
        evalstring += ','
        evalstring += repr(IMSLS_R)
        checkForList(r, 'r')
        evalstring += ','
        r_r_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(r_r_tmp)'
    if not (rColDim is None):
        evalstring += ','
        evalstring += repr(IMSLS_R_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(rColDim)'
    if not (rRank is None):
        evalstring += ','
        evalstring += repr(IMSLS_R_RANK)
        checkForList(rRank, 'rRank')
        evalstring += ','
        rRank_rank_tmp = c_int()
        evalstring += 'byref(rRank_rank_tmp)'
    if not (xColDim is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(xColDim)'
    if not (df is None):
        evalstring += ','
        evalstring += repr(IMSLS_DF)
        checkForList(df, 'df')
        evalstring += ','
        df_df_tmp = c_int()
        evalstring += 'byref(df_df_tmp)'
    if not (sse is None):
        evalstring += ','
        evalstring += repr(IMSLS_SSE)
        checkForList(sse, 'sse')
        evalstring += ','
        sse_sse_tmp = c_double()
        evalstring += 'byref(sse_sse_tmp)'
    if not (varianceCovarianceMatrix is None):
        evalstring += ','
        evalstring += repr(IMSLS_VARIANCE_COVARIANCE_MATRIX)
        checkForList(varianceCovarianceMatrix, 'varianceCovarianceMatrix')
        evalstring += ','
        varianceCovarianceMatrix_varCovar_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(varianceCovarianceMatrix_varCovar_tmp)'
    if not (fcnWData is None):
        evalstring += ','
        evalstring += repr(IMSLS_FCN_W_DATA)
        checkForDict(fcnWData, 'fcnWData', ['fcn', 'data'])
        evalstring += ','
        tmp_fcnWData_fcn_param = fcnWData['fcn']
        checkForCallable(tmp_fcnWData_fcn_param, 'fcn')
        TMP_FCNWDATA_FCN = CFUNCTYPE(c_double, c_int, POINTER(
            c_double), c_int, POINTER(c_double))
        tmp_fcnWData_fcn = TMP_FCNWDATA_FCN(tmp_fcnWData_fcn_param)
        evalstring += 'tmp_fcnWData_fcn'
        evalstring += ','
        fcnWData_data_tmp = fcnWData['data']
        fcnWData_data_tmp = toNumpyArray(
            fcnWData_data_tmp, 'data', shape=shape, dtype='double')
        evalstring += 'fcnWData_data_tmp.ctypes.data_as(c_void_p)'
    if not (jacobianWData is None):
        evalstring += ','
        evalstring += repr(IMSLS_JACOBIAN_W_DATA)
        checkForDict(jacobianWData, 'jacobianWData', ['jacobianWData', 'data'])
        evalstring += ','
        tmp_jacobianWData_jacobianWData_param = jacobianWData['jacobianWData']
        checkForCallable(
            tmp_jacobianWData_jacobianWData_param, 'jacobianWData')
        TMP_JACOBIANWDATA_JACOBIANWDATA = CFUNCTYPE(c_void_p, c_int, POINTER(
            c_double), c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double))
        tmp_jacobianWData_jacobianWData = TMP_JACOBIANWDATA_JACOBIANWDATA(
            tmp_jacobianWData_jacobianWData_param)
        evalstring += 'tmp_jacobianWData_jacobianWData'
        evalstring += ','
        jacobianWData_data_tmp = jacobianWData['data']
        jacobianWData_data_tmp = toNumpyArray(
            jacobianWData_data_tmp, 'data', shape=shape, dtype='double')
        evalstring += 'jacobianWData_data_tmp.ctypes.data_as(c_void_p)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (predicted is None):
        processRet(predicted_predicted_tmp, shape=(
            nObservations), pyvar=predicted)
    if not (residual is None):
        processRet(residual_residual_tmp, shape=(
            nObservations), pyvar=residual)
    if not (r is None):
        processRet(r_r_tmp, shape=(nParameters, nParameters), pyvar=r)
    if not (rRank is None):
        processRet(rRank_rank_tmp, shape=(1), pyvar=rRank)
    if not (df is None):
        processRet(df_df_tmp, shape=(1), pyvar=df)
    if not (sse is None):
        processRet(sse_sse_tmp, shape=(1), pyvar=sse)
    if not (varianceCovarianceMatrix is None):
        processRet(varianceCovarianceMatrix_varCovar_tmp, shape=(
            nParameters, nParameters), pyvar=varianceCovarianceMatrix)
    return processRet(result, shape=(nParameters), result=True)
