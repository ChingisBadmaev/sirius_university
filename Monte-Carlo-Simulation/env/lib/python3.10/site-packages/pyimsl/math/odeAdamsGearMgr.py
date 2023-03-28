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
from pyimsl.util.imslUtils import MATH, checkForCallable, checkForList, fatalErrorCheck, loadimsl, toNumpyArray
from numpy import double, dtype, floor, shape, size
from ctypes import CFUNCTYPE, POINTER, byref, c_double, c_int, c_void_p
from pyimsl.math.OdeAGState import OdeAGState

IMSL_JACOBIAN = 10118
IMSL_METHOD = 10309
IMSL_MAXORD = 10310
IMSL_MITER = 10311
IMSL_TOL = 10072
IMSL_HINIT = 10073
IMSL_HMIN = 10074
IMSL_HMAX = 10085
IMSL_MAX_NUMBER_STEPS = 10077
IMSL_MAX_NUMBER_FCN_EVALS = 10078
IMSL_SCALE = 10075
IMSL_NORM = 10071
IMSL_FLOOR = 10076
IMSL_NSTEP = 10081
IMSL_NFCN = 10082
IMSL_NFCNJ = 10312
IMSL_FCN_W_DATA = 13101
IMSL_JACOBIAN_W_DATA = 13104

# Legal values for the "task" parameter

ODE_INITIALIZE = 1
ODE_CHANGE = 2
ODE_RESET = 3

imslmath = loadimsl(MATH)


def odeAdamsGearMgr(task, state, jacobian=None, method=None, maxord=None, miter=None, tol=None, hinit=None, hmin=None, hmax=None, maxNumberSteps=None, maxNumberFcnEvals=None, scale=None, norm=None, floor=None, nstep=None, nfcn=None, nfcnj=None, fcnWData=None, jacobianWData=None):
    imslmath.imsl_d_ode_adams_gear_mgr.restype = c_double
    shape = []
    evalstring = 'imslmath.imsl_d_ode_adams_gear_mgr('
    evalstring += 'c_int(task)'
    evalstring += ','
    if (task == ODE_INITIALIZE):
        state_tmp = c_void_p()
    elif (task == ODE_CHANGE) or (task == ODE_RESET):
        stateWrapper = state[0]
        state_tmp = stateWrapper.state
    evalstring += 'byref(state_tmp)'
    if not (jacobian is None):
        evalstring += ','
        evalstring += repr(IMSL_JACOBIAN)
        evalstring += ','
        checkForCallable(jacobian, 'jacobian')
        TMP_JACOBIAN_JACOBIAN = CFUNCTYPE(c_void_p, c_int, c_double, POINTER(
            c_double), POINTER(c_double), POINTER(c_double))
        tmp_jacobian_jacobian = TMP_JACOBIAN_JACOBIAN(jacobian)
        evalstring += 'tmp_jacobian_jacobian'
    if not (method is None):
        evalstring += ','
        evalstring += repr(IMSL_METHOD)
        evalstring += ','
        evalstring += 'c_int(method)'
    if not (maxord is None):
        evalstring += ','
        evalstring += repr(IMSL_MAXORD)
        evalstring += ','
        evalstring += 'c_int(maxord)'
    if not (miter is None):
        evalstring += ','
        evalstring += repr(IMSL_MITER)
        evalstring += ','
        evalstring += 'c_int(miter)'
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
    if not (hmin is None):
        evalstring += ','
        evalstring += repr(IMSL_HMIN)
        evalstring += ','
        evalstring += 'c_double(hmin)'
    if not (hmax is None):
        evalstring += ','
        evalstring += repr(IMSL_HMAX)
        evalstring += ','
        evalstring += 'c_double(hmax)'
    if not (maxNumberSteps is None):
        evalstring += ','
        evalstring += repr(IMSL_MAX_NUMBER_STEPS)
        evalstring += ','
        evalstring += 'c_int(maxNumberSteps)'
    if not (maxNumberFcnEvals is None):
        evalstring += ','
        evalstring += repr(IMSL_MAX_NUMBER_FCN_EVALS)
        evalstring += ','
        evalstring += 'c_int(maxNumberFcnEvals)'
    if not (scale is None):
        evalstring += ','
        evalstring += repr(IMSL_SCALE)
        evalstring += ','
        evalstring += 'c_double(scale)'
    if not (norm is None):
        evalstring += ','
        evalstring += repr(IMSL_NORM)
        evalstring += ','
        evalstring += 'c_int(norm)'
    if not (floor is None):
        evalstring += ','
        evalstring += repr(IMSL_FLOOR)
        evalstring += ','
        evalstring += 'c_double(floor)'
    if not (nstep is None):
        evalstring += ','
        evalstring += repr(IMSL_NSTEP)
        checkForList(nstep, 'nstep')
        evalstring += ','
        nstep_nstep_tmp = c_int()
        evalstring += 'byref(nstep_nstep_tmp)'
    if not (nfcn is None):
        evalstring += ','
        evalstring += repr(IMSL_NFCN)
        checkForList(nfcn, 'nfcn')
        evalstring += ','
        nfcn_nfcn_tmp = c_int()
        evalstring += 'byref(nfcn_nfcn_tmp)'
    if not (nfcnj is None):
        evalstring += ','
        evalstring += repr(IMSL_NFCNJ)
        checkForList(nfcnj, 'nfcnj')
        evalstring += ','
        nfcnj_nfcnj_tmp = c_int()
        evalstring += 'byref(nfcnj_nfcnj_tmp)'
    if not (fcnWData is None):
        evalstring += ','
        evalstring += repr(IMSL_FCN_W_DATA)
        checkForDict(fcnWData, 'fcnWData', ['fcnWData', 'data'])
        evalstring += ','
        tmp_fcnWData_fcnWData_param = fcnWData['fcnWData']
        checkForCallable(tmp_fcnWData_fcnWData_param, 'fcnWData')
        TMP_FCNWDATA_FCNWDATA = CFUNCTYPE(c_void_p, c_int, c_double, POINTER(
            c_double), POINTER(c_double), POINTER(c_double))
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
        evalstring += repr(IMSL_JACOBIAN_W_DATA)
        checkForDict(jacobianWData, 'jacobianWData', ['jacobianWData', 'data'])
        evalstring += ','
        tmp_jacobianWData_jacobianWData_param = jacobianWData['jacobianWData']
        checkForCallable(
            tmp_jacobianWData_jacobianWData_param, 'jacobianWData')
        TMP_JACOBIANWDATA_JACOBIANWDATA = CFUNCTYPE(c_void_p, c_int, c_double, POINTER(
            c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double))
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
    fatalErrorCheck(MATH)

    if (task == ODE_INITIALIZE):
        stateWrapper = OdeAGState(state_tmp)
        state[:] = []
        state.append(stateWrapper)
    if not (nstep is None):
        stateWrapper._setNstep(nstep_nstep_tmp)
        nstep[:] = []
        nstep.append(nstep_nstep_tmp)
    if not (nfcn is None):
        state.append(nfcn)
        state.append(nfcn_nfcn_tmp)
        # stateWrapper._setNfcn (nfcn_nfcn_tmp)
        nfcn[:] = []
        nfcn.append(nfcn_nfcn_tmp)
        nfcn.append(nfcn)
    if not (nfcnj is None):
        state.append(nfcnj)
        state.append(nfcnj_nfcnj_tmp)
        # stateWrapper._setNfcnj (nfcnj_nfcnj_tmp)
        nfcnj[:] = []
        nfcnj.append(nfcnj_nfcnj_tmp)
        nfcnj.append(nfcnj)
    if not (jacobian is None):
        state.append(jacobian)
        state.append(tmp_jacobian_jacobian)
    if (task == ODE_RESET):
        stateWrapper.setState(None)
        state[:] = []
    return result
