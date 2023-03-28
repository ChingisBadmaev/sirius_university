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
from pyimsl.util.imslUtils import STAT, checkForBoolean, checkForCallable, checkForList, checkForDict, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, ndarray, shape, size
from ctypes import CFUNCTYPE, POINTER, byref, c_double, c_int, c_void_p
IMSLS_INDEX_ONLY = 40004
IMSLS_RETURN_USER = 14280
IMSLS_FCN_W_DATA = 40020
imslstat = loadimsl(STAT)


def discreteTableSetup(prf, t_del, nndx, imin, nmass, indexOnly=None, returnUser=None, fcnWData=None):
    """ Sets up table to generate pseudorandom numbers from a general discrete distribution.
    """
    imslstat.imsls_d_discrete_table_setup.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_discrete_table_setup('
    checkForCallable(prf, 'prf')
    TMP_PRF = CFUNCTYPE(c_double, c_int)
    tmp_prf = TMP_PRF(prf)
    evalstring += 'tmp_prf'
    evalstring += ','
    evalstring += 'c_double(t_del)'
    evalstring += ','
    evalstring += 'c_int(nndx)'
    evalstring += ','
    imin_tmp = imin[0]
    if (not(isinstance(imin_tmp, c_int))):
        imin_tmp = c_int(imin[0])
    evalstring += 'byref(imin_tmp)'
    evalstring += ','
    nmass_tmp = nmass[0]
    if (not(isinstance(nmass_tmp, c_int))):
        nmass_tmp = c_int(nmass[0])
    evalstring += 'byref(nmass_tmp)'
    checkForBoolean(indexOnly, 'indexOnly')
    if (indexOnly):
        evalstring += ','
        evalstring += repr(IMSLS_INDEX_ONLY)
    if not (returnUser is None):
        evalstring += ','
        evalstring += repr(IMSLS_RETURN_USER)
        checkForDict(returnUser, 'returnUser', ['cumpr', 'lcumpr'])
        evalstring += ','
        returnUser_cumpr_tmp = returnUser['cumpr']
        if (not(isinstance(returnUser_cumpr_tmp, ndarray))):
            returnUser_cumpr_tmp = toNumpyArray(
                cumpr, 'cumpr', shape=shape, dtype='double', expectedShape=(nmass_tmp + nndx))
            returnUser[0] = returnUser_cumpr_tmp
        evalstring += 'returnUser_cumpr_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        returnUser_lcumpr_tmp = returnUser['lcumpr']
        # don't pass lcumpr by reference.  This is just an input variable.
        # If passed by ref then Linux64 causes fatal errors.  The CNL code
        # expects an int.
        # if (not(isinstance(returnUser_lcumpr_tmp, c_int))):
        #        returnUser_lcumpr_tmp=c_int(returnUser[1])
        #        returnUser[1] = returnUser_lcumpr_tmp
        evalstring += 'c_int(returnUser_lcumpr_tmp)'
    if not (fcnWData is None):
        evalstring += ','
        evalstring += repr(IMSLS_FCN_W_DATA)
        checkForDict(fcnWData, 'fcnWData', ['prf', 'data'])
        evalstring += ','
        tmp_fcnWData_fcnWData_param = fcnWData['prf']
        checkForCallable(tmp_fcnWData_fcnWData_param, 'fcnWData')
        TMP_FCNWDATA_FCNWDATA = CFUNCTYPE(c_double, c_int, POINTER(c_double))
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
    print(imin_tmp.value, nmass_tmp.value)
    if isinstance(imin, list):
        imin[:] = []
    processRet(imin_tmp, shape=(1), pyvar=imin)
    if isinstance(nmass, list):
        nmass[:] = []
    processRet(nmass_tmp, shape=(1), pyvar=nmass)
    if(returnUser is None):
        freemem = True
    else:
        freemem = False
    return processRet(result, shape=(nmass_tmp.value + nndx), result=True, freemem=freemem)
