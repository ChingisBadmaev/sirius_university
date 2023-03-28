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
from pyimsl.util.imslUtils import *
from numpy import array, empty
from ctypes import *
from pyimsl.util.VersionFacade import VersionFacade

IMSL_FCN_INIT = 15030
IMSL_FCN_FORCE = 15032
IMSL_ATOL_RTOL_SCALARS = 14017
IMSL_ATOL_RTOL_ARRAYS = 14010
IMSL_NDEGREE = 15034
IMSL_TDEPEND = 15035
IMSL_MAX_STEP = 10111
IMSL_INITIAL_STEPSIZE = 11137
IMSL_MAX_NUMBER_STEPS = 10077
IMSL_STEP_CONTROL = 15036
IMSL_MAX_BDF_ORDER = 14022
IMSL_T_BARRIER = 14029
IMSL_ISTATE = 15037
IMSL_EVALS = 15038

# lets keep these around just to be safe but does not make a difference
TMP_FCNFKCFIV = None
tmp_fcnFkbcp = None
TMP_FCNFORCE_FCNFORCE = None
tmp_fcnForce_fcnForce = None

imslmath = loadimsl(MATH)


def feynmanKac(nlbcd, nrbcd, xgrid, tgrid, fcnFkcfiv, fcnFkbcp, y, yPrime,
               fcnInit=None, fcnForce=None, atolRtolScalars=None, atolRtolArrays=None,
               ndegree=None, tdepend=None, maxStep=None, initialStepsize=None,
               maxNumberSteps=None, stepControl=None, maxBdfOrder=None, tBarrier=None,
               istate=None, evals=None):
    VersionFacade.checkVersion(7)
    imslmath.imsl_d_feynman_kac.restype = None
    shape = []
    evalstring = 'imslmath.imsl_d_feynman_kac('
    evalstring += 'c_int(nxgrid)'
    evalstring += ','
    evalstring += 'c_int(ntgrid)'
    evalstring += ','
    evalstring += 'c_int(nlbcd)'
    evalstring += ','
    evalstring += 'c_int(nrbcd)'
    evalstring += ','
    xgrid = toNumpyArray(xgrid, 'xgrid', shape=shape,
                         dtype='double', expectedShape=(0))
    evalstring += 'xgrid.ctypes.data_as(c_void_p)'
    nxgrid = shape[0]
    evalstring += ','
    tgrid = toNumpyArray(tgrid, 'tgrid', shape=shape,
                         dtype='double', expectedShape=(0))
    evalstring += 'tgrid.ctypes.data_as(c_void_p)'
    ntgrid = shape[0]
    evalstring += ','
    checkForCallable(fcnFkcfiv, 'fcnFkcfiv')
    TMP_FCNFKCFIV = CFUNCTYPE(None, c_double, c_double,
                              POINTER(c_int), POINTER(c_double))
    tmp_fcnFkcfiv = TMP_FCNFKCFIV(fcnFkcfiv)
    evalstring += 'tmp_fcnFkcfiv'
    evalstring += ','
    checkForCallable(fcnFkbcp, 'fcnFkbcp')
    TMP_FCNFKBCP = CFUNCTYPE(None, c_int, c_double,
                             POINTER(c_int), POINTER(c_double))
    tmp_fcnFkbcp = TMP_FCNFKBCP(fcnFkbcp)
    evalstring += 'tmp_fcnFkbcp'
    evalstring += ','
    # y and yPrime are output but memory must be allocated outside CNL
    y_tmp = empty((ntgrid + 1) * (3 * nxgrid))
    evalstring += 'y_tmp.ctypes.data_as(c_void_p)'
    evalstring += ','
    yPrime_tmp = empty((ntgrid + 1) * (3 * nxgrid))
    evalstring += 'yPrime_tmp.ctypes.data_as(c_void_p)'
    if not (fcnInit is None):
        evalstring += ','
        evalstring += repr(IMSL_FCN_INIT)
        evalstring += ','
        checkForCallable(fcnInit, 'fcnInit')
        TMP_FCNINIT_FCNINIT = CFUNCTYPE(c_void_p, c_int, c_int, POINTER(c_double), POINTER(c_double),
                                        c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double))
        tmp_fcnInit_fcnInit = TMP_FCNINIT_FCNINIT(fcnInit)
        evalstring += 'tmp_fcnInit_fcnInit'
    if not (fcnForce is None):
        evalstring += ','
        evalstring += repr(IMSL_FCN_FORCE)
        evalstring += ','
        checkForCallable(fcnForce, 'fcnForce')
        TMP_FCNFORCE_FCNFORCE = CFUNCTYPE(c_void_p, c_int, c_int, c_int, POINTER(c_double),
                                          c_double, c_double, POINTER(c_double), POINTER(
                                              c_double), POINTER(c_double),
                                          POINTER(c_double), POINTER(c_double))
        tmp_fcnForce_fcnForce = TMP_FCNFORCE_FCNFORCE(fcnForce)
        evalstring += 'tmp_fcnForce_fcnForce'
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
    if not (atolRtolArrays is None):
        evalstring += ','
        evalstring += repr(IMSL_ATOL_RTOL_ARRAYS)
        checkForDict(atolRtolArrays, 'atolRtolArrays', ['atol', 'rtol'])
        evalstring += ','
        atolRtolArrays_atol_tmp = atolRtolArrays['atol']
        atolRtolArrays_atol_tmp = toNumpyArray(
            atolRtolArrays_atol_tmp, 'atol', shape=shape, dtype='double', expectedShape=(3 * nxgrid))
        evalstring += 'atolRtolArrays_atol_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        atolRtolArrays_rtol_tmp = atolRtolArrays['rtol']
        atolRtolArrays_rtol_tmp = toNumpyArray(
            atolRtolArrays_rtol_tmp, 'rtol', shape=shape, dtype='double', expectedShape=(3 * nxgrid))
        evalstring += 'atolRtolArrays_rtol_tmp.ctypes.data_as(c_void_p)'
    if not (ndegree is None):
        evalstring += ','
        evalstring += repr(IMSL_NDEGREE)
        evalstring += ','
        evalstring += 'c_int(ndegree)'
    if not (tdepend is None):
        evalstring += ','
        evalstring += repr(IMSL_TDEPEND)
        evalstring += ','
        # tdepend = toNumpyArray(tdepend, 'tdepend', shape=shape, dtype='int', expectedShape=(7))
        # evalstring +='tdepend.ctypes.data_as(c_void_p)'
        tdepend_tdepend_tmp = [0, 0, 0, 0, 0, 0, 0]
        tdepend_tdepend_tmp = toNumpyArray(
            tdepend_tdepend_tmp, 'tdepend', shape=(7), dtype='int')
        evalstring += 'tdepend_tdepend_tmp.ctypes.data_as(c_void_p)'
    if not (maxStep is None):
        evalstring += ','
        evalstring += repr(IMSL_MAX_STEP)
        evalstring += ','
        evalstring += 'c_double(maxStep)'
    if not (initialStepsize is None):
        evalstring += ','
        evalstring += repr(IMSL_INITIAL_STEPSIZE)
        evalstring += ','
        evalstring += 'c_double(initialStepsize)'
    if not (maxNumberSteps is None):
        evalstring += ','
        evalstring += repr(IMSL_MAX_NUMBER_STEPS)
        evalstring += ','
        evalstring += 'c_int(maxNumberSteps)'
    if not (stepControl is None):
        evalstring += ','
        evalstring += repr(IMSL_STEP_CONTROL)
        evalstring += ','
        evalstring += 'c_int(stepControl)'
    if not (maxBdfOrder is None):
        evalstring += ','
        evalstring += repr(IMSL_MAX_BDF_ORDER)
        evalstring += ','
        evalstring += 'c_int(maxBdfOrder)'
    if not (tBarrier is None):
        evalstring += ','
        evalstring += repr(IMSL_T_BARRIER)
        evalstring += ','
        evalstring += 'c_double(tBarrier)'
    if not (istate is None):
        evalstring += ','
        evalstring += repr(IMSL_ISTATE)
        checkForList(istate, 'istate')
        evalstring += ','
        # istate_istate_tmp = POINTER(c_int)(c_int())
        # evalstring += 'byref(istate_istate_tmp)'
        istate_istate_tmp = [0, 0, 0, 0, 0, 0, 0]
        istate_istate_tmp = toNumpyArray(
            istate_istate_tmp, 'istate', shape=(7), dtype='int')
        evalstring += 'istate_istate_tmp.ctypes.data_as(c_void_p)'
    if not (evals is None):
        evalstring += ','
        evalstring += repr(IMSL_EVALS)
        checkForList(evals, 'evals')
        evalstring += ','
        # evals_nval_tmp = POINTER(c_int)(c_int())
        # evalstring += 'byref(evals_nval_tmp)'
        evals_evals_tmp = [0, 0, 0]
        evals_evals_tmp = toNumpyArray(
            evals_evals_tmp, 'evals', shape=(3), dtype='int')
        evalstring += 'evals_evals_tmp.ctypes.data_as(c_void_p)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (y is None):
        processRet(y_tmp, shape=((ntgrid + 1), (3 * nxgrid)), pyvar=y)
    if not (yPrime is None):
        processRet(yPrime_tmp, shape=(
            (ntgrid + 1), (3 * nxgrid)), pyvar=yPrime)
    if not (istate is None):
        processRet(istate_istate_tmp, shape=(7), pyvar=istate)
    if not (tdepend is None):
        processRet(tdepend_tdepend_tmp, shape=(7), pyvar=tdepend)
    if not (evals is None):
        processRet(evals_evals_tmp, shape=(3), pyvar=evals)
    return
