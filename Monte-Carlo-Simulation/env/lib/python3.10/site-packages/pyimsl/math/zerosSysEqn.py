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
from pyimsl.util.imslUtils import MATH, checkForCallable, checkForList, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, shape, size
from ctypes import CFUNCTYPE, POINTER, byref, c_double, c_int, c_void_p

IMSL_XGUESS = 10100
IMSL_JACOBIAN = 10118
IMSL_ERR_REL = 10011
IMSL_MAX_ITN = 10113
IMSL_FNORM = 10119
IMSL_FCN_W_DATA = 13101
IMSL_JACOBIAN_W_DATA = 13104
imslmath = loadimsl(MATH)


def zerosSysEqn(fcn, n, xguess=None, jacobian=None, errRel=None, maxItn=None, fnorm=None, fcnWData=None, jacobianWData=None):
    """ Solves a system of n nonlinear equations f(x) = 0 using a modified Powell hybrid algorithm.
    """
    imslmath.imsl_d_zeros_sys_eqn.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslmath.imsl_d_zeros_sys_eqn('
    checkForCallable(fcn, 'fcn')
    TMP_FCN = CFUNCTYPE(c_void_p, c_int, POINTER(c_double), POINTER(c_double))
    tmp_fcn = TMP_FCN(fcn)
    evalstring += 'tmp_fcn'
    evalstring += ','
    evalstring += 'c_int(n)'
    if not (xguess is None):
        evalstring += ','
        evalstring += repr(IMSL_XGUESS)
        evalstring += ','
        xguess = toNumpyArray(xguess, 'xguess', shape=shape,
                              dtype='double', expectedShape=(n))
        evalstring += 'xguess.ctypes.data_as(c_void_p)'
    if not (jacobian is None):
        evalstring += ','
        evalstring += repr(IMSL_JACOBIAN)
        evalstring += ','
        checkForCallable(jacobian, 'jacobian')
        TMP_JACOBIAN_JACOBIAN = CFUNCTYPE(
            c_void_p, c_int, POINTER(c_double), POINTER(c_double))
        tmp_jacobian_jacobian = TMP_JACOBIAN_JACOBIAN(jacobian)
        evalstring += 'tmp_jacobian_jacobian'
    if not (errRel is None):
        evalstring += ','
        evalstring += repr(IMSL_ERR_REL)
        evalstring += ','
        evalstring += 'c_double(errRel)'
    if not (maxItn is None):
        evalstring += ','
        evalstring += repr(IMSL_MAX_ITN)
        evalstring += ','
        evalstring += 'c_int(maxItn)'
    if not (fnorm is None):
        evalstring += ','
        evalstring += repr(IMSL_FNORM)
        checkForList(fnorm, 'fnorm')
        evalstring += ','
        fnorm_fnorm_tmp = c_double()
        evalstring += 'byref(fnorm_fnorm_tmp)'
    if not (fcnWData is None):
        evalstring += ','
        evalstring += repr(IMSL_FCN_W_DATA)
        checkForDict(fcnWData, 'fcnWData', ['fcn', 'data'])
        evalstring += ','
        tmp_fcnWData_fcnWData_param = fcnWData['fcn']
        checkForCallable(tmp_fcnWData_fcnWData_param, 'fcnWData')
        TMP_FCNWDATA_FCNWDATA = CFUNCTYPE(c_void_p, c_int, POINTER(
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
        checkForDict(jacobianWData, 'jacobianWData', ['jacobian', 'data'])
        checkForList(jacobianWData, 'jacobianWData', size=2)
        evalstring += ','
        tmp_jacobianWData_jacobianWData_param = jacobianWData['jacobian']
        checkForCallable(
            tmp_jacobianWData_jacobianWData_param, 'jacobianWData')
        TMP_JACOBIANWDATA_JACOBIANWDATA = CFUNCTYPE(
            c_void_p, c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double))
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
    if not (fnorm is None):
        processRet(fnorm_fnorm_tmp, shape=1, pyvar=fnorm)
    return processRet(result, shape=(n), result=True)
