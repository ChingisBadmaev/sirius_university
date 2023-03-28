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
from pyimsl.util.imslUtils import STAT, checkForBoolean, checkForCallable, checkForList, fatalErrorCheck, loadimsl, processRet, toNumpyArray, checkForDict
from numpy import double, dtype, ndarray, shape, size
from ctypes import CFUNCTYPE, POINTER, byref, c_double, c_int, c_void_p

IMSLS_N_PARAMETERS_ESTIMATED = 13450
IMSLS_CUTPOINTS = 11090
IMSLS_CUTPOINTS_USER = 11110
IMSLS_CUTPOINTS_EQUAL = 11100
IMSLS_CHI_SQUARED = 10450
IMSLS_DEGREES_OF_FREEDOM = 11140
IMSLS_FREQUENCIES = 11790
IMSLS_BOUNDS = 10290
IMSLS_CELL_COUNTS = 10360
IMSLS_CELL_EXPECTED = 10380
IMSLS_CELL_CHI_SQUARED = 10340
IMSLS_FCN_W_DATA = 40020
IMSLS_IDO = 20440
imslstat = loadimsl(STAT)


def chiSquaredTest(userProcCdf, nCategories, x, nParametersEstimated=None, cutpoints=None, cutpointsUser=None, cutpointsEqual=None, chiSquared=None, degreesOfFreedom=None, frequencies=None, bounds=None, cellCounts=None, cellExpected=None, cellChiSquared=None, fcnWData=None, ido=None):
    """ Performs a chi-squared goodness-of-fit test.
    """
    imslstat.imsls_d_chi_squared_test.restype = c_double
    shape = []
    evalstring = 'imslstat.imsls_d_chi_squared_test('
    checkForCallable(userProcCdf, 'userProcCdf')
    TMP_USERPROCCDF = CFUNCTYPE(c_double, c_double)
    tmp_userProcCdf = TMP_USERPROCCDF(userProcCdf)
    evalstring += 'tmp_userProcCdf'
    evalstring += ','
    evalstring += 'c_int(nObservations)'
    evalstring += ','
    evalstring += 'c_int(nCategories)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nObservations = shape[0]
    if not (nParametersEstimated is None):
        evalstring += ','
        evalstring += repr(IMSLS_N_PARAMETERS_ESTIMATED)
        evalstring += ','
        evalstring += 'c_int(nParametersEstimated)'
    if not (cutpoints is None):
        evalstring += ','
        evalstring += repr(IMSLS_CUTPOINTS)
        checkForList(cutpoints, 'cutpoints')
        evalstring += ','
        cutpoints_cutpoints_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(cutpoints_cutpoints_tmp)'
    if not (cutpointsUser is None):
        evalstring += ','
        evalstring += repr(IMSLS_CUTPOINTS_USER)
        cutpointsUser_tmp = cutpointsUser[0]
        if (not(isinstance(cutpointsUser_tmp, ndarray))):
            cutpointsUser_tmp = toNumpyArray(
                cutpointsUser_tmp, 'cutpointsUser', shape=shape, expectedShape=(nCategories - 1))
            cutpointsUser[0] = cutpointsUser_tmp
        evalstring += ','
        evalstring += 'cutpointsUser_tmp.ctypes.data_as(c_void_p)'
    checkForBoolean(cutpointsEqual, 'cutpointsEqual')
    if (cutpointsEqual):
        evalstring += ','
        evalstring += repr(IMSLS_CUTPOINTS_EQUAL)
    if not (chiSquared is None):
        evalstring += ','
        evalstring += repr(IMSLS_CHI_SQUARED)
        checkForList(chiSquared, 'chiSquared')
        evalstring += ','
        chiSquared_chiSquared_tmp = c_double()
        evalstring += 'byref(chiSquared_chiSquared_tmp)'
    if not (degreesOfFreedom is None):
        evalstring += ','
        evalstring += repr(IMSLS_DEGREES_OF_FREEDOM)
        checkForList(degreesOfFreedom, 'degreesOfFreedom')
        evalstring += ','
        degreesOfFreedom_df_tmp = c_double()
        evalstring += 'byref(degreesOfFreedom_df_tmp)'
    if not (frequencies is None):
        evalstring += ','
        evalstring += repr(IMSLS_FREQUENCIES)
        evalstring += ','
        frequencies = toNumpyArray(
            frequencies, 'frequencies', shape=shape, dtype='double', expectedShape=(nObservations))
        evalstring += 'frequencies.ctypes.data_as(c_void_p)'
    if not (bounds is None):
        evalstring += ','
        evalstring += repr(IMSLS_BOUNDS)
        checkForDict(bounds, 'bounds', ['lowerBound', 'upperBound'])
        evalstring += ','
        bounds_lowerBound_tmp = bounds['lowerBound']
        evalstring += 'c_double(bounds_lowerBound_tmp)'
        evalstring += ','
        bounds_upperBound_tmp = bounds['upperBound']
        evalstring += 'c_double(bounds_upperBound_tmp)'
    if not (cellCounts is None):
        evalstring += ','
        evalstring += repr(IMSLS_CELL_COUNTS)
        checkForList(cellCounts, 'cellCounts')
        evalstring += ','
        cellCounts_cellCounts_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(cellCounts_cellCounts_tmp)'
    if not (cellExpected is None):
        evalstring += ','
        evalstring += repr(IMSLS_CELL_EXPECTED)
        checkForList(cellExpected, 'cellExpected')
        evalstring += ','
        cellExpected_cellExpected_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(cellExpected_cellExpected_tmp)'
    if not (cellChiSquared is None):
        evalstring += ','
        evalstring += repr(IMSLS_CELL_CHI_SQUARED)
        checkForList(cellChiSquared, 'cellChiSquared')
        evalstring += ','
        cellChiSquared_cellChiSquared_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(cellChiSquared_cellChiSquared_tmp)'
    if not (fcnWData is None):
        evalstring += ','
        evalstring += repr(IMSLS_FCN_W_DATA)
        checkForDict(fcnWData, 'fcnWData', ['fcnWData', 'data'])
        evalstring += ','
        tmp_fcnWData_fcnWData_param = fcnWData[0]
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
    if not (ido is None):
        evalstring += ','
        evalstring += repr(IMSLS_IDO)
        evalstring += ','
        evalstring += 'c_int(ido)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (cutpoints is None):
        processRet(cutpoints_cutpoints_tmp, shape=(
            nCategories - 1), pyvar=cutpoints)
    if not (chiSquared is None):
        processRet(chiSquared_chiSquared_tmp, shape=(1), pyvar=chiSquared)
    if not (degreesOfFreedom is None):
        processRet(degreesOfFreedom_df_tmp, shape=(1), pyvar=degreesOfFreedom)
    if not (cellCounts is None):
        processRet(cellCounts_cellCounts_tmp, shape=(
            nCategories), pyvar=cellCounts)
    if not (cellExpected is None):
        processRet(cellExpected_cellExpected_tmp,
                   shape=(nCategories), pyvar=cellExpected)
    if not (cellChiSquared is None):
        processRet(cellChiSquared_cellChiSquared_tmp,
                   shape=(nCategories), pyvar=cellChiSquared)
    return result
