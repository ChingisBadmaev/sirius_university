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
from pyimsl.util.imslUtils import STAT, checkForCallable, checkForDict, fatalErrorCheck, loadimsl, processRet, toNumpyArray, checkForList
from numpy import double, dtype, shape, size
from ctypes import CFUNCTYPE, POINTER, byref, c_double, c_int, c_void_p

IMSLS_FCN_W_DATA = 40020
imslstat = loadimsl(STAT)


def randomNpp(tbegin, tend, ftheta, thetaMin, thetaMax, neub, ne, fcnWData=None):
    """ Generates pseudorandom numbers from a nonhomogeneous Poisson process.
    """
    imslstat.imsls_d_random_npp.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_random_npp('
    evalstring += 'c_double(tbegin)'
    evalstring += ','
    evalstring += 'c_double(tend)'
    evalstring += ','
    checkForCallable(ftheta, 'ftheta')
    TMP_FTHETA = CFUNCTYPE(c_double, c_double)
    tmp_ftheta = TMP_FTHETA(ftheta)
    evalstring += 'tmp_ftheta'
    evalstring += ','
    evalstring += 'c_double(thetaMin)'
    evalstring += ','
    evalstring += 'c_double(thetaMax)'
    evalstring += ','
    evalstring += 'c_int(neub)'
    evalstring += ','
    checkForList(ne, 'ne')
    ne_tmp = c_int()
    evalstring += 'byref(ne_tmp)'
    if not (fcnWData is None):
        evalstring += ','
        evalstring += repr(IMSLS_FCN_W_DATA)
        checkForDict(fcnWData, 'fcnWData', ['ftheta', 'data'])
        evalstring += ','
        tmp_fcnWData_fcnWData_param = fcnWData['ftheta']
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
    fatalErrorCheck(STAT)
    processRet(ne_tmp, shape=1, pyvar=ne)
    return processRet(result, shape=(neub), result=True)
