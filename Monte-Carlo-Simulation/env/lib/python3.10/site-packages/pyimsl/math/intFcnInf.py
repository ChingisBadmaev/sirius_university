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
from pyimsl.util.imslUtils import MATH, checkForCallable, checkForList, fatalErrorCheck, loadimsl, toNumpyArray, processRet
from numpy import double, dtype, shape, size
from ctypes import CFUNCTYPE, byref, c_double, c_int, c_void_p

IMSL_ERR_ABS = 10010
IMSL_ERR_REL = 10011
IMSL_ERR_EST = 10020
IMSL_MAX_SUBINTER = 10021
IMSL_N_SUBINTER = 10022
IMSL_N_EVALS = 10023
IMSL_FCN_W_DATA = 13101
# IMSL_QUAD
ALG = 1
ALG_LEFT_LOG = 2
ALG_RIGHT_LOG = 3
ALG_LOG = 4
INF_BOUND = 5
BOUND_INF = 6
INF_INF = 7
COS = 8
SIN = 9
imslmath = loadimsl(MATH)


def intFcnInf(fcn, bound, interval, errAbs=None, errRel=None, errEst=None, maxSubinter=None, nSubinter=None, nEvals=None, fcnWData=None):
    """ Integrates a function over an infinite or semi-infinite interval.
    """
    imslmath.imsl_d_int_fcn_inf.restype = c_double
    shape = []
    evalstring = 'imslmath.imsl_d_int_fcn_inf('
    checkForCallable(fcn, 'fcn')
    TMP_FCN = CFUNCTYPE(c_double, c_double)
    tmp_fcn = TMP_FCN(fcn)
    evalstring += 'tmp_fcn'
    evalstring += ','
    evalstring += 'c_double(bound)'
    evalstring += ','
    evalstring += 'c_int(interval)'
    if not (errAbs is None):
        evalstring += ','
        evalstring += repr(IMSL_ERR_ABS)
        evalstring += ','
        evalstring += 'c_double(errAbs)'
    if not (errRel is None):
        evalstring += ','
        evalstring += repr(IMSL_ERR_REL)
        evalstring += ','
        evalstring += 'c_double(errRel)'
    if not (errEst is None):
        evalstring += ','
        evalstring += repr(IMSL_ERR_EST)
        checkForList(errEst, 'errEst')
        evalstring += ','
        errEst_errEst_tmp = c_double()
        evalstring += 'byref(errEst_errEst_tmp)'
    if not (maxSubinter is None):
        evalstring += ','
        evalstring += repr(IMSL_MAX_SUBINTER)
        evalstring += ','
        evalstring += 'c_int(maxSubinter)'
    if not (nSubinter is None):
        evalstring += ','
        evalstring += repr(IMSL_N_SUBINTER)
        checkForList(nSubinter, 'nSubinter')
        evalstring += ','
        nSubinter_nSubinter_tmp = c_int()
        evalstring += 'byref(nSubinter_nSubinter_tmp)'
    if not (nEvals is None):
        evalstring += ','
        evalstring += repr(IMSL_N_EVALS)
        checkForList(nEvals, 'nEvals')
        evalstring += ','
        nEvals_nEvals_tmp = c_int()
        evalstring += 'byref(nEvals_nEvals_tmp)'
    if not (fcnWData is None):
        evalstring += ','
        evalstring += repr(IMSL_FCN_W_DATA)
        checkForDict(fcnWData, 'fcnWData', ['fcn', 'x', 'data'])
        evalstring += ','
        tmp_fcnWData_fcnWData_param = fcnWData['fcn']
        checkForCallable(tmp_fcnWData_fcnWData_param, 'fcnWData')
        TMP_FCNWDATA_FCNWDATA = CFUNCTYPE(
            c_double, c_double, POINTER(c_double))
        tmp_fcnWData_fcnWData = TMP_FCNWDATA_FCNWDATA(
            tmp_fcnWData_fcnWData_param)
        evalstring += 'tmp_fcnWData_fcnWData'
        evalstring += ','
        fcnWData_x_tmp = fcnWData['x']
        evalstring += 'c_double(fcnWData_x_tmp)'
        evalstring += ','
        fcnWData_data_tmp = fcnWData['data']
        fcnWData_data_tmp = toNumpyArray(
            fcnWData_data_tmp, 'data', shape=shape, dtype='double')
        evalstring += 'fcnWData_data_tmp.ctypes.data_as(c_void_p)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (errEst is None):
        processRet(errEst_errEst_tmp, shape=1, pyvar=errEst)
    if not (nSubinter is None):
        processRet(nSubinter_nSubinter_tmp, shape=1, pyvar=nSubinter)
    if not (nEvals is None):
        processRet(nEvals_nEvals_tmp, shape=1, pyvar=nEvals)
    return result
