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

IMSL_TOLERANCE = 10053
IMSL_FCN_W_DATA = 13101
IMSL_LOWER_ENDPOINT = 15019
IMSL_UPPER_ENDPOINT = 15020
imslmath = loadimsl(MATH)


def minUnconGolden(fcn, a, b, tolerance=None, fcnWData=None, lowerEndpoint=None, upperEndpoint=None):
    VersionFacade.checkVersion(7)
    imslmath.imsl_d_min_uncon_golden.restype = c_double
    shape = []
    evalstring = 'imslmath.imsl_d_min_uncon_golden('
    checkForCallable(fcn, 'fcn')
    TMP_FCN = CFUNCTYPE(c_double, c_double)
    tmp_fcn = TMP_FCN(fcn)
    evalstring += 'tmp_fcn'
    evalstring += ','
    evalstring += 'c_double(a)'
    evalstring += ','
    evalstring += 'c_double(b)'
    if not (tolerance is None):
        evalstring += ','
        evalstring += repr(IMSL_TOLERANCE)
        evalstring += ','
        evalstring += 'c_double(tolerance)'
    if not (fcnWData is None):
        evalstring += ','
        evalstring += repr(IMSL_FCN_W_DATA)
        checkForDict(fcnWData, 'fcnWData', ['fcnWData', 'data'])
        evalstring += ','
        tmp_fcnWData_fcnWData_param = fcnWData['fcnWData']
        checkForCallable(tmp_fcnWData_fcnWData_param, 'fcnWData')
        TMP_FCNWDATA_FCNWDATA = CFUNCTYPE(c_double, POINTER(c_double))
        tmp_fcnWData_fcnWData = TMP_FCNWDATA_FCNWDATA(
            tmp_fcnWData_fcnWData_param)
        evalstring += 'tmp_fcnWData_fcnWData'
        evalstring += ','
        fcnWData_data_tmp = fcnWData['data']
        fcnWData_data_tmp = toNumpyArray(
            fcnWData_data_tmp, 'data', shape=shape, dtype='double')
        evalstring += 'fcnWData_data_tmp.ctypes.data_as(c_void_p)'
    if not (lowerEndpoint is None):
        evalstring += ','
        evalstring += repr(IMSL_LOWER_ENDPOINT)
        checkForList(lowerEndpoint, 'lowerEndpoint')
        evalstring += ','
        lowerEndpoint_lower_tmp = c_double()
        evalstring += 'byref(lowerEndpoint_lower_tmp)'
    if not (upperEndpoint is None):
        evalstring += ','
        evalstring += repr(IMSL_UPPER_ENDPOINT)
        checkForList(upperEndpoint, 'upperEndpoint')
        evalstring += ','
        upperEndpoint_upper_tmp = c_double()
        evalstring += 'byref(upperEndpoint_upper_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (lowerEndpoint is None):
        processRet(lowerEndpoint_lower_tmp, shape=(1), pyvar=lowerEndpoint)
    if not (upperEndpoint is None):
        processRet(upperEndpoint_upper_tmp, shape=(1), pyvar=upperEndpoint)
    return result
