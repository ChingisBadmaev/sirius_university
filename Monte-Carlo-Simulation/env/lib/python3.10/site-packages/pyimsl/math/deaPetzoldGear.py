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
from pyimsl.util.imslUtils import MATH, checkForBoolean, checkForCallable, checkForList, fatalErrorCheck, loadimsl, toNumpyArray, checkForDict, processRet
from pyimsl.util.VersionFacade import VersionFacade
from numpy import double, dtype, ndarray, shape, size
from ctypes import CFUNCTYPE, POINTER, byref, c_double, c_int, c_void_p
from pyimsl.math.DeaPGState import DeaPGState
from pyimsl.util.Translator import Translator

IMSL_ATOL_RTOL_ARRAYS = 14010
IMSL_ATOL_RTOL_SCALARS = 14017
IMSL_MAX_NUMBER_STEPS = 10077
IMSL_MAX_STEP = 10111
IMSL_ALL_NONNEGATIVE = 14013
IMSL_BDF_ORDER_NEXT_STEP = 14026
IMSL_BDF_ORDER_PREVIOUS_STEP = 14027
IMSL_NSTEPS_TAKEN = 14028
IMSL_NFCN = 10082
IMSL_NFCNJ = 10312
IMSL_NERROR_TEST_FAILURES = 14024
IMSL_NCONV_TEST_FAILURES = 14025
IMSL_CONDITION = 10270
imslmath = loadimsl(MATH)


def deaPetzoldGear(t, tend, y, yprime, state, gcn, atolRtolArrays=None, atolRtolScalars=None, maxNumberSteps=None, maxStep=None, allNonnegative=None, bdfOrderNextStep=None, bdfOrderPreviousStep=None, nstepsTaken=None, nfcn=None, nfcnj=None, nerrorTestFailures=None, nconvTestFailures=None, condition=None):
    """ Solves a first order differential-algebraic system of equations, g(t, y, y') = 0, using the Petzold-Gear BDF method.
    """
    VersionFacade.checkVersion(6)
    if (state[0] is None) or (state[0].state is None):
        errStr = Translator.getString("dpgnotavailable")
        raise ValueError(errStr)
    if (not(isinstance(state[0], DeaPGState))):
        errStr = Translator.getString("statcorrupt")
        raise ValueError(errStr)
    imslmath.imsl_d_dea_petzold_gear.restype = c_int
    shape = []
    evalstring = 'imslmath.imsl_d_dea_petzold_gear('
    evalstring += 'c_int(neq)'
    evalstring += ','
    t_tmp = t[0]
    if (not(isinstance(t_tmp, c_double))):
        t_tmp = c_double(t[0])
    evalstring += 'byref(t_tmp)'
    evalstring += ','
    evalstring += 'c_double(tend)'
    evalstring += ','
    y_tmp = toNumpyArray(y, 'y', shape=shape,
                         dtype='double', expectedShape=(0))
    evalstring += 'y_tmp.ctypes.data_as(c_void_p)'
    neq = shape[0]
    evalstring += ','
    yprime_tmp = toNumpyArray(
        yprime, 'yprime', shape=shape, dtype='double', expectedShape=(neq))
    evalstring += 'yprime_tmp.ctypes.data_as(c_void_p)'
    evalstring += ','
    evalstring += 'state[0].state'
    evalstring += ','
    if (gcn is None):
        tmp_gcn = None
    else:
        checkForCallable(gcn, 'gcn')
        TMP_GCN = CFUNCTYPE(c_int, c_int, c_double, POINTER(
            c_double), POINTER(c_double), POINTER(c_double))
        tmp_gcn = TMP_GCN(gcn)
        # keep a reference to the fcn in case it is used by the state variable
        state.append(gcn)
        state.append(tmp_gcn)
    evalstring += 'tmp_gcn'
    if not (atolRtolArrays is None):
        evalstring += ','
        evalstring += repr(IMSL_ATOL_RTOL_ARRAYS)
        checkForDict(atolRtolArrays, 'atolRtolArrays', ['atol', 'rtol'])
        evalstring += ','
        atolRtolArrays_atol_tmp = atolRtolArrays['atol']
        atolRtolArrays_atol_tmp = toNumpyArray(
            atolRtolArrays_atol_tmp, 'atol', shape=shape, dtype='double', expectedShape=(neq))
        evalstring += 'atolRtolArrays_atol_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        atolRtolArrays_rtol_tmp = atolRtolArrays['rtol']
        atolRtolArrays_rtol_tmp = toNumpyArray(
            atolRtolArrays_rtol_tmp, 'rtol', shape=shape, dtype='double', expectedShape=(neq))
        evalstring += 'atolRtolArrays_rtol_tmp.ctypes.data_as(c_void_p)'
    if not (atolRtolScalars is None):
        evalstring += ','
        evalstring += repr(IMSL_ATOL_RTOL_SCALARS)
        checkForDict(atolRtolScalars, 'atolRtolScalars', ['atol', 'rtol'])
        evalstring += ','
        atolRtolScalars_atol_tmp = atolRtolScalars['atol']
        evalstring += 'c_double(atolRtolScalars_atol_tmp)'
        evalstring += ','
        atolRtolScalars_rtol_tmp = atolRtolScalars['rtol']
        evalstring += 'c_double(atolRtolScalars_rtol_tmp)'
    if not (maxNumberSteps is None):
        evalstring += ','
        evalstring += repr(IMSL_MAX_NUMBER_STEPS)
        evalstring += ','
        evalstring += 'c_int(maxNumberSteps)'
    if not (maxStep is None):
        evalstring += ','
        evalstring += repr(IMSL_MAX_STEP)
        evalstring += ','
        evalstring += 'c_double(maxStep)'
    checkForBoolean(allNonnegative, 'allNonnegative')
    if (allNonnegative):
        evalstring += ','
        evalstring += repr(IMSL_ALL_NONNEGATIVE)
    if not (bdfOrderNextStep is None):
        evalstring += ','
        evalstring += repr(IMSL_BDF_ORDER_NEXT_STEP)
        evalstring += ','
        evalstring += 'c_int(bdfOrderNextStep)'
    if not (bdfOrderPreviousStep is None):
        evalstring += ','
        evalstring += repr(IMSL_BDF_ORDER_PREVIOUS_STEP)
        checkForList(bdfOrderPreviousStep, 'bdfOrderPreviousStep')
        evalstring += ','
        bdfOrderPreviousStep_prevBdfOrder_tmp = c_int()
        evalstring += 'byref(bdfOrderPreviousStep_prevBdfOrder_tmp)'
    if not (nstepsTaken is None):
        evalstring += ','
        evalstring += repr(IMSL_NSTEPS_TAKEN)
        checkForList(nstepsTaken, 'nstepsTaken')
        evalstring += ','
        nstepsTaken_nstepsTaken_tmp = c_int()
        evalstring += 'byref(nstepsTaken_nstepsTaken_tmp)'
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
    if not (nerrorTestFailures is None):
        evalstring += ','
        evalstring += repr(IMSL_NERROR_TEST_FAILURES)
        checkForList(nerrorTestFailures, 'nerrorTestFailures')
        evalstring += ','
        nerrorTestFailures_nerrorTestFailures_tmp = c_int()
        evalstring += 'byref(nerrorTestFailures_nerrorTestFailures_tmp)'
    if not (nconvTestFailures is None):
        evalstring += ','
        evalstring += repr(IMSL_NCONV_TEST_FAILURES)
        checkForList(nconvTestFailures, 'nconvTestFailures')
        evalstring += ','
        nconvTestFailures_nconvTestFailures_tmp = c_int()
        evalstring += 'byref(nconvTestFailures_nconvTestFailures_tmp)'
    if not (condition is None):
        evalstring += ','
        evalstring += repr(IMSL_CONDITION)
        checkForList(condition, 'condition')
        evalstring += ','
        condition_condition_tmp = c_double()
        evalstring += 'byref(condition_condition_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    processRet(t_tmp, inout=True, shape=(1), pyvar=t)
    processRet(y_tmp, inout=True, shape=(neq), pyvar=y)
    processRet(yprime_tmp, inout=True, shape=(neq), pyvar=yprime)
    if not (bdfOrderPreviousStep is None):
        processRet(bdfOrderPreviousStep_prevBdfOrder_tmp,
                   shape=(1), pyvar=bdfOrderPreviousStep)
    if not (nstepsTaken is None):
        processRet(nstepsTaken_nstepsTaken_tmp, shape=(1), pyvar=nstepsTaken)
    if not (nfcn is None):
        processRet(nfcn_nfcn_tmp, shape=(1), pyvar=nfcn)
    if not (nfcnj is None):
        processRet(nfcnj_nfcnj_tmp, shape=(1), pyvar=nfcnj)
    if not (nerrorTestFailures is None):
        processRet(nerrorTestFailures_nerrorTestFailures_tmp,
                   shape=(1), pyvar=nerrorTestFailures)
    if not (nconvTestFailures is None):
        processRet(nconvTestFailures_nconvTestFailures_tmp,
                   shape=(1), pyvar=nconvTestFailures)
    if not (condition is None):
        processRet(condition_condition_tmp, shape=(1), pyvar=condition)
    return result
