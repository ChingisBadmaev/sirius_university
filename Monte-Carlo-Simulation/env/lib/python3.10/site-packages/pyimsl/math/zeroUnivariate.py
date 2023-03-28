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

IMSL_FCN_W_DATA = 13101
IMSL_ERR_TOL = 15054
IMSL_MAX_EVALS = 10277
IMSL_N_EVALS = 10023
imslmath = loadimsl(MATH)


def zeroUnivariate(fcn, a, b, errTol=None, maxEvals=None, nEvals=None):
    """ Finds a zero of a real univariate function.
    """
    imslmath.imsl_d_zero_univariate.restype = None
    shape = []
    evalstring = 'imslmath.imsl_d_zero_univariate('
    # evalstring +='usr_fcn(fcn)'
    checkForCallable(fcn, 'fcn')
    TMP_FCN = CFUNCTYPE(c_double, c_double)
    tmp_fcn = TMP_FCN(fcn)
    evalstring += 'tmp_fcn'
    evalstring += ','
    a_tmp = a[0]
    if (not(isinstance(a_tmp, c_double))):
        a_tmp = c_double(a[0])
    evalstring += 'byref(a_tmp)'
    evalstring += ','
    b_tmp = b[0]
    if (not(isinstance(b_tmp, c_double))):
        b_tmp = c_double(b[0])
    evalstring += 'byref(b_tmp)'
    """
    if not (fcnWData is None):
        evalstring +=','
        evalstring += repr(IMSL_FCN_W_DATA)
        checkForDict(fcnWData,'fcnWData',['fcnWData','x','data'])
        evalstring +=','
        tmp_fcnWData_fcnWData_param = fcnWData['fcnWData']
        checkForCallable(tmp_fcnWData_fcnWData_param,'fcnWData')
        TMP_FCNWDATA_FCNWDATA=CFUNCTYPE(c_double,c_double,POINTER(c_double))
        tmp_fcnWData_fcnWData=TMP_FCNWDATA_FCNWDATA(tmp_fcnWData_fcnWData_param)
        evalstring += 'tmp_fcnWData_fcnWData'
        evalstring +=','
        fcnWData_x_tmp = fcnWData['x']
        evalstring +='c_double(fcnWData_x_tmp)'
        evalstring +=','
        fcnWData_data_tmp = fcnWData['data']
        fcnWData_data_tmp = toNumpyArray(fcnWData_data_tmp, 'data', shape=shape, dtype='double')
        evalstring +='fcnWData_data_tmp.ctypes.data_as(c_void_p)'
    """
    if not (errTol is None):
        evalstring += ','
        evalstring += repr(IMSL_ERR_TOL)
        evalstring += ','
        evalstring += 'c_double(errTol)'
    if not (maxEvals is None):
        evalstring += ','
        evalstring += repr(IMSL_MAX_EVALS)
        evalstring += ','
        evalstring += 'c_int(maxEvals)'
    if not (nEvals is None):
        evalstring += ','
        evalstring += repr(IMSL_N_EVALS)
        checkForList(nEvals, 'nEvals')
        evalstring += ','
        nEvals_nEvals_tmp = c_int()
        evalstring += 'byref(nEvals_nEvals_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    processRet(a_tmp, inout=True, shape=(1), pyvar=a)
    processRet(b_tmp, inout=True, shape=(1), pyvar=b)
    if not (nEvals is None):
        processRet(nEvals_nEvals_tmp, shape=(1), pyvar=nEvals)
    return
