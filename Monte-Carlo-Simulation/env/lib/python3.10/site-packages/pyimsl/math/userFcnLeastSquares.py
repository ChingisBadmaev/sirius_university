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
from pyimsl.util.imslUtils import MATH, checkForCallable, checkForList, checkForDict, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, shape, size
from ctypes import CFUNCTYPE, POINTER, byref, c_double, c_int, c_void_p

IMSL_INTERCEPT = 10144
IMSL_SSE = 10145
IMSL_WEIGHTS = 10141
IMSL_FCN_W_DATA = 13101
imslmath = loadimsl(MATH)


def userFcnLeastSquares(fcn, nbasis, xdata, ydata, intercept=None, sse=None, weights=None, fcnWData=None):
    """ Computes a least-squares fit using user-supplied functions.
    """
    imslmath.imsl_d_user_fcn_least_squares.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslmath.imsl_d_user_fcn_least_squares('
    checkForCallable(fcn, 'fcn')
    TMP_FCN = CFUNCTYPE(c_double, c_int, c_double)
    tmp_fcn = TMP_FCN(fcn)
    evalstring += 'tmp_fcn'
    evalstring += ','
    evalstring += 'c_int(nbasis)'
    evalstring += ','
    evalstring += 'c_int(ndata)'
    evalstring += ','
    xdata = toNumpyArray(xdata, 'xdata', shape=shape,
                         dtype='double', expectedShape=(0))
    evalstring += 'xdata.ctypes.data_as(c_void_p)'
    ndata = shape[0]
    evalstring += ','
    ydata = toNumpyArray(ydata, 'ydata', shape=shape,
                         dtype='double', expectedShape=(ndata))
    evalstring += 'ydata.ctypes.data_as(c_void_p)'
    if not (intercept is None):
        evalstring += ','
        evalstring += repr(IMSL_INTERCEPT)
        checkForList(intercept, 'intercept')
        evalstring += ','
        intercept_intercept_tmp = c_double()
        evalstring += 'byref(intercept_intercept_tmp)'
    if not (sse is None):
        evalstring += ','
        evalstring += repr(IMSL_SSE)
        checkForList(sse, 'sse')
        evalstring += ','
        sse_ssqErr_tmp = c_double()
        evalstring += 'byref(sse_ssqErr_tmp)'
    if not (weights is None):
        evalstring += ','
        evalstring += repr(IMSL_WEIGHTS)
        evalstring += ','
        weights = toNumpyArray(
            weights, 'weights', shape=shape, dtype='double', expectedShape=(ndata))
        evalstring += 'weights.ctypes.data_as(c_void_p)'
    if not (fcnWData is None):
        evalstring += ','
        evalstring += repr(IMSL_FCN_W_DATA)
        checkForDict(fcnWData, 'fcnWData', ['fcn', 'data'])
        evalstring += ','
        tmp_fcnWData_fcnWData_param = fcnWData['fcn']
        checkForCallable(tmp_fcnWData_fcnWData_param, 'fcnWData')
        TMP_FCNWDATA_FCNWDATA = CFUNCTYPE(c_double, POINTER(c_double))
        tmp_fcnWData_fcnWData = TMP_FCNWDATA_FCNWDATA(
            tmp_fcnWData_fcnWData_param)
        evalstring += 'tmp_fcnWData_fcnWData'
        evalstring += ','
        fcnWData_data_tmp = fcnWData['data']
        fcnWData_data_tmp = toNumpyArray(
            fcnWData_data_tmp, 'data', shape=shape, dtype='double', expectedShape=(0))
        evalstring += 'fcnWData_data_tmp.ctypes.data_as(c_void_p)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (intercept is None):
        processRet(intercept_intercept_tmp, shape=1, pyvar=intercept)
    if not (sse is None):
        processRet(sse_ssqErr_tmp, shape=1, pyvar=sse)
    return processRet(result, shape=(nbasis), result=True)
