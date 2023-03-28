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
from pyimsl.math.DeaPGState import DeaPGState

IMSL_INITIAL_STEPSIZE = 11137
IMSL_T_BARRIER = 14029
IMSL_MAX_BDF_ORDER = 14022
IMSL_INITIAL_VALUES_INCONSISTENT = 14014
IMSL_JACOBIAN = 10118
IMSL_JACOBIAN_W_DATA = 13104
IMSL_GCN_W_DATA = 13100
IMSL_NORM_FCN = 14031
IMSL_NORM_FCN_W_DATA = 14032

# Legal values for task
DEA_INITIALIZE = 1
DEA_RESET = 3

imslmath = loadimsl(MATH)


def deaPetzoldGearMgr(task, state, initialStepsize=None, tBarrier=None, maxBdfOrder=None, initialValuesInconsistent=None, jacobian=None, normFcn=None):
    VersionFacade.checkVersion(6)
    imslmath.imsl_d_dea_petzold_gear_mgr.restype = None
    shape = []
    evalstring = 'imslmath.imsl_d_dea_petzold_gear_mgr('
    evalstring += 'c_int(task)'
    evalstring += ','
    if (task == DEA_INITIALIZE):
        state_tmp = c_void_p()
    else:
        stateWrapper = state[0]
        state_tmp = stateWrapper.state
    evalstring += 'byref(state_tmp)'
    if not (initialStepsize is None):
        evalstring += ','
        evalstring += repr(IMSL_INITIAL_STEPSIZE)
        evalstring += ','
        evalstring += 'c_double(initialStepsize)'
    if not (tBarrier is None):
        evalstring += ','
        evalstring += repr(IMSL_T_BARRIER)
        evalstring += ','
        evalstring += 'c_double(tBarrier)'
    if not (maxBdfOrder is None):
        evalstring += ','
        evalstring += repr(IMSL_MAX_BDF_ORDER)
        evalstring += ','
        evalstring += 'c_int(maxBdfOrder)'
    checkForBoolean(initialValuesInconsistent, 'initialValuesInconsistent')
    if (initialValuesInconsistent):
        evalstring += ','
        evalstring += repr(IMSL_INITIAL_VALUES_INCONSISTENT)
    if not (jacobian is None):
        evalstring += ','
        evalstring += repr(IMSL_JACOBIAN)
        evalstring += ','
        jgcn = jacobian
        checkForCallable(jgcn, 'jgcn')
        TMP_JACOBIAN_JGCN = CFUNCTYPE(c_void_p, c_int, c_double, POINTER(
            c_double), POINTER(c_double), c_double, POINTER(c_double))
        tmp_jacobian_jgcn = TMP_JACOBIAN_JGCN(jgcn)
        evalstring += 'tmp_jacobian_jgcn'
    if not (normFcn is None):
        evalstring += ','
        evalstring += repr(IMSL_NORM_FCN)
        evalstring += ','
        checkForCallable(normFcn, 'normFcn')
        TMP_NORMFCN_NORMFCN = CFUNCTYPE(
            c_double, c_int, POINTER(c_double), POINTER(c_double))
        tmp_normFcn_normFcn = TMP_NORMFCN_NORMFCN(normFcn)
        evalstring += 'tmp_normFcn_normFcn'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if (task == DEA_INITIALIZE):
        stateWrapper = DeaPGState(state_tmp)
        state[:] = []
        state.append(stateWrapper)
    if not (jacobian is None):
        state.append(jacobian)
        state.append(tmp_jacobian_jgcn)
    if not (normFcn is None):
        state.append(normFcn)
        state.append(tmp_normFcn_normFcn)
    if (task == DEA_RESET):
        stateWrapper.setState(None)
        state[:] = []
    return
