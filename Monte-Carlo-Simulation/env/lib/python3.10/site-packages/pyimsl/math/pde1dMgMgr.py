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
from pyimsl.util.imslUtils import MATH, checkForBoolean, checkForCallable, checkForList, fatalErrorCheck, loadimsl, toNumpyArray, checkForDict
from pyimsl.util.VersionFacade import VersionFacade
from numpy import double, dtype, shape, size
from ctypes import CFUNCTYPE, POINTER, byref, c_double, c_int, c_void_p
from pyimsl.math.pde1dMgState import pde1dMgState

IMSL_CART_COORDINATES = 14035
IMSL_CYL_COORDINATES = 14036
IMSL_SPH_COORDINATES = 14037
IMSL_TIME_SMOOTHING = 14038
IMSL_SPATIAL_SMOOTHING = 14039
IMSL_MONITOR_REGULARIZING = 14040
IMSL_MAX_BDF_ORDER = 14022
IMSL_USER_FACTOR_SOLVE = 14046
IMSL_INITIAL_CONDITIONS = 14048
IMSL_INITIAL_CONDITIONS_W_DATA = 14049
imslmath = loadimsl(MATH)

# Legal values for task
PDE_INITIALIZE = 1
PDE_CHANGE = 2
PDE_RESET = 3


def pde1dMgMgr(task, state, cartCoordinates=None, cylCoordinates=None, sphCoordinates=None, timeSmoothing=None, spatialSmoothing=None, monitorRegularizing=None, maxBdfOrder=None, userFactorSolve=None, initialConditions=None, initialConditionsWData=None):
    VersionFacade.checkVersion(6)
    imslmath.imsl_d_pde_1d_mg_mgr.restype = None
    shape = []
    evalstring = 'imslmath.imsl_d_pde_1d_mg_mgr('
    evalstring += 'c_int(task)'
    evalstring += ','
    if (task == PDE_INITIALIZE):
        state_tmp = c_void_p()
    else:
        stateWrapper = state[0]
        state_tmp = stateWrapper.state
    evalstring += 'byref(state_tmp)'
    checkForBoolean(cartCoordinates, 'cartCoordinates')
    if (cartCoordinates):
        evalstring += ','
        evalstring += repr(IMSL_CART_COORDINATES)
    checkForBoolean(cylCoordinates, 'cylCoordinates')
    if (cylCoordinates):
        evalstring += ','
        evalstring += repr(IMSL_CYL_COORDINATES)
    checkForBoolean(sphCoordinates, 'sphCoordinates')
    if (sphCoordinates):
        evalstring += ','
        evalstring += repr(IMSL_SPH_COORDINATES)
    if not (timeSmoothing is None):
        evalstring += ','
        evalstring += repr(IMSL_TIME_SMOOTHING)
        evalstring += ','
        evalstring += 'c_double(timeSmoothing)'
    if not (spatialSmoothing is None):
        evalstring += ','
        evalstring += repr(IMSL_SPATIAL_SMOOTHING)
        evalstring += ','
        evalstring += 'c_double(spatialSmoothing)'
    if not (monitorRegularizing is None):
        evalstring += ','
        evalstring += repr(IMSL_MONITOR_REGULARIZING)
        evalstring += ','
        evalstring += 'c_double(monitorRegularizing)'
    if not (maxBdfOrder is None):
        evalstring += ','
        evalstring += repr(IMSL_MAX_BDF_ORDER)
        evalstring += ','
        evalstring += 'c_int(maxBdfOrder)'
    if not (userFactorSolve is None):
        evalstring += ','
        evalstring += repr(IMSL_USER_FACTOR_SOLVE)
        checkForDict(userFactorSolve, 'userFactorSolve', ['fac', 'sol'])
        evalstring += ','
        tmp_userFactorSolve_fac_param = userFactorSolve['fac']
        checkForCallable(tmp_userFactorSolve_fac_param, 'fac')
        TMP_USERFACTORSOLVE_FAC = CFUNCTYPE(
            c_int, c_int, c_int, POINTER(c_double))
        tmp_userFactorSolve_fac = TMP_USERFACTORSOLVE_FAC(
            tmp_userFactorSolve_fac_param)
        evalstring += 'tmp_userFactorSolve_fac'
        evalstring += ','
        tmp_userFactorSolve_sol_param = userFactorSolve['sol']
        checkForCallable(tmp_userFactorSolve_sol_param, 'sol')
        TMP_USERFACTORSOLVE_SOL = CFUNCTYPE(
            c_void_p, c_int, c_int, POINTER(c_double), POINTER(c_double))
        tmp_userFactorSolve_sol = TMP_USERFACTORSOLVE_SOL(
            tmp_userFactorSolve_sol_param)
        evalstring += 'tmp_userFactorSolve_sol'
    if not (initialConditions is None):
        evalstring += ','
        evalstring += repr(IMSL_INITIAL_CONDITIONS)
        evalstring += ','
        checkForCallable(initialConditions, 'initialConditions')
        TMP_INITIALCONDITIONS_INITIALCONDITIONS = CFUNCTYPE(
            c_void_p, c_int, c_int, POINTER(c_double))
        tmp_initialConditions_initialConditions = TMP_INITIALCONDITIONS_INITIALCONDITIONS(
            initialConditions)
        # print "initialConditionsWData_data_tmp=",initialConditions
        # print "tmp_initialConditions_initialConditions=",tmp_initialConditions_initialConditions
        # print "TMP_INITIALCONDITIONS_INITIALCONDITIONS=",TMP_INITIALCONDITIONS_INITIALCONDITIONS
        evalstring += 'tmp_initialConditions_initialConditions'
    if not (initialConditionsWData is None):
        evalstring += ','
        evalstring += repr(IMSL_INITIAL_CONDITIONS_W_DATA)
        checkForDict(initialConditionsWData, 'initialConditionsWData', [
                     'initialConditionsWData', 'data'])
        evalstring += ','
        tmp_initialConditionsWData_initialConditionsWData_param = initialConditionsWData[
            'initialConditionsWData']
        checkForCallable(
            tmp_initialConditionsWData_initialConditionsWData_param, 'initialConditionsWData')
        TMP_INITIALCONDITIONSWDATA_INITIALCONDITIONSWDATA = CFUNCTYPE(
            c_void_p, c_int, c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double))
        tmp_initialConditionsWData_initialConditionsWData = TMP_INITIALCONDITIONSWDATA_INITIALCONDITIONSWDATA(
            tmp_initialConditionsWData_initialConditionsWData_param)
        evalstring += 'tmp_initialConditionsWData_initialConditionsWData'
        evalstring += ','
        initialConditionsWData_data_tmp = initialConditionsWData['data']
        initialConditionsWData_data_tmp = toNumpyArray(
            initialConditionsWData_data_tmp, 'data', shape=shape, dtype='double')
        evalstring += 'initialConditionsWData_data_tmp.ctypes.data_as(c_void_p)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if (task == PDE_INITIALIZE):
        stateWrapper = pde1dMgState(state_tmp)
        state[:] = []
        state.append(stateWrapper)
    if not (initialConditions is None):
        state.append(initialConditions)
        state.append(tmp_initialConditions_initialConditions)
        # state.append(timeSmoothing)
        # stateWrapper.__initialConditionsFcn__=initialConditions
        # stateWrapper.__tmpInitialConditionsFcn__=tmp_initialConditions_initialConditions
        # TODO: figure out why the following function are not getting called.
        # For some reason calls to the following functions
        # never happen.  I added a print statement to the
        # setter functions but it never is printed??.
        # stateWrapper._setInitialConditionsFcn
        # (initialConditions)
        # stateWrapper.setTmpInitialConditionsFcn
        # (tmp_initialConditions_initialConditions)
    if not (userFactorSolve is None):
        state.append(tmp_userFactorSolve_fac_param)
        state.append(tmp_userFactorSolve_sol_param)
        state.append(tmp_userFactorSolve_fac)
        state.append(tmp_userFactorSolve_fac)
        # stateWrapper._setUserFactorSolveFcn
        # (tmp_userFactorSolve_fac,
        # tmp_userFactorSolve_sol)
    if (task == PDE_RESET):
        stateWrapper.reset()
        state[:] = []
    return
