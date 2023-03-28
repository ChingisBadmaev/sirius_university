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
from pyimsl.util.imslUtils import MATH, checkForCallable, checkForList, checkForNumpy, fatalErrorCheck, loadimsl, processRet, toNumpyArray, checkForDict
from numpy import double, dtype, shape, size, ndarray
from ctypes import CFUNCTYPE, POINTER, byref, c_double, c_int, c_void_p
from pyimsl.util.CnlState import CnlState

IMSL_TOL = 10072
IMSL_HINIT = 10073
IMSL_INITIAL_VALUE_DERIVATIVE = 11151
IMSL_HTRIAL = 10083
IMSL_FCN_UT_W_DATA = 13107
IMSL_FCN_BC_W_DATA = 13108

# Legal values for task
PDE_INITIALIZE = 1
PDE_CHANGE = 2
PDE_RESET = 3

imslmath = loadimsl(MATH)
# initialValueDerivative - Must be a numpy array.


def modifiedMethodOfLinesMgr(task, state, tol=None, hinit=None, initialValueDerivative=None, htrial=None, fcnUtWData=None, fcnBcWData=None):
    imslmath.imsl_d_modified_method_of_lines_mgr.restype = None
    shape = []
    evalstring = 'imslmath.imsl_d_modified_method_of_lines_mgr('
    evalstring += 'c_int(task)'
    evalstring += ','
    if (task == PDE_INITIALIZE):
        state_tmp = c_void_p()
    else:
        stateWrapper = state[0]
        state_tmp = stateWrapper.state
    evalstring += 'byref(state_tmp)'
    if not (tol is None):
        evalstring += ','
        evalstring += repr(IMSL_TOL)
        evalstring += ','
        evalstring += 'c_double(tol)'
    if not (hinit is None):
        evalstring += ','
        evalstring += repr(IMSL_HINIT)
        evalstring += ','
        evalstring += 'c_double(hinit)'
    if not (initialValueDerivative is None):
        evalstring += ','
        evalstring += repr(IMSL_INITIAL_VALUE_DERIVATIVE)
        checkForNumpy(initialValueDerivative,
                      'initialValueDerivative', dtype='double')
        evalstring += ','
        if(not(isinstance(initialValueDerivative, ndarray))):
            initialValueDerivative = toNumpyArray(
                initialValueDerivative, 'initialValueDerivative', shape=shape, dtype='double', expectedShape=(0, 0))
        # npdes = shape[0]
        # nx = shape[1]
        evalstring += 'initialValueDerivative.ctypes.data_as(c_void_p)'
    if not (htrial is None):
        evalstring += ','
        evalstring += repr(IMSL_HTRIAL)
        checkForList(htrial, 'htrial')
        evalstring += ','
        htrial_htrial_tmp = c_double()
        evalstring += 'byref(htrial_htrial_tmp)'
    if not (fcnUtWData is None):
        evalstring += ','
        evalstring += repr(IMSL_FCN_UT_W_DATA)
        checkForDict(fcnUtWData, 'fcnUtWData', ['fcnUtWData', 'data'])
        evalstring += ','
        tmp_fcnUtWData_fcnUtWData_param = fcnUtWData['fcnUtWData']
        checkForCallable(tmp_fcnUtWData_fcnUtWData_param, 'fcnUtWData')
        TMP_FCNUTWDATA_FCNUTWDATA = CFUNCTYPE(c_void_p, c_int, c_double, c_double, POINTER(
            c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double))
        tmp_fcnUtWData_fcnUtWData = TMP_FCNUTWDATA_FCNUTWDATA(
            tmp_fcnUtWData_fcnUtWData_param)
        evalstring += 'tmp_fcnUtWData_fcnUtWData'
        evalstring += ','
        fcnUtWData_data_tmp = fcnUtWData['data']
        fcnUtWData_data_tmp = toNumpyArray(
            fcnUtWData_data_tmp, 'data', shape=shape, dtype='double')
        evalstring += 'fcnUtWData_data_tmp.ctypes.data_as(c_void_p)'
    if not (fcnBcWData is None):
        evalstring += ','
        evalstring += repr(IMSL_FCN_BC_W_DATA)
        checkForDict(fcnBcWData, 'fcnBcWData', ['fcnBcWData', 'data'])
        evalstring += ','
        tmp_fcnBcWData_fcnBcWData_param = fcnBcWData['fcnBcWData']
        checkForCallable(tmp_fcnBcWData_fcnBcWData_param, 'fcnBcWData')
        TMP_FCNBCWDATA_FCNBCWDATA = CFUNCTYPE(c_void_p, c_int, c_double, c_double, POINTER(
            c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double))
        tmp_fcnBcWData_fcnBcWData = TMP_FCNBCWDATA_FCNBCWDATA(
            tmp_fcnBcWData_fcnBcWData_param)
        evalstring += 'tmp_fcnBcWData_fcnBcWData'
        evalstring += ','
        fcnBcWData_data_tmp = fcnBcWData['data']
        fcnBcWData_data_tmp = toNumpyArray(
            fcnBcWData_data_tmp, 'data', shape=shape, dtype='double')
        evalstring += 'fcnBcWData_data_tmp.ctypes.data_as(c_void_p)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if (task == PDE_INITIALIZE):
        stateWrapper = CnlState(state_tmp)
        state[:] = []
        state.append(stateWrapper)
    if (task == PDE_RESET):
        stateWrapper.setState(None)
    # if not (initialValueDerivative is None):
    #   processRet(initialValueDerivative_initialDeriv_tmp, shape=(npdes,nx), inout=True, pyvar=initialValueDerivative)
    if not (htrial is None):
        processRet(htrial_htrial_tmp, shape=(1), pyvar=htrial)
    return
