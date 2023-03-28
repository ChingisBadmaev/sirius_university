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
from numpy import double, dtype, shape, size
from ctypes import CFUNCTYPE, POINTER, c_double, c_int, c_void_p

IMSL_ORDER = 10036
IMSL_INITIAL_STEPSIZE = 11137
IMSL_RELATIVE_ERROR = 11138
IMSL_FCN_W_DATA = 13101
imslmath = loadimsl(MATH)


def fcnDerivative(fcn, x, order=None, initialStepsize=None, relativeError=None, fcnWData=None):
    """ Computes the first, second, or third derivative of a user-supplied function.
    """
    imslmath.imsl_d_fcn_derivative.restype = c_double
    shape = []
    evalstring = 'imslmath.imsl_d_fcn_derivative('
    checkForCallable(fcn, 'fcn')
    TMP_FCN = CFUNCTYPE(c_double, c_double)
    tmp_fcn = TMP_FCN(fcn)
    evalstring += 'tmp_fcn'
    evalstring += ','
    evalstring += 'c_double(x)'
    if not (order is None):
        evalstring += ','
        evalstring += repr(IMSL_ORDER)
        evalstring += ','
        evalstring += 'c_int(order)'
    if not (initialStepsize is None):
        evalstring += ','
        evalstring += repr(IMSL_INITIAL_STEPSIZE)
        evalstring += ','
        evalstring += 'c_double(initialStepsize)'
    if not (relativeError is None):
        evalstring += ','
        evalstring += repr(IMSL_RELATIVE_ERROR)
        evalstring += ','
        evalstring += 'c_double(relativeError)'
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
    return result
