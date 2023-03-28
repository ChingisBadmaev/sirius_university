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
IMSLS_SIMPLE_LOWER_BOUNDS = 20470
IMSLS_SIMPLE_UPPER_BOUNDS = 20480
IMSLS_LINEAR_CONSTRAINTS = 20540
IMSLS_FREQUENCIES = 11790
IMSLS_WEIGHTS = 15400
IMSLS_ACC = 20490
IMSLS_MAX_SSE_EVALUATIONS = 13060
IMSLS_PRINT_LEVEL = 20530
IMSLS_STOP_INFO = 20500
IMSLS_ACTIVE_CONSTRAINTS_INFO = 20510
IMSLS_PREDICTED = 16079
IMSLS_RESIDUAL = 14190
IMSLS_SSE = 14640
IMSLS_FCN_W_DATA = 40020
IMSLS_JACOBIAN_W_DATA = 40023
imslstat = loadimsl(STAT)


def nonlinearOptimization(fcn, nParameters, x, y, thetaGuess=None, jacobian=None, simpleLowerBounds=None, simpleUpperBounds=None, linearConstraints=None, frequencies=None, weights=None, acc=None, maxSseEvaluations=None, printLevel=None, stopInfo=None, activeConstraintsInfo=None, predicted=None, residual=None, sse=None, fcnWData=None, jacobianWData=None):
    """ Fits data to a nonlinear model (possibly with linear constraints) using the successive quadratic programming algorithm.
    """
    imslstat.imsls_d_nonlinear_optimization.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_nonlinear_optimization('
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
    if not (simpleLowerBounds is None):
        evalstring += ','
        evalstring += repr(IMSLS_SIMPLE_LOWER_BOUNDS)
        evalstring += ','
        simpleLowerBounds = toNumpyArray(
            simpleLowerBounds, 'simpleLowerBounds', shape=shape, dtype='double', expectedShape=(nParameters))
        evalstring += 'simpleLowerBounds.ctypes.data_as(c_void_p)'
    if not (simpleUpperBounds is None):
        evalstring += ','
        evalstring += repr(IMSLS_SIMPLE_UPPER_BOUNDS)
        evalstring += ','
        simpleUpperBounds = toNumpyArray(
            simpleUpperBounds, 'simpleUpperBounds', shape=shape, dtype='double', expectedShape=(nParameters))
        evalstring += 'simpleUpperBounds.ctypes.data_as(c_void_p)'
    if not (linearConstraints is None):
        evalstring += ','
        evalstring += repr(IMSLS_LINEAR_CONSTRAINTS)
        checkForDict(linearConstraints, 'linearConstraints',
                     ['nEquality', 'a', 'b'])
        evalstring += ','
        evalstring += 'c_int(linearConstraints_nConstraints_tmp)'
        evalstring += ','
        linearConstraints_nEquality_tmp = linearConstraints['nEquality']
        evalstring += 'c_int(linearConstraints_nEquality_tmp)'
        evalstring += ','
        linearConstraints_a_tmp = linearConstraints['a']
        linearConstraints_a_tmp = toNumpyArray(
            linearConstraints_a_tmp, 'a', shape=shape, dtype='double', expectedShape=(0, nParameters))
        evalstring += 'linearConstraints_a_tmp.ctypes.data_as(c_void_p)'
        linearConstraints_nConstraints_tmp = shape[0]
        evalstring += ','
        linearConstraints_b_tmp = linearConstraints['b']
        linearConstraints_b_tmp = toNumpyArray(
            linearConstraints_b_tmp, 'b', shape=shape, dtype='double', expectedShape=(linearConstraints_nConstraints_tmp))
        evalstring += 'linearConstraints_b_tmp.ctypes.data_as(c_void_p)'
    if not (frequencies is None):
        evalstring += ','
        evalstring += repr(IMSLS_FREQUENCIES)
        evalstring += ','
        evalstring += 'c_double(frequencies)'
    if not (weights is None):
        evalstring += ','
        evalstring += repr(IMSLS_WEIGHTS)
        evalstring += ','
        evalstring += 'c_double(weights)'
    if not (acc is None):
        evalstring += ','
        evalstring += repr(IMSLS_ACC)
        evalstring += ','
        evalstring += 'c_double(acc)'
    if not (maxSseEvaluations is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_SSE_EVALUATIONS)
        checkForList(maxSseEvaluations, 'maxSseEvaluations')
        evalstring += ','
        maxSseEvaluations_maxSseEval_tmp = maxSseEval[0]
        if (not(isinstance(maxSseEvaluations_maxSseEval_tmp, c_int))):
            maxSseEvaluations_maxSseEval_tmp = c_int(maxSseEval[0])
        evalstring += 'byref(maxSseEvaluations_maxSseEval_tmp)'
    if not (printLevel is None):
        evalstring += ','
        evalstring += repr(IMSLS_PRINT_LEVEL)
        evalstring += ','
        evalstring += 'c_int(printLevel)'
    if not (stopInfo is None):
        evalstring += ','
        evalstring += repr(IMSLS_STOP_INFO)
        checkForList(stopInfo, 'stopInfo')
        evalstring += ','
        stopInfo_stopInfo_tmp = c_int()
        evalstring += 'byref(stopInfo_stopInfo_tmp)'
    if not (activeConstraintsInfo is None):
        evalstring += ','
        evalstring += repr(IMSLS_ACTIVE_CONSTRAINTS_INFO)
        checkForDict(activeConstraintsInfo, 'activeConstraintsInfo', [])
        evalstring += ','
        activeConstraintsInfo_nActive_tmp = c_int()
        evalstring += 'byref(activeConstraintsInfo_nActive_tmp)'
        evalstring += ','
        activeConstraintsInfo_indicesActive_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(activeConstraintsInfo_indicesActive_tmp)'
        evalstring += ','
        activeConstraintsInfo_multiplier_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(activeConstraintsInfo_multiplier_tmp)'
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
    if not (sse is None):
        evalstring += ','
        evalstring += repr(IMSLS_SSE)
        checkForList(sse, 'sse')
        evalstring += ','
        sse_sse_tmp = c_double()
        evalstring += 'byref(sse_sse_tmp)'
    if not (fcnWData is None):
        evalstring += ','
        evalstring += repr(IMSLS_FCN_W_DATA)
        checkForDict(fcnWData, 'fcnWData', ['fcnWData', 'data'])
        evalstring += ','
        tmp_fcnWData_fcnWData_param = fcnWData['fcnWData']
        checkForCallable(tmp_fcnWData_fcnWData_param, 'fcnWData')
        TMP_FCNWDATA_FCNWDATA = CFUNCTYPE(c_double, c_int, POINTER(
            c_double), c_int, POINTER(c_double), POINTER(c_double))
        tmp_fcnWData_fcnWData = TMP_FCNWDATA_FCNWDATA(
            tmp_fcnWData_fcnWData_param)
        evalstring += 'tmp_fcnWData_fcnWData'
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
        TMP_JACOBIANWDATA_JACOBIANWDATA = CFUNCTYPE(c_double, c_int, POINTER(
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
    if not (maxSseEvaluations is None):
        processRet(maxSseEvaluations_maxSseEval_tmp,
                   shape=(1), pyvar=maxSseEvaluations)
    if not (stopInfo is None):
        processRet(stopInfo_stopInfo_tmp, shape=(1), pyvar=stopInfo)
    if not (activeConstraintsInfo is None):
        processRet(activeConstraintsInfo_nActive_tmp, shape=(
            1), key='nActive', pyvar=activeConstraintsInfo)
        processRet(activeConstraintsInfo_indicesActive_tmp, shape=(
            activeConstraintsInfo_nActive_tmp), key='indicesActive', pyvar=activeConstraintsInfo)
        processRet(activeConstraintsInfo_multiplier_tmp, shape=(
            activeConstraintsInfo_nActive_tmp), key='multiplier', pyvar=activeConstraintsInfo)
    if not (predicted is None):
        processRet(predicted_predicted_tmp, shape=(
            nObservations), pyvar=predicted)
    if not (residual is None):
        processRet(residual_residual_tmp, shape=(
            nObservations), pyvar=residual)
    if not (sse is None):
        processRet(sse_sse_tmp, shape=(1), pyvar=sse)
    return processRet(result, shape=(nParameters), result=True)
