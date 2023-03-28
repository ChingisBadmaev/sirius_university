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
from pyimsl.util.imslUtils import STAT, checkForCallable, checkForList, fatalErrorCheck, loadimsl, processRet, toNumpyArray, checkForDict
from numpy import double, dtype, shape, size
from ctypes import CFUNCTYPE, POINTER, byref, c_double, c_int, c_void_p

IMSLS_DIFFERENCES = 30018
IMSLS_N_MISSING = 13440
IMSLS_FCN_W_DATA = 40020
imslstat = loadimsl(STAT)


def kolmogorovOne(cdf, x, differences=None, nMissing=None, fcnWData=None):
    """ Performs a Kolmogorov-Smirnov one-sample test for continuous distributions.
    """
    imslstat.imsls_d_kolmogorov_one.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_kolmogorov_one('
    checkForCallable(cdf, 'cdf')
    TMP_CDF = CFUNCTYPE(c_double, c_double)
    tmp_cdf = TMP_CDF(cdf)
    evalstring += 'tmp_cdf'
    evalstring += ','
    evalstring += 'c_int(nObservations)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nObservations = shape[0]
    if not (differences is None):
        evalstring += ','
        evalstring += repr(IMSLS_DIFFERENCES)
        checkForList(differences, 'differences')
        evalstring += ','
        differences_differences_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(differences_differences_tmp)'
    if not (nMissing is None):
        evalstring += ','
        evalstring += repr(IMSLS_N_MISSING)
        checkForList(nMissing, 'nMissing')
        evalstring += ','
        nMissing_nMissing_tmp = c_int()
        evalstring += 'byref(nMissing_nMissing_tmp)'
    if not (fcnWData is None):
        evalstring += ','
        evalstring += repr(IMSLS_FCN_W_DATA)
        checkForDict(fcnWData, 'fcnWData', ['fcnWData', 'data'])
        evalstring += ','
        tmp_fcnWData_fcnWData_param = fcnWData['fcnWData']
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
    if not (differences is None):
        processRet(differences_differences_tmp, shape=(3), pyvar=differences)
    if not (nMissing is None):
        processRet(nMissing_nMissing_tmp, shape=(1), pyvar=nMissing)
    return processRet(result, shape=(3), result=True)
