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
from numpy import double, dtype, ndim, shape, size
from ctypes import CFUNCTYPE, POINTER, byref, c_double, c_int, c_void_p

IMSL_ERR_ABS = 10010
IMSL_ERR_REL = 10011
IMSL_ERR_EST = 10020
IMSL_MAX_EVALS = 10277
IMSL_BASE = 12100
IMSL_SKIP = 12101
IMSL_FCN_W_DATA = 13101
imslmath = loadimsl(MATH)


def intFcnQmc(fcn, a, b, errAbs=None, errRel=None, errEst=None, maxEvals=None, base=None, skip=None, fcnWData=None):
    """ Integrates a function on a hyper-rectangle using a quasi-Monte Carlo method.
    """
    imslmath.imsl_d_int_fcn_qmc.restype = c_double
    shape = []
    evalstring = 'imslmath.imsl_d_int_fcn_qmc('
    checkForCallable(fcn, 'fcn')
    TMP_FCN = CFUNCTYPE(c_double, c_int, POINTER(c_double))
    tmp_fcn = TMP_FCN(fcn)
    evalstring += 'tmp_fcn'
    evalstring += ','
    evalstring += 'c_int(ndim)'
    evalstring += ','
    a = toNumpyArray(a, 'a', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'a.ctypes.data_as(c_void_p)'
    ndim = shape[0]
    evalstring += ','
    b = toNumpyArray(b, 'b', shape=shape, dtype='double', expectedShape=(ndim))
    evalstring += 'b.ctypes.data_as(c_void_p)'
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
    if not (maxEvals is None):
        evalstring += ','
        evalstring += repr(IMSL_MAX_EVALS)
        evalstring += ','
        evalstring += 'c_int(maxEvals)'
    if not (base is None):
        evalstring += ','
        evalstring += repr(IMSL_BASE)
        evalstring += ','
        evalstring += 'c_int(base)'
    if not (skip is None):
        evalstring += ','
        evalstring += repr(IMSL_SKIP)
        evalstring += ','
        evalstring += 'c_int(skip)'
    if not (fcnWData is None):
        evalstring += ','
        evalstring += repr(IMSL_FCN_W_DATA)
        checkForList(fcnWData, 'fcnWData', size=3)
        evalstring += ','
        tmp_fcnWData_fcnWData_param = fcnWData[0]
        checkForCallable(tmp_fcnWData_fcnWData_param, 'fcnWData')
        TMP_FCNWDATA_FCNWDATA = CFUNCTYPE(
            c_double, c_int, POINTER(c_double), POINTER(c_double))
        tmp_fcnWData_fcnWData = TMP_FCNWDATA_FCNWDATA(
            tmp_fcnWData_fcnWData_param)
        evalstring += 'tmp_fcnWData_fcnWData'
        evalstring += ','
        fcnWData_x_tmp = fcnWData[1]
        evalstring += 'c_double(fcnWData_x_tmp)'
        evalstring += ','
        fcnWData_data_tmp = fcnWData[2]
        fcnWData_data_tmp = toNumpyArray(
            fcnWData_data_tmp, 'data', shape=shape, dtype='double')
        evalstring += 'fcnWData_data_tmp.ctypes.data_as(c_void_p)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (errEst is None):
        processRet(errEst_errEst_tmp, shape=1, pyvar=errEst)
    return result
