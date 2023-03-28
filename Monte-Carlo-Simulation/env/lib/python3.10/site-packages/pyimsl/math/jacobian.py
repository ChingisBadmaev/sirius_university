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

IMSL_YSCALE = 15110
IMSL_METHOD = 10309
IMSL_ACCUMULATE = 15114
IMSL_FACTOR = 10004
IMSL_ISTATUS = 15053
IMSL_FCN_W_DATA = 13101

# Legal values for method
DD_ONE_SIDED = 0
DD_CENTRAL = 1
DD_SKIP = 3

imslmath = loadimsl(MATH)


def jacobian(fcn, y, f, fjac, yscale=None, method=None, accumulate=None, factor=None, istatus=None):
    """ Approximates the Jacobian of m functions in n unknowns using divided differences.
    """
    # imslmath.imsl_d_jacobian.restype = c_double
    imslmath.imsl_d_jacobian.restype = None
    shape = []
    evalstring = 'imslmath.imsl_d_jacobian('
    checkForCallable(fcn, 'fcn')
    TMP_FCN = CFUNCTYPE(None, c_int, POINTER(c_double), POINTER(c_double))
    tmp_fcn = TMP_FCN(fcn)
    evalstring += 'tmp_fcn'
    evalstring += ','
    evalstring += 'c_int(m)'
    evalstring += ','
    evalstring += 'c_int(n)'
    evalstring += ','
    y = toNumpyArray(y, 'y', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'y.ctypes.data_as(c_void_p)'
    n = shape[0]
    evalstring += ','
    # f_tmp = POINTER(c_double)(c_double())
    # evalstring += 'byref(f_tmp)'
    f_tmp = toNumpyArray(f, 'f', shape=shape,
                         dtype='double', expectedShape=(0))
    evalstring += 'f_tmp.ctypes.data_as(c_void_p)'
    m = shape[0]
    evalstring += ','
    # fjac_tmp = toNumpyArray(fjac, 'fjac', shape=shape, dtype='double', expectedShape=(0,n))
    fjac_tmp = toNumpyArray(fjac, 'fjac', shape=shape,
                            dtype='double', expectedShape=(m, n))
    evalstring += 'fjac_tmp.ctypes.data_as(c_void_p)'
    # m=shape[0]
    if not (yscale is None):
        evalstring += ','
        evalstring += repr(IMSL_YSCALE)
        evalstring += ','
        yscale = toNumpyArray(yscale, 'yscale', shape=shape,
                              dtype='double', expectedShape=(n))
        evalstring += 'yscale.ctypes.data_as(c_void_p)'
    if not (method is None):
        evalstring += ','
        evalstring += repr(IMSL_METHOD)
        evalstring += ','
        method = toNumpyArray(method, 'method', shape=shape,
                              dtype='int', expectedShape=(n))
        evalstring += 'method.ctypes.data_as(c_void_p)'
    checkForBoolean(accumulate, 'accumulate')
    if (accumulate):
        evalstring += ','
        evalstring += repr(IMSL_ACCUMULATE)
    if not (factor is None):
        evalstring += ','
        evalstring += repr(IMSL_FACTOR)
        evalstring += ','
        factor = toNumpyArray(factor, 'factor', shape=shape,
                              dtype='double', expectedShape=(n))
        evalstring += 'factor.ctypes.data_as(c_void_p)'
    if not (istatus is None):
        evalstring += ','
        evalstring += repr(IMSL_ISTATUS)
        evalstring += ','
        istatus = toNumpyArray(
            istatus, 'istatus', shape=shape, dtype='int', expectedShape=(10))
        evalstring += 'istatus.ctypes.data_as(c_void_p)'
    """
    if not (fcnWData is None):
        evalstring +=','
        evalstring += repr(IMSL_FCN_W_DATA)
        checkForDict(fcnWData,'fcnWData',['fcnWData','indx','y','data'])
        evalstring +=','
        tmp_fcnWData_fcnWData_param = fcnWData['fcnWData']
        checkForCallable(tmp_fcnWData_fcnWData_param,'fcnWData')
        TMP_FCNWDATA_FCNWDATA=CFUNCTYPE(None,c_int,POINTER(c_double),POINTER(c_double),POINTER(c_double))
        tmp_fcnWData_fcnWData=TMP_FCNWDATA_FCNWDATA(tmp_fcnWData_fcnWData_param)
        evalstring += 'tmp_fcnWData_fcnWData'
        evalstring +=','
        fcnWData_indx_tmp = fcnWData['indx']
        evalstring +='c_int(fcnWData_indx_tmp)'
        evalstring +=','
        fcnWData_y_tmp = fcnWData['y']
        fcnWData_y_tmp = toNumpyArray(fcnWData_y_tmp, 'y', shape=shape, dtype='double', expectedShape=(n))
        evalstring +='fcnWData_y_tmp.ctypes.data_as(c_void_p)'
        evalstring +=','
        fcnWData_f_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(fcnWData_f_tmp)'
        evalstring +=','
        fcnWData_data_tmp = fcnWData['data']
        fcnWData_data_tmp = toNumpyArray(fcnWData_data_tmp, 'data', shape=shape, dtype='double')
        evalstring +='fcnWData_data_tmp.ctypes.data_as(c_void_p)'
    """
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    processRet(f_tmp, shape=(m), pyvar=f)
    processRet(fjac_tmp, inout=True, shape=(m, n), pyvar=fjac)
    # if not (fcnWData is None):
    #    processRet(fcnWData_f_tmp, shape=(m), key='f', pyvar=fcnWData)
    # return result
    return
