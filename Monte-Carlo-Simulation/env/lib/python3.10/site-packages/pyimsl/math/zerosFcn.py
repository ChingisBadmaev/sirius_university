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
from numpy import double, dtype, info, shape, size
from ctypes import CFUNCTYPE, POINTER, byref, c_double, c_int, c_void_p

IMSL_XGUESS = 10100
IMSL_NUM_ROOTS = 10018
IMSL_ERR_ABS = 10010
IMSL_ERR_REL = 10011
IMSL_ETA = 10012
IMSL_EPS = 10013
IMSL_MAX_ITN = 10113
IMSL_INFO = 10017
IMSL_FCN_W_DATA = 13101
imslmath = loadimsl(MATH)


def zerosFcn(fcn, xguess=None, numRoots=None, errAbs=None, errRel=None, eta=None, eps=None, maxItn=None, info=None, fcnWData=None):
    """ Finds the real zeros of a real function using Miller's method.
    """
    nroot = 1      # Default is 1 root
    imslmath.imsl_d_zeros_fcn.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslmath.imsl_d_zeros_fcn('
    checkForCallable(fcn, 'fcn')
    TMP_FCN = CFUNCTYPE(c_double, c_double)
    tmp_fcn = TMP_FCN(fcn)
    evalstring += 'tmp_fcn'
    if not (numRoots is None):
        evalstring += ','
        evalstring += repr(IMSL_NUM_ROOTS)
        evalstring += ','
        evalstring += 'c_int(numRoots)'
        nroot = numRoots
    if not (xguess is None):
        if not (numRoots is None):
            xguess = toNumpyArray(
                xguess, 'xguess', shape=shape, dtype='double', expectedShape=(nroot))
        else:
            # If xguess is specified, the number of roots is implied
            # by the number of elements in xguess.
            xguess = toNumpyArray(
                xguess, 'xguess', shape=shape, dtype='double', expectedShape=(0))
            nroot = len(xguess)
            evalstring += ','
            evalstring += repr(IMSL_NUM_ROOTS)
            evalstring += ','
            evalstring += 'c_int(nroot)'
            xguess = toNumpyArray(
                xguess, 'xguess', shape=shape, dtype='double', expectedShape=(0))
            nroot = len(xguess)
        evalstring += ','
        evalstring += repr(IMSL_XGUESS)
        evalstring += ','
        evalstring += 'xguess.ctypes.data_as(c_void_p)'
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
    if not (eta is None):
        evalstring += ','
        evalstring += repr(IMSL_ETA)
        evalstring += ','
        evalstring += 'c_double(eta)'
    if not (eps is None):
        evalstring += ','
        evalstring += repr(IMSL_EPS)
        evalstring += ','
        evalstring += 'c_double(eps)'
    if not (maxItn is None):
        evalstring += ','
        evalstring += repr(IMSL_MAX_ITN)
        evalstring += ','
        evalstring += 'c_int(maxItn)'
    if not (info is None):
        evalstring += ','
        evalstring += repr(IMSL_INFO)
        checkForList(info, 'info')
        evalstring += ','
        info_info_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(info_info_tmp)'
    if not (fcnWData is None):
        evalstring += ','
        evalstring += repr(IMSL_FCN_W_DATA)
        checkForDict(fcnWData, 'fcnWData', ['fcn', 'data'])
        evalstring += ','
        tmp_fcnWData_fcnWData_param = fcnWData['fcn']
        checkForCallable(tmp_fcnWData_fcnWData_param, 'fcnWData')
        TMP_FCNWDATA_FCNWDATA = CFUNCTYPE(
            c_double, c_double, POINTER(c_double))
        tmp_fcnWData_fcnWData = TMP_FCNWDATA_FCNWDATA(
            tmp_fcnWData_fcnWData_param)
        evalstring += 'tmp_fcnWData_fcnWData'
        evalstring += ','
        fcnWData_data_tmp = fcnWData['data']
        fcnWData_data_tmp = toNumpyArray(
            fcnWData_data_tmp, 'data', shape=shape, dtype='double')
        evalstring += 'fcnWData_data_tmp.ctypes.data_as(c_void_p)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (info is None):
        processRet(info_info_tmp, shape=(nroot), pyvar=info)
    return processRet(result, shape=(nroot), result=True)
